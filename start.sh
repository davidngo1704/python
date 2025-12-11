#!/bin/bash

SESSION_NAME="fastapi"
APP_PATH="app.main:app"
HOST="0.0.0.0"
PORT="8000"
VENV_PATH="venv/bin/activate"

cd /var/lib/ApiGateway/source_code/python

git pull

alembic upgrade head

echo "Killing old Uvicorn processes..."
pkill -f "uvicorn" 2>/dev/null
sleep 1

tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? != 0 ]; then
    echo "Starting new tmux session: $SESSION_NAME"
    tmux new-session -d -s $SESSION_NAME
else
    echo "Using existing session: $SESSION_NAME"
    # Clear màn hình trong session trước khi chạy lệnh mới
    tmux send-keys -t $SESSION_NAME C-c
    tmux send-keys -t $SESSION_NAME "clear" C-m
fi

# Activate venv
tmux send-keys -t $SESSION_NAME "source $VENV_PATH" C-m

# Chạy Uvicorn
tmux send-keys -t $SESSION_NAME "uvicorn $APP_PATH --host $HOST --port $PORT --reload" C-m

echo "FastAPI restarted in tmux session: $SESSION_NAME"
echo "Attach with: tmux attach -t $SESSION_NAME"
