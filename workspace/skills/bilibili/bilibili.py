#!/usr/bin/env python3
"""
B站视频信息获取工具
用于获取视频详情、评论、下载地址等
支持登录凭据以获取完整评论
"""

import argparse
import asyncio
import json
import os
import re
import sys
import io

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from bilibili_api import video, comment, Credential
    from bilibili_api.comment import CommentResourceType
except ImportError:
    print(json.dumps({
        "error": "Missing bilibili-api-python. Run: pip install bilibili-api-python aiohttp"
    }))
    sys.exit(1)


# 配置文件路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")


def load_credential() -> Credential | None:
    """从配置文件加载登录凭据"""
    if not os.path.exists(CONFIG_FILE):
        return None
    
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        sessdata = config.get("SESSDATA")
        bili_jct = config.get("bili_jct")
        buvid3 = config.get("buvid3")
        dedeuserid = config.get("DedeUserID")
        ac_time_value = config.get("ac_time_value")
        
        if sessdata and bili_jct:
            return Credential(
                sessdata=sessdata,
                bili_jct=bili_jct,
                buvid3=buvid3,
                dedeuserid=dedeuserid,
                ac_time_value=ac_time_value
            )
    except Exception:
        pass
    
    return None


def extract_bvid(url_or_bvid: str) -> str:
    """从URL或直接的BV号中提取BV号"""
    # 如果已经是BV号格式
    if url_or_bvid.startswith("BV") and len(url_or_bvid) == 12:
        return url_or_bvid
    
    # 从URL中提取
    patterns = [
        r'BV[a-zA-Z0-9]{10}',  # 标准BV号
        r'/video/(BV[a-zA-Z0-9]{10})',  # URL中的BV号
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url_or_bvid)
        if match:
            bvid = match.group(0) if 'BV' in match.group(0) else match.group(1)
            if bvid.startswith("BV"):
                return bvid
    
    return url_or_bvid  # 返回原始输入


async def get_video_info(bvid: str, credential: Credential = None) -> dict:
    """获取视频基本信息"""
    try:
        v = video.Video(bvid=bvid, credential=credential)
        info = await v.get_info()
        
        # 提取关键信息
        result = {
            "bvid": info.get("bvid"),
            "aid": info.get("aid"),
            "title": info.get("title"),
            "description": info.get("desc"),
            "duration": info.get("duration"),  # 秒
            "duration_text": f"{info.get('duration', 0) // 60}:{info.get('duration', 0) % 60:02d}",
            "cover": info.get("pic"),
            "publish_time": info.get("pubdate"),
            "stats": {
                "view": info.get("stat", {}).get("view"),  # 播放量
                "danmaku": info.get("stat", {}).get("danmaku"),  # 弹幕数
                "like": info.get("stat", {}).get("like"),  # 点赞
                "coin": info.get("stat", {}).get("coin"),  # 投币
                "favorite": info.get("stat", {}).get("favorite"),  # 收藏
                "share": info.get("stat", {}).get("share"),  # 分享
                "reply": info.get("stat", {}).get("reply"),  # 评论数
            },
            "owner": {
                "uid": info.get("owner", {}).get("mid"),
                "name": info.get("owner", {}).get("name"),
                "face": info.get("owner", {}).get("face"),
            },
            "tags": [tag.get("tag_name") for tag in info.get("tags", []) if tag.get("tag_name")],
            "url": f"https://www.bilibili.com/video/{bvid}",
        }
        
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


