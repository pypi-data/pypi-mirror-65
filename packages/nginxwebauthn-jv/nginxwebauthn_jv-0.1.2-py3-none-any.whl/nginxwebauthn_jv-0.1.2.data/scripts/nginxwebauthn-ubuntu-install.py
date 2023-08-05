#!python

import os
import sys
from pathlib import Path

print("creating directroy structure")
Path("/opt/nginxwebauthn/credentials").mkdir(parents=True, exist_ok=True)
Path("/opt/nginxwebauthn/headers").mkdir(parents=True, exist_ok=True)

script_path = os.path.realpath(__file__).replace("/nginxwebauthn-ubuntu-install.py", "/nginxwebauthn.py")

systemd_contents = """
[Unit]
Description=Python NGINX Webauthn

[Service]
Type=simple
User=%s
Group=%s
ExecStart="%s"
StandardOutput=/var/log/nginxwebauthn.log
StandardError=/var/log/nginxwebauthn.err.log
Restart=always

[Install]
WantedBy=multi-user.target
"""

print("creating systemd service file")
with open('/lib/systemd/system/nginxwebauthn.service', 'w') as f:
    f.write(systemd_contents % (sys.argv[1], sys.argv[2], script_path))

print("running systemctl commands")
os.system("systemctl daemon-reload")
os.system("systemctl enable nginxwebauthn.service")
os.system("systemctl start nginxwebauthn.service")

