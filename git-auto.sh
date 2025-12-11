#!/bin/bash

cd /var/lib/ApiGateway/source_code/python || exit 1

# Tạo timestamp đẹp
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
COMMIT_MSG="auto commit at $TIMESTAMP"

# Kiểm tra xem có thay đổi hay không (staged + unstaged + untracked)
if git diff --quiet && git diff --cached --quiet; then
    echo "Không có thay đổi nào. Không commit, không push."
    exit 0
fi

# Stage mọi thay đổi
git add .

# Commit
git commit -m "$COMMIT_MSG"

# Lấy branch hiện tại
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

git pull

# Push
git push origin "$CURRENT_BRANCH" --force

echo "Đã commit & push với message: $COMMIT_MSG"
