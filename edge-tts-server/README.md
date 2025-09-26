# Edge TTS Server

Microsoft Edge TTS 서비스를 활용한 FastAPI 기반 텍스트-음성 변환 서버입니다.

## 🚀 주요 기능

- 텍스트를 음성으로 변환 (TTS)
- 다양한 언어 및 음성 지원
- 스트리밍 오디오 응답
- RESTful API 제공
- Docker 컨테이너화
- 확장 가능한 아키텍처

## 📁 프로젝트 구조

```
edge-tts/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 애플리케이션 진입점
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # 설정 관리
│   │   └── logging.py       # 로깅 설정
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # 의존성 주입
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py       # API 라우터 통합
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── tts.py   # TTS 엔드포인트
│   │           └── voices.py # 음성 목록 엔드포인트
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic 모델
│   ├── services/
│   │   ├── __init__.py
│   │   └── tts_service.py   # TTS 비즈니스 로직
│   └── utils/
│       ├── __init__.py
│       └── helpers.py       # 유틸리티 함수
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── docker/
│   └── Dockerfile
├── docker-compose.yml
├── docker-compose.dev.yml
├── requirements.txt
├── pyproject.toml
├── env.example
├── .gitignore
└── README.md
```

## 🛠️ 설치 및 실행

### Docker Compose 사용 (추천)

```bash
# 환경 변수 설정
cp env.example .env

# 프로덕션 환경으로 실행
docker-compose up -d

# 개발 환경으로 실행 (코드 변경사항 실시간 반영)
docker-compose -f docker-compose.dev.yml up -d

# 로그 확인
docker-compose logs -f

# 서비스 중지
docker-compose down
```

### 로컬 개발

```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp env.example .env

# 서버 실행
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📚 API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔧 API 엔드포인트

### TTS 변환
```http
POST /api/v1/tts/synthesize
Content-Type: application/json

{
    "text": "안녕하세요, 세계!",
    "voice": "ko-KR-SunHiNeural",
    "rate": "0%",
    "volume": "0%",
    "pitch": "0Hz"
}
```

### 음성 목록 조회
```http
GET /api/v1/voices/voices
```

### 음성 유효성 검사
```http
GET /api/v1/voices/voices/{voice_name}/validate
```

### 헬스 체크
```http
GET /health
```

## 🔧 환경 변수

`.env` 파일에서 다음 변수들을 설정할 수 있습니다:

```env
# 서버 설정
HOST=0.0.0.0
PORT=8000
DEBUG=false

# 로깅 설정
LOG_LEVEL=INFO
LOG_FORMAT=json

# CORS 설정
ALLOWED_ORIGINS=["chrome-extension://*", "http://localhost:3000"]

# TTS 설정
DEFAULT_VOICE=ko-KR-SunHiNeural
MAX_TEXT_LENGTH=5000
```

## 🧪 테스트

```bash
# 전체 테스트 실행
pytest

# 특정 테스트 실행
pytest tests/test_api.py

# 커버리지 포함 테스트
pytest --cov=app tests/
```

## 📦 배포

### Docker 이미지 빌드

```bash
docker build -f docker/Dockerfile -t edge-tts-server:latest .
```

### Docker Compose 배포

```bash
# 프로덕션 환경
docker-compose up -d

# 개발 환경
docker-compose -f docker-compose.dev.yml up -d
```

## 🌐 Chrome Extension 연동

Chrome Extension에서 이 서버를 사용하는 예시:

```javascript
// TTS 요청
async function synthesizeText(text, voice = 'ko-KR-SunHiNeural') {
    try {
        const response = await fetch('http://localhost:8000/api/v1/tts/synthesize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text,
                voice,
                rate: '0%',
                volume: '0%',
                pitch: '0Hz'
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // 오디오 재생
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
        
    } catch (error) {
        console.error('TTS 오류:', error);
    }
}

// 사용 예시
synthesizeText('안녕하세요, Chrome Extension입니다!');
```

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 🔗 관련 링크

- [Microsoft Edge TTS](https://github.com/rany2/edge-tts)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://www.docker.com/)
