#!/usr/bin/env python3
"""
国内搜索工具 - 使用百度或Bing进行网络搜索
用于替代在国内网络环境下无法使用的 Brave Search API
"""

import argparse
import json
import re
import sys
from urllib.parse import quote_plus, urljoin

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print(json.dumps({
        "error": "Missing dependencies. Run: pip install requests beautifulsoup4 lxml"
    }))
    sys.exit(1)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


def search_baidu(query: str, count: int = 5) -> list:
    """使用百度搜索"""
    results = []
    url = f"https://www.baidu.com/s?wd={quote_plus(query)}&rn={count}"
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "lxml")
        
        # 百度搜索结果在 class="result" 或 class="c-container" 的 div 中
        for item in soup.select(".result, .c-container"):
            title_elem = item.select_one("h3 a")
            if not title_elem:
                continue
            
            title = title_elem.get_text(strip=True)
            link = title_elem.get("href", "")
            
            # 获取摘要
            snippet_elem = item.select_one(".c-abstract, .c-span-last")
            snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
            
            if title and link:
                results.append({
                    "title": title,
                    "url": link,
                    "snippet": snippet[:200]
                })
            
            if len(results) >= count:
                break
                
    except Exception as e:
        return [{"error": f"Baidu search failed: {str(e)}"}]
    
    return results


def search_bing(query: str, count: int = 5) -> list:
    """使用 Bing 中国搜索"""
    results = []
    url = f"https://cn.bing.com/search?q={quote_plus(query)}&count={count}"
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "lxml")
        
        # Bing 搜索结果
        for item in soup.select(".b_algo"):
            title_elem = item.select_one("h2 a")
            if not title_elem:
                continue
            
            title = title_elem.get_text(strip=True)
            link = title_elem.get("href", "")
            
            # 获取摘要
            snippet_elem = item.select_one(".b_caption p, .b_algoSlug")
            snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
            
            if title and link:
                results.append({
                    "title": title,
                    "url": link,
                    "snippet": snippet[:200]
                })
            
            if len(results) >= count:
                break
                
    except Exception as e:
        return [{"error": f"Bing search failed: {str(e)}"}]
    
    return results


def main():
    parser = argparse.ArgumentParser(description="国内网络搜索工具")
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("--engine", choices=["baidu", "bing"], default="bing",
                        help="搜索引擎 (默认: bing)")
    parser.add_argument("--count", type=int, default=5,
                        help="返回结果数量 (默认: 5)")
    parser.add_argument("--json", action="store_true", default=True,
                        help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    if args.engine == "baidu":
        results = search_baidu(args.query, args.count)
    else:
        results = search_bing(args.query, args.count)
    
    output = {
        "query": args.query,
        "engine": args.engine,
        "count": len(results),
        "results": results
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    # Fix Windows encoding
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()
