"""TTS 서비스 비즈니스 로직"""

import asyncio
from typing import AsyncGenerator, Dict, List, Optional

import edge_tts
from app.core.config import settings
from app.core.logging import get_logger
from app.models.schemas import VoiceInfo

logger = get_logger(__name__)


class TTSService:
    """TTS 서비스 클래스"""
    
    def __init__(self):
        self.logger = logger
    
    async def synthesize_text(
        self,
        text: str,
        voice: str,
        rate: str = "0%",
        volume: str = "0%",
        pitch: str = "0Hz"
    ) -> AsyncGenerator[bytes, None]:
        """
        텍스트를 음성으로 변환합니다.
        
        Args:
            text: 변환할 텍스트
            voice: 음성 선택
            rate: 말하기 속도
            volume: 볼륨
            pitch: 음높이
            
        Yields:
            bytes: 오디오 데이터 청크
        """
        try:
            # 텍스트 전처리: 줄바꿈을 자연스러운 휴지로 변환
            processed_text = self._preprocess_text(text)
            
            self.logger.info(
                "TTS 요청 시작",
                original_length=len(text),
                processed_length=len(processed_text),
                voice=voice,
                rate=rate,
                volume=volume,
                pitch=pitch
            )
            
            # edge-tts로 음성 생성
            communicate = edge_tts.Communicate(
                text=processed_text,
                voice=voice,
                rate=rate,
                volume=volume,
                pitch=pitch
            )
            
            # 스트리밍으로 오디오 데이터 전송
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    self.logger.debug(
                        "오디오 청크 전송",
                        chunk_size=len(chunk["data"])
                    )
                    yield chunk["data"]
            
            self.logger.info("TTS 요청 완료")
            
        except Exception as e:
            self.logger.error(
                "TTS 변환 중 오류 발생",
                error=str(e),
                text_length=len(text),
                voice=voice
            )
            raise
    
    def _preprocess_text(self, text: str) -> str:
        """
        TTS를 위한 텍스트 전처리
        
        Args:
            text: 원본 텍스트
            
        Returns:
            str: 전처리된 텍스트
        """
        # 줄바꿈을 적절한 휴지로 변환
        processed = text.strip()
        
        # 연속된 줄바꿈을 더 긴 휴지로 변환
        processed = processed.replace('\n\n\n', ' ... ')  # 3개 이상 연속 줄바꿈
        processed = processed.replace('\n\n', ' .. ')      # 2개 연속 줄바꿈 (문단 구분)
        processed = processed.replace('\n', ' . ')         # 단일 줄바꿈 (줄 구분)
        
        # 기존 마침표와 새로 추가된 마침표 사이 충돌 해결
        import re
        processed = re.sub(r'\.(\s*\.)+', ' .. ', processed)  # 연속 마침표를 2개로 정리
        processed = re.sub(r'\.{3,}', ' ... ', processed)     # 3개 이상 마침표를 3개로
        
        # 불필요한 공백 정리
        processed = re.sub(r'\s+', ' ', processed)
        processed = processed.strip()
        
        return processed
    
    async def get_available_voices(self) -> List[VoiceInfo]:
        """
        사용 가능한 음성 목록을 가져옵니다.
        
        Returns:
            List[VoiceInfo]: 음성 정보 목록
        """
        try:
            self.logger.info("음성 목록 조회 시작")
            
            # edge-tts에서 음성 목록 가져오기 (비동기 함수)
            voices_data = await edge_tts.list_voices()
            
            # VoiceInfo 모델로 변환
            voices = []
            for voice_data in voices_data:
                # VoiceTag에서 데이터 추출
                voice_tag = voice_data.get("VoiceTag", {})
                content_categories = voice_tag.get("ContentCategories", [])
                voice_personalities = voice_tag.get("VoicePersonalities", [])
                
                voice_info = VoiceInfo(
                    name=voice_data["Name"],
                    gender=voice_data["Gender"],
                    locale=voice_data["Locale"],
                    content_categories=content_categories,
                    voice_personalities=voice_personalities
                )
                voices.append(voice_info)
            
            self.logger.info(
                "음성 목록 조회 완료",
                total_voices=len(voices)
            )
            
            return voices
            
        except Exception as e:
            self.logger.error(
                "음성 목록 조회 중 오류 발생",
                error=str(e)
            )
            raise
    
    async def validate_voice(self, voice: str) -> bool:
        """
        음성이 유효한지 확인합니다.
        
        Args:
            voice: 확인할 음성 이름
            
        Returns:
            bool: 유효한 음성인지 여부
        """
        try:
            # 간단한 패턴 검증 (임시)
            # ko-KR-로 시작하는 한국어 음성들
            korean_voices = [
                "ko-KR-SunHiNeural",
                "ko-KR-InJoonNeural", 
                "ko-KR-HyunsuMultilingualNeural",
                "ko-KR-BongJinNeural",
                "ko-KR-GookMinNeural",
                "ko-KR-HyunsuNeural",
                "ko-KR-JiMinNeural",
                "ko-KR-SeoHyeonNeural",
                "ko-KR-SoonBokNeural",
                "ko-KR-YuJinNeural"
            ]
            
            # 기본적인 패턴 검증
            if voice in korean_voices:
                return True
                
            # 일반적인 패턴 검증 (언어-국가-이름Neural 형태)
            import re
            pattern = r'^[a-z]{2}-[A-Z]{2}-[A-Za-z]+Neural$'
            if re.match(pattern, voice):
                return True
                
            return False
            
        except Exception as e:
            self.logger.error(
                "음성 검증 중 오류 발생",
                error=str(e),
                voice=voice
            )
            return False


# 전역 TTS 서비스 인스턴스
tts_service = TTSService()
