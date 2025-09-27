"""스트리밍 TTS 엔드포인트"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from app.api.deps import get_tts_service
from app.core.logging import get_logger
from app.models.schemas import TTSRequest
from app.services.tts_service import TTSService

router = APIRouter()
logger = get_logger(__name__)


@router.get("/stream")
async def stream_tts_get(
    text: str,
    voice: str = "ko-KR-SunHiNeural",
    rate: str = "+0%", 
    volume: str = "+0%",
    pitch: str = "+0Hz",
    tts_service: TTSService = Depends(get_tts_service)
) -> StreamingResponse:
    """
    GET 방식으로 텍스트를 음성으로 변환하여 실시간 스트리밍합니다.
    
    브라우저 주소창에서 직접 접근 가능합니다.
    
    Args:
        text: 변환할 텍스트
        voice: 음성 선택
        rate: 말하기 속도 
        volume: 볼륨
        pitch: 음높이
        tts_service: TTS 서비스 의존성
        
    Returns:
        StreamingResponse: 실시간 오디오 스트림 응답
    """
    try:
        logger.info(
            "GET 스트리밍 TTS 요청 수신",
            text_length=len(text),
            voice=voice
        )
        
        # 텍스트 길이 검사
        if len(text) > 5000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="텍스트가 너무 깁니다. 최대 5000자까지 지원됩니다."
            )
        
        # TTS 변환 실행
        audio_generator = tts_service.synthesize_text(
            text=text,
            voice=voice,
            rate=rate,
            volume=volume,
            pitch=pitch
        )
        
        return StreamingResponse(
            audio_generator,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "inline; filename=audio.mp3",
                "Cache-Control": "no-cache",
                "X-Voice": voice,
                "X-Text-Length": str(len(text)),
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "GET 스트리밍 TTS 변환 중 예상치 못한 오류 발생",
            error=str(e),
            text_preview=text[:50] + "..." if len(text) > 50 else text
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="TTS 변환 중 오류가 발생했습니다."
        )

@router.post("/stream") 
async def stream_tts(
    request: TTSRequest,
    tts_service: TTSService = Depends(get_tts_service)
) -> StreamingResponse:
    """
    텍스트를 음성으로 변환하여 실시간 스트리밍합니다.
    
    브라우저에서 바로 재생할 수 있도록 스트리밍 응답을 제공합니다.
    
    Args:
        request: TTS 요청 데이터
        tts_service: TTS 서비스 의존성
        
    Returns:
        StreamingResponse: 실시간 오디오 스트림 응답
    """
    try:
        logger.info(
            "스트리밍 TTS 요청 수신",
            text_length=len(request.text),
            voice=request.voice
        )
        
        # 텍스트 길이 검사
        if len(request.text) > 5000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="텍스트가 너무 깁니다. 최대 5000자까지 지원됩니다."
            )
        
        # TTS 변환 실행
        audio_generator = tts_service.synthesize_text(
            text=request.text,
            voice=request.voice,
            rate=request.rate,
            volume=request.volume,
            pitch=request.pitch
        )
        
        return StreamingResponse(
            audio_generator,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "inline; filename=audio.mp3",
                "Cache-Control": "no-cache",
                "X-Voice": request.voice,
                "X-Text-Length": str(len(request.text)),
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "스트리밍 TTS 변환 중 예상치 못한 오류 발생",
            error=str(e),
            text_length=len(request.text),
            voice=request.voice
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="스트리밍 TTS 변환 중 오류가 발생했습니다."
        )
