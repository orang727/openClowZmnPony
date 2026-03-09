#!/usr/bin/env python3
"""简单的 HTTP 服务器来显示任务看板"""
import http.server
import socketserver
import os

PORT = 18888
DIRECTORY = os.path.expanduser("~/.openclaw/workspace")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

print(f"🎯 任务看板服务器启动中...")
print(f"📍 访问地址: http://127.0.0.1:{PORT}/dashboard.html")
print(f"📁 文件目录: {DIRECTORY}")
print(f"\n按 Ctrl+C 停止服务器")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
