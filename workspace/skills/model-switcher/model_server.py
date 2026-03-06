# -*- coding: utf-8 -*-
"""
OpenClaw 模型切换服务器
启动后访问 http://localhost:5566 即可切换模型
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import json
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

OPENCLAW_CONFIG = os.path.expanduser('~/.openclaw/openclaw.json')

class ModelSwitcherHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.directory = os.path.dirname(os.path.abspath(__file__))
        super().__init__(*args, **kwargs)
    
    def translate_path(self, path):
        path = urlparse(path).path
        if path == '/':
            path = '/index.html'
        return os.path.join(self.directory, path.lstrip('/'))
    
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == '/api/config':
            self.handle_get_config()
        elif parsed.path == '/api/gateway-status':
            self.handle_gateway_status()
        else:
            super().do_GET()
    
    def do_POST(self):
        parsed = urlparse(self.path)
        
        if parsed.path == '/api/set-model':
            self.handle_set_model()
        elif parsed.path == '/api/set-agent-model':
            self.handle_set_agent_model()
        elif parsed.path == '/api/restart-gateway':
            self.handle_restart_gateway()
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
    
    def read_config(self):
        """读取 OpenClaw 配置"""
        try:
            with open(OPENCLAW_CONFIG, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            return None
    
    def write_config(self, config):
        """写入 OpenClaw 配置"""
        # 先备份
        backup_path = OPENCLAW_CONFIG + '.bak'
        try:
            with open(OPENCLAW_CONFIG, 'r', encoding='utf-8') as f:
                backup_content = f.read()
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(backup_content)
        except:
            pass
        
        # 写入新配置
        with open(OPENCLAW_CONFIG, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def handle_get_config(self):
        """获取配置信息"""
        config = self.read_config()
        if not config:
            self.send_json({'success': False, 'message': '无法读取配置文件'}, 500)
            return
        
        # 提取模型列表
        models = []
        providers = config.get('models', {}).get('providers', {})
        for provider_id, provider in providers.items():
            for model in provider.get('models', []):
                models.append({
                    'id': model.get('id'),
                    'name': model.get('name'),
                    'fullId': f"{provider_id}/{model.get('id')}",
                    'reasoning': model.get('reasoning', False),
                    'contextWindow': model.get('contextWindow', 0),
                    'maxTokens': model.get('maxTokens', 0)
                })
        
        current_model = config.get('agents', {}).get('defaults', {}).get('model', {}).get('primary', '')
        
        self.send_json({
            'success': True,
            'config': config,
            'models': models,
            'currentModel': current_model
        })
    
    def handle_gateway_status(self):
        """检查网关状态"""
        try:
            # 尝试检查进程
            if os.name == 'nt':
                result = subprocess.run(
                    ['tasklist', '/FI', 'IMAGENAME eq node.exe'],
                    capture_output=True, text=True, timeout=5
                )
                running = 'node.exe' in result.stdout
            else:
                result = subprocess.run(
                    ['pgrep', '-f', 'openclaw'],
                    capture_output=True, timeout=5
                )
                running = result.returncode == 0
            
            self.send_json({'running': running})
        except:
            self.send_json({'running': False})
    
    def handle_set_model(self):
        """设置默认模型"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body)
            model = data.get('model')
            
            if not model:
                self.send_json({'success': False, 'message': '未指定模型'}, 400)
                return
            
            config = self.read_config()
            if not config:
                self.send_json({'success': False, 'message': '无法读取配置'}, 500)
                return
            
            # 更新默认模型
            if 'agents' not in config:
                config['agents'] = {}
            if 'defaults' not in config['agents']:
                config['agents']['defaults'] = {}
            if 'model' not in config['agents']['defaults']:
                config['agents']['defaults']['model'] = {}
            
            config['agents']['defaults']['model']['primary'] = model
            
            self.write_config(config)
            
            self.send_json({
                'success': True,
                'message': f'默认模型已切换为 {model}'
            })
        except json.JSONDecodeError:
            self.send_json({'success': False, 'message': '无效的 JSON'}, 400)
        except Exception as e:
            self.send_json({'success': False, 'message': str(e)}, 500)
    
    def handle_set_agent_model(self):
        """设置智能体模型"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body)
            agent_id = data.get('agentId')
            model = data.get('model')
            
            if not agent_id or not model:
                self.send_json({'success': False, 'message': '参数不完整'}, 400)
                return
            
            config = self.read_config()
            if not config:
                self.send_json({'success': False, 'message': '无法读取配置'}, 500)
                return
            
            # 找到对应智能体并更新
            agents = config.get('agents', {}).get('list', [])
            found = False
            for agent in agents:
                if agent.get('id') == agent_id:
                    agent['model'] = model
                    found = True
                    break
            
            if not found:
                self.send_json({'success': False, 'message': f'未找到智能体 {agent_id}'}, 404)
                return
            
            self.write_config(config)
            
            self.send_json({
                'success': True,
                'message': f'{agent_id} 模型已更新为 {model}'
            })
        except Exception as e:
            self.send_json({'success': False, 'message': str(e)}, 500)
    
    def handle_restart_gateway(self):
        """重启网关"""
        try:
            # 异步执行重启命令
            if os.name == 'nt':
                subprocess.Popen(
                    ['cmd', '/c', 'openclaw', 'gateway', 'restart'],
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:
                subprocess.Popen(
                    ['openclaw', 'gateway', 'restart'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            self.send_json({
                'success': True,
                'message': '网关重启命令已发送'
            })
        except Exception as e:
            self.send_json({'success': False, 'message': str(e)}, 500)
    
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}")


def main():
    port = 5566
    server_address = ('', port)
    httpd = HTTPServer(server_address, ModelSwitcherHandler)
    
    print('=' * 50)
    print('  OpenClaw 模型切换服务器')
    print('=' * 50)
    print(f'  访问地址: http://localhost:{port}')
    print(f'  配置文件: {OPENCLAW_CONFIG}')
    print('  按 Ctrl+C 停止服务器')
    print('=' * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n服务器已停止')
        httpd.server_close()


if __name__ == '__main__':
    main()
