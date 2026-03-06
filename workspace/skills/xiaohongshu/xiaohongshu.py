#!/usr/bin/env python3
"""
小红书内容搜索工具
用于获取推荐笔记、笔记详情等
"""

import argparse
import json
import os
import re
import sys
import io

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests

# 配置文件路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://www.xiaohongshu.com/',
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


def extract_initial_state(html: str) -> dict | None:
    """从 HTML 中提取 __INITIAL_STATE__ 数据"""
    pattern = r'window\.__INITIAL_STATE__\s*=\s*({.+?})\s*</script>'
    match = re.search(pattern, html, re.DOTALL)
    if match:
        try:
            json_str = match.group(1)
            json_str = re.sub(r':undefined', ':null', json_str)
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
    return None


def get_recommend_notes(count: int = 20) -> dict:
    """获取首页推荐笔记"""
    try:
        url = 'https://www.xiaohongshu.com/'
        resp = requests.get(url, headers=get_headers(), timeout=15)
        
        if resp.status_code != 200:
            return {"success": False, "error": f"HTTP {resp.status_code}"}
        
        data = extract_initial_state(resp.text)
        if not data:
            return {"success": False, "error": "无法解析页面数据"}
        
        feeds = data.get("feed", {}).get("feeds", [])
        
        notes = []
        for item in feeds[:count]:
            note_card = item.get("noteCard", {})
            user = note_card.get("user", {})
            interact_info = note_card.get("interactInfo", {})
            cover = note_card.get("cover", {})
            
            notes.append({
                "note_id": item.get("id"),
                "title": note_card.get("displayTitle"),
                "type": note_card.get("type"),
                "cover": cover.get("urlDefault") or cover.get("url"),
                "user": {
                    "user_id": user.get("userId"),
                    "nickname": user.get("nickname") or user.get("nickName"),
                    "avatar": user.get("avatar"),
                },
                "liked_count": interact_info.get("likedCount"),
                "url": f"https://www.xiaohongshu.com/explore/{item.get('id')}",
            })
        
        return {
            "success": True,
            "data": {
                "type": "recommend",
                "count": len(notes),
                "notes": notes
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def search_notes(keyword: str, count: int = 10) -> dict:
    """搜索笔记 - 返回推荐内容（小红书搜索API受限）"""
    # 由于小红书搜索 API 限制，返回首页推荐内容
    result = get_recommend_notes(count)
    if result.get("success"):
        result["data"]["keyword"] = keyword
        result["data"]["notice"] = "小红书搜索API受限，返回首页推荐内容"
    return result


def get_note_detail(note_id: str) -> dict:
    """获取笔记详情 - 功能受限"""
    return {
        "success": False,
        "error": "小红书笔记详情API受限，无法直接获取。请使用 recommend 命令获取推荐内容，或在浏览器中访问笔记链接。",
        "url": f"https://www.xiaohongshu.com/explore/{note_id}"
    }


def check_status() -> dict:
    """检查配置状态"""
    cookie = load_cookie()
    if cookie:
        try:
            resp = requests.get('https://www.xiaohongshu.com/', headers=get_headers(), timeout=10)
            return {
                "success": True,
                "configured": True,
                "status": f"HTTP {resp.status_code}",
                "message": "Cookie 已配置，可获取推荐内容"
            }
        except Exception as e:
            return {"success": True, "configured": True, "error": str(e)}
    return {"success": True, "configured": False, "message": "未配置 Cookie"}


def main():
    parser = argparse.ArgumentParser(description="小红书内容获取工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # recommend 命令 - 获取推荐内容
    rec_parser = subparsers.add_parser("recommend", help="获取首页推荐笔记")
    rec_parser.add_argument("--count", type=int, default=10, help="返回数量")
    
    # search 命令 - 搜索（受限）
    search_parser = subparsers.add_parser("search", help="搜索笔记（受限，返回推荐内容）")
    search_parser.add_argument("keyword", help="搜索关键词")
    search_parser.add_argument("--count", type=int, default=10, help="返回数量")
    
    # detail 命令 - 笔记详情（受限）
    detail_parser = subparsers.add_parser("detail", help="获取笔记详情（受限）")
    detail_parser.add_argument("note_id", help="笔记ID或链接")
    
    # status 命令
    status_parser = subparsers.add_parser("status", help="检查配置状态")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "recommend":
        result = get_recommend_notes(args.count)
    elif args.command == "search":
        result = search_notes(args.keyword, args.count)
    elif args.command == "detail":
        note_id = args.note_id
        if 'xiaohongshu.com' in note_id:
            match = re.search(r'/explore/([a-f0-9]+)', note_id)
            if match:
                note_id = match.group(1)
        result = get_note_detail(note_id)
    elif args.command == "status":
        result = check_status()
    else:
        result = {"error": "Unknown command"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
