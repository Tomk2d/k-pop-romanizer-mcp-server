#!/bin/bash

# HTTPS 설정 스크립트
echo "🔒 HTTPS 설정을 시작합니다..."

# 1. 시스템 업데이트
echo "📦 시스템 업데이트 중..."
sudo apt update

# 2. Nginx 설치
echo "🌐 Nginx 설치 중..."
sudo apt install -y nginx

# 3. Certbot 설치
echo "🔐 Certbot 설치 중..."
sudo apt install -y certbot python3-certbot-nginx

# 4. Nginx 시작
echo "🚀 Nginx 시작 중..."
sudo systemctl start nginx
sudo systemctl enable nginx

# 5. 방화벽 설정
echo "🔥 방화벽 설정 중..."
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw --force enable

# 6. SSL 인증서 발급
echo "📜 SSL 인증서 발급 중..."
sudo certbot --nginx -d kpop-romanizer.duckdns.org --non-interactive --agree-tos --email admin@kpop-romanizer.duckdns.org

# 7. 자동 갱신 설정
echo "🔄 자동 갱신 설정 중..."
sudo crontab -l | { cat; echo "0 12 * * * /usr/bin/certbot renew --quiet"; } | sudo crontab -

# 8. Docker Compose 재시작
echo "🐳 Docker Compose 재시작 중..."
docker-compose down
docker-compose up -d

echo "✅ HTTPS 설정이 완료되었습니다!"
echo "🌐 HTTPS URL: https://kpop-romanizer.duckdns.org/mcp"
echo "🔗 PlayMCP 등록 URL: https://kpop-romanizer.duckdns.org/mcp"
