#!/usr/bin/env python3
"""
抖音视频信息获取工具
用于解析抖音视频链接，获取视频信息
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

import requests

try:
    from douyin_tiktok_scraper.scraper import Scraper
    HAS_SCRAPER = True
except ImportError:
    HAS_SCRAPER = False

# 配置文件路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.douyin.com/',
}


def load_cookie() -> str | None:
    """从配置文件加载 Cookie"""
    if not os.path.exists(CONFIG_FILE):
        return None
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config.get("cookie")
    except Exception:
        return None


def get_headers() -> dict:
    """获取请求头"""
    headers = HEADERS.copy()
    cookie = load_cookie()
    if cookie:
        headers['Cookie'] = cookie
    return headers


def extract_video_id(url: str) -> str | None:
    """从 URL 中提取视频 ID"""
    # 标准链接格式
    patterns = [
        r'/video/(\d+)',
        r'aweme_id=(\d+)',
        r'/(\d{19})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def resolve_short_url(url: str) -> str | None:
    """解析短链接获取真实 URL"""
    try:
        resp = requests.head(url, headers=get_headers(), allow_redirects=True, timeout=10)
        return resp.url
    except Exception:
        return None


async def get_video_info_scraper(url: str) -> dict:
    """使用 scraper 获取视频信息"""
    if not HAS_SCRAPER:
        return {"success": False, "error": "douyin-tiktok-scraper 未安装"}
    
    try:
        scraper = Scraper()
        data = await scraper.hybrid_parsing(url)
        
        if not data or data.get("status") == "failed":
            return {"success": False, "error": data.get("message", "解析失败")}
        
        # 提取视频信息
        result = {
            "video_id": data.get("aweme_id"),
            "title": data.get("desc"),
            "author": {
                "uid": data.get("author", {}).get("uid"),
                "nickname": data.get("author", {}).get("nickname"),
                "avatar": data.get("author", {}).get("avatar_thumb", {}).get("url_list", [None])[0],
            },
            "stats": {
                "digg_count": data.get("statistics", {}).get("digg_count"),
                "comment_count": data.get("statistics", {}).get("comment_count"),
                "share_count": data.get("statistics", {}).get("share_count"),
                "play_count": data.get("statistics", {}).get("play_count"),
            },
            "video": {
                "cover": data.get("video", {}).get("cover", {}).get("url_list", [None])[0],
                "duration": data.get("video", {}).get("duration"),
                "play_url": data.get("video", {}).get("play_addr", {}).get("url_list", [None])[0],
            },
            "music": {
                "title": data.get("music", {}).get("title"),
                "author": data.get("music", {}).get("author"),
            },
            "create_time": data.get("create_time"),
            "url": url,
        }
        
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_video_info_web(url: str) -> dict:
    """通过网页获取视频信息（备用方案）"""
    try:
        # 解析短链接
        if 'v.douyin.com' in url:
            real_url = resolve_short_url(url)
            if real_url:
                url = real_url
        
        video_id = extract_video_id(url)
        if not video_id:
            return {"success": False, "error": "无法提取视频 ID"}
        
        # 访问视频页面
        page_url = f'https://www.douyin.com/video/{video_id}'
        resp = requests.get(page_url, headers=get_headers(), timeout=15)
        
        if resp.status_code != 200:
            return {"success": False, "error": f"HTTP {resp.status_code}"}
        
        # 尝试从页面提取基本信息
        title_match = re.search(r'<title>([^<]+)</title>', resp.text)
        title = title_match.group(1) if title_match else None
        
        # 由于抖音使用客户端渲染，大部分数据需要 JS 执行才能获取
        return {
            "success": True,
            "data": {
                "video_id": video_id,
                "title": title,
                "url": page_url,
                "note": "抖音使用客户端渲染，详细数据需要登录或使用专业工具获取"
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_video_info(url: str) -> dict:
    """获取视频信息"""
    # 优先使用 scraper
    if HAS_SCRAPER:
        try:
            result = asyncio.run(get_video_info_scraper(url))
            if result.get("success"):
                return result
        except Exception:
            pass
    
    # 备用方案
    return get_video_info_web(url)


def check_status() -> dict:
    """检查配置状态"""
    status = {
        "success": True,
        "scraper_available": HAS_SCRAPER,
    }
    
    cookie = load_cookie()
    status["cookie_configured"] = cookie is not None
    
    # 测试网络连接
    try:
        resp = requests.get('https://www.douyin.com/', headers=get_headers(), timeout=10)
        status["network"] = f"HTTP {resp.status_code}"
    except Exception as e:
        status["network"] = f"Error: {str(e)}"
    
    return status


def main():
    parser = argparse.ArgumentParser(description="抖音视频信息获取工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # info 命令 - 获取视频信息
    info_parser = subparsers.add_parser("info", help="获取视频信息")
    info_parser.add_argument("url", help="视频链接（支持短链接和完整链接）")
    
    # status 命令 - 检查状态
    status_parser = subparsers.add_parser("status", help="检查配置状态")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "info":
        result = get_video_info(args.url)
    elif args.command == "status":
        result = check_status()
    else:
        result = {"error": "Unknown command"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
