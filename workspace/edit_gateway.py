import re

with open('C:/Users/Administrator/.openclaw/gateway.cmd', 'r') as f:
    content = f.read()

# Add the BRAVE_API_KEY before the node command
new_content = content.replace(
    'set "OPENCLAW_SERVICE_VERSION=2026.2.26"',
    'set "OPENCLAW_SERVICE_VERSION=2026.2.26"\nset "BRAVE_API_KEY=BSAP3xm4s10rblwH8cJF8H2wfyKxze8"'
)

with open('C:/Users/Administrator/.openclaw/gateway.cmd', 'w') as f:
    f.write(new_content)

print('OK')
