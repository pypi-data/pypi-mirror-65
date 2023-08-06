import getpass
import os

SERVICE_TEMPLATE = """
[Unit]
Description=Raspi-View service
[Service]
Type=simple
User=%s
ExecStart=/bin/sh -c "raspi-view -s"
WorkingDirectory=%s
Restart=always
[Install]
WantedBy=multi-user.target
"""

NAME = 'raspi-view'
SERVICE_NAME = NAME + '.service'

def get_stats_service():
    return SERVICE_TEMPLATE % (getpass.getuser(), os.environ['HOME'])


def install():
    with open(SERVICE_NAME, 'w') as f:
        f.write(get_stats_service())
    os.system("sudo mv ./" + SERVICE_NAME + " /etc/systemd/system/" + SERVICE_NAME)
    os.system("sudo systemctl enable " + NAME)
    os.system("sudo systemctl start " + NAME)

def uninstall():
    print("This feature is comming soon...")
