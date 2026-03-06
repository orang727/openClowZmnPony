#!/usr/bin/env python3
"""
知乎内容获取工具
用于获取知乎热门回答、问题详情等
"""

import argparse
import json
import os
import re
import sys
import io

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from zhihuapi.answer import Answer
    from zhihuapi.question import Question
    HAS_ZHIHUAPI = True
except ImportError:
    HAS_ZHIHUAPI = False

import requests

# 配置文件路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.zhihu.com/',
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


def get_hot_answers(time_type: str = "day", count: int = 10) -> dict:
    """获取热门回答
    
    Args:
        time_type: 时间范围 (day/month)
        count: 返回数量
    """
    if not HAS_ZHIHUAPI:
        return {"success": False, "error": "zhihuapi 未安装，请运行: pip install zhihuapi"}
    
    try:
        if time_type == "month":
            data = Answer.explore_month()
        else:
            data = Answer.explore_day()
        
        answers = []
        for item in (data or [])[:count]:
            question = item.get("question", {})
            author = item.get("author", {})
            
            # 清理 HTML 内容
            content = item.get("content", "")
            content = content.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
            content = content.replace('&quot;', '"').replace('&#39;', "'")
            content = re.sub(r'<[^>]+>', '', content)  # 移除 HTML 标签
            content = re.sub(r'\s+', ' ', content).strip()  # 压缩空白
            content = content[:300] + "..." if len(content) > 300 else content
            
            answers.append({
                "answer_id": item.get("id"),
                "question": {
                    "id": question.get("id"),
                    "title": question.get("title"),
                    "url": f"https://www.zhihu.com/question/{question.get('id')}",
                },
                "author": {
                    "id": author.get("id"),
                    "name": author.get("name"),
                    "avatar": author.get("avatar_url"),
                },
                "voteup_count": item.get("voteup_count"),
                "comment_count": item.get("comment_count"),
                "content_preview": content,
                "created_time": item.get("created_time"),
                "url": f"https://www.zhihu.com/question/{question.get('id')}/answer/{item.get('id')}",
            })
        
        return {
            "success": True,
            "data": {
                "type": f"hot_{time_type}",
                "count": len(answers),
                "answers": answers
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_question_detail(question_id: int) -> dict:
    """获取问题详情"""
    if not HAS_ZHIHUAPI:
        return {"success": False, "error": "zhihuapi 未安装"}
    
    try:
        q = Question(question_id)
        detail = q.detail()
        
        if not detail:
            return {"success": False, "error": "无法获取问题详情"}
        
        return {
            "success": True,
            "data": {
                "question_id": detail.get("id"),
                "title": detail.get("title"),
                "detail": detail.get("detail"),
                "answer_count": detail.get("answer_count"),
                "follower_count": detail.get("follower_count"),
                "visit_count": detail.get("visit_count"),
                "created_time": detail.get("created_time"),
                "updated_time": detail.get("updated_time"),
                "url": f"https://www.zhihu.com/question/{detail.get('id')}",
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_question_answers(question_id: int, count: int = 10, sort: str = "vote") -> dict:
    """获取问题的回答列表"""
    if not HAS_ZHIHUAPI:
        return {"success": False, "error": "zhihuapi 未安装"}
    
    try:
        q = Question(question_id)
        
        if sort == "time":
            data = q.answers_bypage()
        else:
            data = q.answers_byvote()
        
        answers = []
        for item in (data or [])[:count]:
            author = item.get("author", {})
            content = item.get("content", "")
            content = content.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
            content = content.replace('&quot;', '"').replace('&#39;', "'")
            content = re.sub(r'<[^>]+>', '', content)
            content = re.sub(r'\s+', ' ', content).strip()
            content = content[:300] + "..." if len(content) > 300 else content
            
            answers.append({
                "answer_id": item.get("id"),
                "author": {
                    "id": author.get("id"),
                    "name": author.get("name"),
                },
                "voteup_count": item.get("voteup_count"),
                "comment_count": item.get("comment_count"),
                "content_preview": content,
                "created_time": item.get("created_time"),
                "url": f"https://www.zhihu.com/question/{question_id}/answer/{item.get('id')}",
            })
        
        return {
            "success": True,
            "data": {
                "question_id": question_id,
                "sort": sort,
                "count": len(answers),
                "answers": answers
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def search_zhihu(keyword: str, search_type: str = "general", count: int = 10) -> dict:
    """搜索知乎
    
    Args:
        keyword: 搜索关键词
        search_type: 搜索类型 (general/question/answer/article/user)
        count: 返回数量
    """
    cookie = load_cookie()
    if not cookie:
        return {
            "success": False,
            "error": "搜索需要登录，请先配置 Cookie",
            "suggestion": f"你可以访问 https://www.zhihu.com/search?q={keyword} 在浏览器中搜索"
        }
    
    try:
        headers = HEADERS.copy()
        headers['Cookie'] = cookie
        
        # 搜索类型映射
        type_map = {
            "general": "general",
            "question": "content",
            "answer": "content", 
            "article": "content",
            "user": "people",
        }
        t = type_map.get(search_type, "general")
        
        url = f'https://www.zhihu.com/api/v4/search_v3?t={t}&q={keyword}&correction=1&offset=0&limit={count}'
        resp = requests.get(url, headers=headers, timeout=15)
        
        if resp.status_code != 200:
            return {"success": False, "error": f"HTTP {resp.status_code}"}
        
        data = resp.json()
        results = []
        
        for item in data.get("data", [])[:count]:
            obj = item.get("object", {})
            item_type = obj.get("type", "")
            
            # 清理 HTML
            excerpt = obj.get("excerpt", "") or ""
            excerpt = excerpt.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
            excerpt = re.sub(r'<[^>]+>', '', excerpt)
            excerpt = re.sub(r'\s+', ' ', excerpt).strip()
            excerpt = excerpt[:200] + "..." if len(excerpt) > 200 else excerpt
            
            title = obj.get("title", "") or ""
            title = title.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
            title = re.sub(r'<[^>]+>', '', title)
            
            result = {
                "id": obj.get("id"),
                "type": item_type,
                "title": title,
                "excerpt": excerpt,
                "voteup_count": obj.get("voteup_count"),
                "comment_count": obj.get("comment_count"),
                "url": obj.get("url", "").replace("api.zhihu.com", "www.zhihu.com"),
            }
            
            # 添加作者信息（如果有）
            author = obj.get("author", {})
            if author:
                result["author"] = {
                    "id": author.get("id"),
                    "name": author.get("name"),
                }
            
            # 添加问题信息（如果是回答）
            question = obj.get("question", {})
            if question:
                result["question"] = {
                    "id": question.get("id"),
                    "title": question.get("title"),
                }
            
            results.append(result)
        
        return {
            "success": True,
            "data": {
                "keyword": keyword,
                "type": search_type,
                "count": len(results),
                "results": results
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def check_status() -> dict:
    """检查配置状态"""
    status = {
        "success": True,
        "zhihuapi_available": HAS_ZHIHUAPI,
    }
    
    cookie = load_cookie()
    status["cookie_configured"] = cookie is not None
    
    # 测试 API
    if HAS_ZHIHUAPI:
        try:
            data = Answer.explore_day()
            status["api_status"] = f"OK ({len(data or [])} answers)"
        except Exception as e:
            status["api_status"] = f"Error: {str(e)}"
    
    return status


def extract_question_id(url_or_id: str) -> int | None:
    """从 URL 或 ID 字符串中提取问题 ID"""
    # 如果是纯数字
    if url_or_id.isdigit():
        return int(url_or_id)
    
    # 从 URL 提取
    match = re.search(r'question/(\d+)', url_or_id)
    if match:
        return int(match.group(1))
    
    return None


def main():
    parser = argparse.ArgumentParser(description="知乎内容获取工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # hot 命令 - 获取热门回答
    hot_parser = subparsers.add_parser("hot", help="获取热门回答")
    hot_parser.add_argument("--type", choices=["day", "month"], default="day", help="时间范围")
    hot_parser.add_argument("--count", type=int, default=10, help="返回数量")
    
    # question 命令 - 获取问题详情
    question_parser = subparsers.add_parser("question", help="获取问题详情")
    question_parser.add_argument("question_id", help="问题ID或URL")
    
    # answers 命令 - 获取问题的回答
    answers_parser = subparsers.add_parser("answers", help="获取问题的回答列表")
    answers_parser.add_argument("question_id", help="问题ID或URL")
    answers_parser.add_argument("--count", type=int, default=10, help="返回数量")
    answers_parser.add_argument("--sort", choices=["vote", "time"], default="vote", help="排序方式")
    
    # search 命令 - 搜索
    search_parser = subparsers.add_parser("search", help="搜索知乎")
    search_parser.add_argument("keyword", help="搜索关键词")
    search_parser.add_argument("--type", choices=["general", "question", "answer", "article", "user"], default="general", help="搜索类型")
    search_parser.add_argument("--count", type=int, default=10, help="返回数量")
    
    # status 命令 - 检查状态
    status_parser = subparsers.add_parser("status", help="检查配置状态")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "hot":
        result = get_hot_answers(args.type, args.count)
    elif args.command == "question":
        q_id = extract_question_id(args.question_id)
        if q_id:
            result = get_question_detail(q_id)
        else:
            result = {"success": False, "error": "无效的问题ID"}
    elif args.command == "answers":
        q_id = extract_question_id(args.question_id)
        if q_id:
            result = get_question_answers(q_id, args.count, args.sort)
        else:
            result = {"success": False, "error": "无效的问题ID"}
    elif args.command == "search":
        result = search_zhihu(args.keyword, args.type, args.count)
    elif args.command == "status":
        result = check_status()
    else:
        result = {"error": "Unknown command"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
