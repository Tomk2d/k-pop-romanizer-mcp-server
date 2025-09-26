#!/bin/bash

# AWS EC2 마이크로서비스 배포 스크립트
set -e

echo "🚀 K-pop Romanizer MCP Microservices 배포 시작..."

# Docker 및 Docker Compose 설치 확인
if ! command -v docker &> /dev/null; then
    echo "❌ Docker가 설치되지 않았습니다."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose가 설치되지 않았습니다."
    exit 1
fi

# 기존 컨테이너 정리
echo "🧹 기존 컨테이너 정리 중..."
docker-compose down --remove-orphans

# 이미지 빌드
echo "🔨 마이크로서비스 이미지 빌드 중..."
docker-compose build --no-cache

# 서비스 시작
echo "🚀 마이크로서비스 시작 중..."
docker-compose up -d

# 헬스 체크
echo "🏥 헬스 체크 중..."
sleep 15

# MCP Gateway 헬스 체크
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ MCP Gateway가 성공적으로 시작되었습니다!"
else
    echo "❌ MCP Gateway 시작에 실패했습니다."
    docker-compose logs mcp-gateway
    exit 1
fi

# Romanize Service 헬스 체크
if curl -f http://localhost/mcp/health > /dev/null 2>&1; then
    echo "✅ Romanize Service가 성공적으로 시작되었습니다!"
else
    echo "❌ Romanize Service 시작에 실패했습니다."
    docker-compose logs romanize-service
    exit 1
fi

echo "🎉 마이크로서비스 배포 완료!"
echo "🌐 MCP Gateway URL: http://$(curl -s ifconfig.me)"
echo "📋 사용 가능한 엔드포인트:"
echo "   - GET  /health (Gateway Health)"
echo "   - GET  /mcp/health (Romanize Service Health)"
echo "   - GET  /mcp/tools (MCP Tools List)"
echo "   - POST /mcp/jsonrpc (MCP JSON-RPC)"

# 서비스 상태 확인
echo "📊 실행 중인 서비스:"
docker-compose ps