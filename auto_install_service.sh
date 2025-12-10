#!/bin/bash

SERVICE_NAME="fastapi"
START_SCRIPT="/var/lib/ApiGateway/source_code/python/start.sh"
WORKING_DIR="/var/lib/ApiGateway/source_code/python"

echo "[1] Creating systemd service file..."

cat <<EOF | sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null
[Unit]
Description=FastAPI with tmux auto start
After=network.target

[Service]
Type=forking
User=root
WorkingDirectory=$WORKING_DIR
ExecStart=$START_SCRIPT
Restart=always
RestartSec=5
Environment=TERM=xterm-256color

[Install]
WantedBy=multi-user.target
EOF

echo "[2] Setting permissions..."
sudo chmod +x $START_SCRIPT

echo "[3] Reloading systemd..."
sudo systemctl daemon-reload

echo "[4] Enabling service to start on boot..."
sudo systemctl enable $SERVICE_NAME.service

echo "[5] Starting service..."
sudo systemctl start $SERVICE_NAME.service

echo "-------------------------------------------"
echo "DONE! Service '$SERVICE_NAME' is installed."
echo "It will now auto-start on reboot."
echo "Check status with: sudo systemctl status $SERVICE_NAME"
echo "-------------------------------------------"
