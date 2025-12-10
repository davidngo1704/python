#!/bin/bash
set -e

echo "=== ULTIMATE UBUNTU CLEANUP BEGIN ==="

#######################
# 1. APT CLEAN DEEP
#######################
echo "=== 1. Dọn APT sâu ==="
apt-get update -y
apt-get autoremove --purge -y
apt-get autoclean -y
apt-get clean -y
rm -rf /var/cache/apt/archives/*
rm -rf /var/lib/apt/lists/*

#######################
# 2. Cleanup old kernels
#######################
echo "=== 2. Xoá kernel cũ (giữ kernel đang chạy) ==="
CURRENT_KERNEL=$(uname -r)
dpkg -l 'linux-image-*' | awk '/^ii/{print $2}' | grep -v "$CURRENT_KERNEL" | while read k; do
    echo "Removing old kernel: $k"
    apt-get purge -y "$k" || true
done

#######################
# 3. System logs
#######################
echo "=== 3. Dọn log hệ thống ==="
find /var/log -type f -name "*.log" -exec truncate -s 0 {} \;
find /var/log -type f -name "*.gz" -delete
journalctl --vacuum-size=80M
journalctl --vacuum-time=5d

#######################
# 4. Crash reports
#######################
echo "=== 4. Xoá crash reports và core dumps ==="
rm -rf /var/crash/*
find / -type f -name "core" -delete 2>/dev/null || true

#######################
# 5. TMP + Cache
#######################
echo "=== 5. Xoá /tmp và cache người dùng ==="
rm -rf /tmp/* /var/tmp/*
rm -rf /home/*/.cache/*
rm -rf /root/.cache/*

#######################
# 6. Browser Cleanup
#######################
echo "=== 6. Dọn cache trình duyệt ==="
rm -rf ~/.cache/google-chrome/*
rm -rf ~/.cache/chromium/*
rm -rf ~/.mozilla/firefox/*.default-release/cache2/*

#######################
# 7. Thumbnail cleanup
#######################
echo "=== 7. Thumbnail cũ ==="
rm -rf ~/.cache/thumbnails/*

#######################
# 8. Snap Cleanup
#######################
echo "=== 8. Snap cleanup ==="
snap set system refresh.retain=2
snap list --all | awk '/disabled/{print $1, $3}' | while read name rev; do
    snap remove "$name" --revision="$rev"
done

#######################
# 9. Docker Cleanup Ultimate
#######################
echo "=== 9. Dọn Docker tận gốc ==="
docker system prune -af --volumes
docker builder prune -af
docker network prune -f
docker volume prune -f
find /var/lib/docker/overlay2 -type f -name "*.tmp" -delete

# Giới hạn log Docker
DAEMON_FILE="/etc/docker/daemon.json"
if [ ! -f "$DAEMON_FILE" ]; then echo "{}" > "$DAEMON_FILE"; fi
tmp=$(mktemp)
jq '. + { "log-driver": "json-file", "log-opts": { "max-size": "10m", "max-file": "3" }}' \
   "$DAEMON_FILE" > "$tmp" && mv "$tmp" "$DAEMON_FILE"
systemctl restart docker

#######################
# 10. orphan libraries (deborphan)
#######################
echo "=== 10. Xoá orphan libs (deborphan) ==="
apt-get install -y deborphan
deborphan | xargs -r apt-get -y purge

#######################
# 11. Fix broken symlinks
#######################
echo "=== 11. Xoá symbolic link bị hỏng ==="
find / -xtype l -delete 2>/dev/null || true

#######################
# 12. orphan users/groups
#######################
echo "=== 12. Tìm user/group không dùng ==="
awk -F: '$3 >= 1000 && $3 < 60000 {print $1}' /etc/passwd > /tmp/system-users.txt
echo "(Không xoá tự động. Tham khảo file /tmp/system-users.txt)"

#######################
# 13. LVM snapshot cleanup (nếu có)
#######################
echo "=== 13. Dọn LVM snapshot ==="
lvscan | grep snapshot | awk '{print $2}' | sed 's/^.//' | sed 's/.$//' | while read lv; do
    echo "Snapshot detected: $lv"
    lvremove -f "$lv" || true
done

#######################
# 14. Huge files scanning
#######################
echo "=== 14. File lớn bất thường (top 20) ==="
find / -type f -size +200M 2>/dev/null | sort | head -n 20

#######################
# 15. Repair permissions (common paths)
#######################
echo "=== 15. Sửa quyền thư mục chính ==="
chmod 755 /usr/local /opt 2>/dev/null || true
chown root:root /usr/local /opt 2>/dev/null || true

#######################
# 16. Final reports
#######################
echo "=== 16. Dung lượng sau cleanup ==="
df -h
echo "--- Top thư mục nặng nhất /var ---"
du -sh /var/* 2>/dev/null | sort -h

echo "=== ULTIMATE CLEANUP DONE ==="
