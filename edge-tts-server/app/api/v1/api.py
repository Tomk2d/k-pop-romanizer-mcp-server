"""API v1 라우터 통합"""

from fastapi import APIRouter

from app.api.v1.endpoints import tts, voices, stream

api_router = APIRouter()

# 엔드포인트 라우터 등록
api_router.include_router(
    tts.router,
    prefix="/tts",
    tags=["TTS - 파일 다운로드"]
)

api_router.include_router(
    stream.router,
    prefix="/tts",
    tags=["TTS - 실시간 스트리밍"]
)

api_router.include_router(
    voices.router,
    prefix="/voices",
    tags=["Voices"]
)
