"""API 의존성 주입"""

from typing import Generator

from fastapi import Depends, HTTPException, status
from app.services.tts_service import TTSService, tts_service


def get_tts_service() -> Generator[TTSService, None, None]:
    """
    TTS 서비스 의존성을 제공합니다.
    
    Yields:
        TTSService: TTS 서비스 인스턴스
    """
    try:
        yield tts_service
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"TTS 서비스 초기화 실패: {str(e)}"
        )
