# K-pop Romanizer MCP Microservices

## 아키텍처 개요

```
┌─────────────────┐    ┌─────────────────┐
│   MCP Gateway   │────│ Romanize Service│
│   (Nginx)       │    │   (Container)   │
└─────────────────┘    └─────────────────┘
         │
         ├── 향후: TTS Service
         ├── 향후: Database
         └── 향후: Auth Service
```

## 현재 서비스

### 1. MCP Gateway (Nginx)
- **역할**: 모든 MCP 요청의 진입점
- **포트**: 80, 443
- **기능**: 로드 밸런싱, 라우팅, 보안 헤더

### 2. Romanize Service
- **역할**: 한국어 로마자 변환
- **포트**: 8080 (내부)
- **기능**: MCP 도구 제공 (romanize_single, romanize_lyrics)

## 향후 추가 예정 서비스

### TTS Service
```yaml
tts-service:
  build: ./tts-service
  networks:
    - mcp-network
```

### Database Service
```yaml
database:
  image: postgres:13
  environment:
    - POSTGRES_DB=mcp_db
  volumes:
    - postgres_data:/var/lib/postgresql/data
  networks:
    - mcp-network
```

## 배포 방법

```bash
# 배포 실행
./deploy.sh

# 서비스 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f romanize-service
```

## 확장 방법

1. **새 서비스 추가**:
   - `docker-compose.yml`에 새 서비스 정의
   - `nginx.conf`에 라우팅 규칙 추가

2. **서비스 간 통신**:
   - 동일한 `mcp-network` 사용
   - 서비스명으로 통신 (예: `http://romanize-service:8080`)

3. **무중단 배포**:
   - `docker-compose up -d --no-deps <service-name>`
   - 롤링 업데이트 지원