async def get_video_comments(bvid: str, count: int = 20, credential: Credential = None) -> dict:
    """获取视频评论"""
    try:
        v = video.Video(bvid=bvid, credential=credential)
        info = await v.get_info()
        aid = info.get("aid")
        
        # 获取评论
        comments_data = await comment.get_comments(
            oid=aid,
            type_=CommentResourceType.VIDEO,
            page_index=1,
            credential=credential
        )
        
        comments = []
        replies = comments_data.get("replies", []) or []
        
        for c in replies[:count]:
            comments.append({
                "user": c.get("member", {}).get("uname"),
                "user_uid": c.get("member", {}).get("mid"),
                "content": c.get("content", {}).get("message"),
                "like": c.get("like"),
                "reply_count": c.get("rcount"),
                "time": c.get("ctime"),
            })
        
        return {
            "success": True,
            "data": {
                "bvid": bvid,
                "total_comments": comments_data.get("page", {}).get("count", 0),
                "fetched": len(comments),
                "logged_in": credential is not None,
                "comments": comments
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def get_download_url(bvid: str, credential: Credential = None) -> dict:
    """获取视频下载地址"""
    try:
        v = video.Video(bvid=bvid, credential=credential)
        
        # 获取下载地址
        download_url = await v.get_download_url(page_index=0)
        
        # 提取视频和音频地址
        result = {
            "bvid": bvid,
            "video_urls": [],
            "audio_urls": [],
        }
        
        # 检查 dash 格式
        if "dash" in download_url:
            dash = download_url["dash"]
            
            # 视频流
            for v_stream in dash.get("video", [])[:3]:  # 取前3个质量
                result["video_urls"].append({
                    "quality": v_stream.get("id"),
                    "codecs": v_stream.get("codecs"),
                    "url": v_stream.get("base_url") or v_stream.get("baseUrl"),
                    "bandwidth": v_stream.get("bandwidth"),
                })
            
            # 音频流
            for a_stream in dash.get("audio", [])[:2]:
                result["audio_urls"].append({
                    "quality": a_stream.get("id"),
                    "codecs": a_stream.get("codecs"),
                    "url": a_stream.get("base_url") or a_stream.get("baseUrl"),
                    "bandwidth": a_stream.get("bandwidth"),
                })
        
        # 检查 durl 格式（旧版）
        if "durl" in download_url:
            for durl in download_url["durl"]:
                result["video_urls"].append({
                    "quality": download_url.get("quality"),
                    "url": durl.get("url"),
                    "size": durl.get("size"),
                })
        
        result["note"] = "下载链接有时效性，需要添加 Referer: https://www.bilibili.com 请求头"
        
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


async def login_qrcode() -> dict:
    """通过扫码登录获取凭据"""
    try:
        from bilibili_api.login_v2 import QrCodeLogin, QrCodeLoginEvents
        import time
        
        qr = QrCodeLogin()
        await qr.generate_qrcode()
        
        # 打印二维码到终端
        print("请使用B站APP扫描以下二维码登录：\n")
        print(qr.get_qrcode_terminal())
        print("\n等待扫码...")
        
        # 轮询检查登录状态
        while True:
            state = await qr.check_state()
            if state == QrCodeLoginEvents.SCAN:
                print("已扫码，请在手机上确认...")
            elif state == QrCodeLoginEvents.CONF:
                print("已确认，正在登录...")
            elif state == QrCodeLoginEvents.DONE:
                break
            elif state == QrCodeLoginEvents.TIMEOUT:
                return {"success": False, "error": "二维码已过期，请重试"}
            time.sleep(1)
        
        credential = qr.get_credential()
        
        if credential:
            # 保存凭据到配置文件
            config = {
                "SESSDATA": credential.sessdata,
                "bili_jct": credential.bili_jct,
                "buvid3": credential.buvid3,
                "DedeUserID": credential.dedeuserid,
                "ac_time_value": credential.ac_time_value,
            }
            
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            return {"success": True, "message": "登录成功，凭据已保存"}
        else:
            return {"success": False, "error": "登录失败"}
    except Exception as e:
        return {"success": False, "error": str(e)}


async def check_login() -> dict:
    """检查登录状态"""
    credential = load_credential()
    if credential:
        try:
            # 验证凭据是否有效
            from bilibili_api import user
            self_info = await user.get_self_info(credential)
            return {
                "success": True,
                "logged_in": True,
                "user": {
                    "uid": self_info.get("mid"),
                    "name": self_info.get("name"),
                    "face": self_info.get("face"),
                }
            }
        except Exception as e:
            return {"success": True, "logged_in": False, "error": str(e)}
    return {"success": True, "logged_in": False, "message": "未配置登录凭据"}


async def main():
    parser = argparse.ArgumentParser(description="B站视频信息获取工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # info 命令
    info_parser = subparsers.add_parser("info", help="获取视频基本信息")
    info_parser.add_argument("bvid", help="BV号或视频链接")
    
    # comments 命令
    comments_parser = subparsers.add_parser("comments", help="获取视频评论")
    comments_parser.add_argument("bvid", help="BV号或视频链接")
    comments_parser.add_argument("--count", type=int, default=20, help="获取评论数量（默认20）")
    
    # download 命令
    download_parser = subparsers.add_parser("download", help="获取视频下载地址")
    download_parser.add_argument("bvid", help="BV号或视频链接")
    
    # login 命令
    login_parser = subparsers.add_parser("login", help="扫码登录B站")
    
    # status 命令
    status_parser = subparsers.add_parser("status", help="检查登录状态")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 加载凭据
    credential = load_credential()
    
    if args.command == "login":
        result = await login_qrcode()
    elif args.command == "status":
        result = await check_login()
    else:
        bvid = extract_bvid(args.bvid)
        
        if args.command == "info":
            result = await get_video_info(bvid, credential)
        elif args.command == "comments":
            result = await get_video_comments(bvid, args.count, credential)
        elif args.command == "download":
            result = await get_download_url(bvid, credential)
        else:
            result = {"error": "Unknown command"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
