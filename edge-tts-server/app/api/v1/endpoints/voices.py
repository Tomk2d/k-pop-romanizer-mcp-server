"""음성 목록 엔드포인트"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_tts_service
from app.core.logging import get_logger
from app.models.schemas import VoicesResponse
from app.services.tts_service import TTSService

router = APIRouter()
logger = get_logger(__name__)


@router.get("/voices", response_model=VoicesResponse)
async def get_voices(
    tts_service: TTSService = Depends(get_tts_service)
) -> VoicesResponse:
    """
    사용 가능한 음성 목록을 조회합니다.
    
    Args:
        tts_service: TTS 서비스 의존성
        
    Returns:
        VoicesResponse: 음성 목록 응답
    """
    try:
        logger.info("음성 목록 조회 요청")
        
        voices = await tts_service.get_available_voices()
        
        logger.info(
            "음성 목록 조회 완료",
            total_voices=len(voices)
        )
        
        return VoicesResponse(
            voices=voices,
            total=len(voices)
        )
        
    except Exception as e:
        logger.error(
            "음성 목록 조회 중 오류 발생",
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="음성 목록을 가져오는 중 오류가 발생했습니다."
        )


@router.get("/voices/{voice_name}/validate")
async def validate_voice(
    voice_name: str,
    tts_service: TTSService = Depends(get_tts_service)
) -> dict:
    """
    특정 음성이 유효한지 확인합니다.
    
    Args:
        voice_name: 확인할 음성 이름
        tts_service: TTS 서비스 의존성
        
    Returns:
        dict: 음성 유효성 검사 결과
    """
    try:
        logger.info(
            "음성 유효성 검사 요청",
            voice_name=voice_name
        )
        
        is_valid = await tts_service.validate_voice(voice_name)
        
        logger.info(
            "음성 유효성 검사 완료",
            voice_name=voice_name,
            is_valid=is_valid
        )
        
        return {
            "voice": voice_name,
            "valid": is_valid
        }
        
    except Exception as e:
        logger.error(
            "음성 유효성 검사 중 오류 발생",
            error=str(e),
            voice_name=voice_name
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="음성 유효성 검사 중 오류가 발생했습니다."
        )
