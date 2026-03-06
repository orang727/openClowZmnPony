# -*- coding: utf-8 -*-
"""
OpenClaw Cookie 配置服务器
启动后访问 http://localhost:5555 即可配置各平台 Cookie
"""
import sys
import io

# Windows 控制台编码修复
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

# 脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 确定 Skills 配置保存路径
# 优先级: 1. OpenClaw 默认路径  2. 脚本父目录  3. 脚本同级目录
def get_skills_path():
    # 尝试 OpenClaw 默认路径
    default_path = os.path.expanduser('~/.openclaw/workspace/skills')
    if os.path.exists(default_path):
        return default_path
    
    # 尝试脚本父目录（如果有其他 skill 目录）
    parent_dir = os.path.dirname(SCRIPT_DIR)
    if os.path.exists(os.path.join(parent_dir, 'bilibili')) or os.path.exists(os.path.join(parent_dir, 'zhihu')):
        return parent_dir
    
    # 使用脚本同级目录
    return SCRIPT_DIR

SKILLS_PATH = get_skills_path()

# 确保各平台目录存在
PLATFORMS = ['bilibili', 'xiaohongshu', 'douyin', 'zhihu']
for platform in PLATFORMS:
    platform_dir = os.path.join(SKILLS_PATH, platform)
    try:
        if not os.path.exists(platform_dir):
            os.makedirs(platform_dir)
    except Exception as e:
        print(f'警告: 无法创建目录 {platform_dir}: {e}')


class ConfigHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.directory = SCRIPT_DIR
        super().__init__(*args, **kwargs)
    
    def translate_path(self, path):
        """重写路径转换"""
        path = urlparse(path).path
        if path == '/':
            path = '/index.html'
        # 处理 Windows 路径
        path = path.replace('/', os.sep)
        return os.path.join(self.directory, path.lstrip(os.sep))
    
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == '/api/config':
            self.send_config_status()
        else:
            super().do_GET()
    
    def do_POST(self):
        parsed = urlparse(self.path)
        
        if parsed.path == '/api/save':
            self.handle_save()
        elif parsed.path == '/api/clear':
            self.handle_clear()
        else:
            self.send_error(404)
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def send_config_status(self):
        """获取各平台配置状态"""
        status = {}
        
        for platform in PLATFORMS:
            config_path = os.path.join(SKILLS_PATH, platform, 'config.json')
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    has_config = False
                    if platform == 'bilibili':
                        has_config = bool(config.get('SESSDATA'))
                    else:
                        has_config = bool(config.get('cookie'))
                    status[platform] = {
                        'configured': has_config,
                        'config': config if has_config else None
                    }
                except:
                    status[platform] = {'configured': False, 'config': None}
            else:
                status[platform] = {'configured': False, 'config': None}
        
        self.send_json(status)
    
    def handle_save(self):
        """保存配置"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            platform = data.get('platform')
            config = data.get('config')
            
            if not platform or not config:
                self.send_json({'success': False, 'message': '缺少必要参数'}, 400)
                return
            
            # 确保目录存在
            platform_dir = os.path.join(SKILLS_PATH, platform)
            if not os.path.exists(platform_dir):
                os.makedirs(platform_dir)
            
            # 保存配置
            config_path = os.path.join(platform_dir, 'config.json')
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            self.send_json({
                'success': True, 
                'message': f'{platform} 配置已保存',
                'path': config_path
            })
        except json.JSONDecodeError:
            self.send_json({'success': False, 'message': '无效的 JSON 数据'}, 400)
        except PermissionError:
            self.send_json({'success': False, 'message': '权限不足，无法写入文件'}, 500)
        except Exception as e:
            self.send_json({'success': False, 'message': f'保存失败: {str(e)}'}, 500)
    
    def handle_clear(self):
        """清除配置"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            platform = data.get('platform')
            if not platform:
                self.send_json({'success': False, 'message': '缺少平台参数'}, 400)
                return
            
            config_path = os.path.join(SKILLS_PATH, platform, 'config.json')
            
            if os.path.exists(config_path):
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump({}, f)
            
            self.send_json({
                'success': True,
                'message': f'{platform} 配置已清除'
            })
        except Exception as e:
            self.send_json({'success': False, 'message': str(e)}, 500)
    
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}")


def main():
    port = 5555
    
    print('=' * 50)
    print('  OpenClaw Cookie 配置服务器')
    print('=' * 50)
    print(f'  配置目录: {SKILLS_PATH}')
    print('')
    
    # 检查端口是否被占用
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('', port))
        sock.close()
    except OSError:
        print(f'  错误: 端口 {port} 已被占用!')
        print(f'  请关闭占用该端口的程序后重试')
        print('=' * 50)
        input('按回车键退出...')
        return
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, ConfigHandler)
    
    print(f'  访问地址: http://localhost:{port}')
    print('  按 Ctrl+C 停止服务器')
    print('=' * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n服务器已停止')
        httpd.server_close()


if __name__ == '__main__':
    main()
