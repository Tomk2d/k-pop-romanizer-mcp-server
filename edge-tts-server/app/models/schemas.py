"""Pydantic 모델 정의"""

from typing import List, Optional
from pydantic import BaseModel, Field, validator


class TTSRequest(BaseModel):
    """TTS 요청 모델"""
    
    text: str = Field(
        ..., 
        description="변환할 텍스트", 
        min_length=1, 
        max_length=5000,
        example="안녕하세요, 테스트입니다"
    )
    voice: str = Field(
        default="ko-KR-SunHiNeural", 
        description="음성 선택",
        example="ko-KR-SunHiNeural"
    )
    rate: str = Field(
        default="0%", 
        description="말하기 속도 (예: 0%, -50%, +50%)",
        example="0%"
    )
    volume: str = Field(
        default="0%", 
        description="볼륨 (예: 0%, -50%, +50%)",
        example="0%"
    )
    pitch: str = Field(
        default="0Hz", 
        description="음높이 (예: 0Hz, -50Hz, +50Hz)",
        example="0Hz"
    )
    
    @validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError('텍스트는 비어있을 수 없습니다')
        return v.strip()
    
    @validator('rate')
    def validate_rate(cls, v):
        if not v.endswith('%'):
            raise ValueError('속도는 %로 끝나야 합니다 (예: 0%, -50%, +50%)')
        # 0%를 +0%로 자동 변환
        if v == '0%':
            return '+0%'
        if not v.startswith(('+', '-')):
            raise ValueError('속도는 + 또는 -로 시작해야 합니다 (예: 0%, -50%, +50%)')
        return v
    
    @validator('volume')
    def validate_volume(cls, v):
        if not v.endswith('%'):
            raise ValueError('볼륨은 %로 끝나야 합니다 (예: 0%, -50%, +50%)')
        # 0%를 +0%로 자동 변환
        if v == '0%':
            return '+0%'
        if not v.startswith(('+', '-')):
            raise ValueError('볼륨은 + 또는 -로 시작해야 합니다 (예: 0%, -50%, +50%)')
        return v
    
    @validator('pitch')
    def validate_pitch(cls, v):
        if not v.endswith('Hz'):
            raise ValueError('음높이는 Hz로 끝나야 합니다 (예: 0Hz, -50Hz, +50Hz)')
        # 0Hz를 +0Hz로 자동 변환
        if v == '0Hz':
            return '+0Hz'
        if not v.startswith(('+', '-')):
            raise ValueError('음높이는 + 또는 -로 시작해야 합니다 (예: 0Hz, -50Hz, +50Hz)')
        return v


class VoiceInfo(BaseModel):
    """음성 정보 모델"""
    
    name: str = Field(..., description="음성 이름")
    gender: str = Field(..., description="성별")
    locale: str = Field(..., description="언어/지역")
    content_categories: List[str] = Field(..., description="콘텐츠 카테고리")
    voice_personalities: List[str] = Field(..., description="음성 성격")


class VoicesResponse(BaseModel):
    """음성 목록 응답 모델"""
    
    voices: List[VoiceInfo] = Field(..., description="사용 가능한 음성 목록")
    total: int = Field(..., description="총 음성 개수")


class HealthResponse(BaseModel):
    """헬스 체크 응답 모델"""
    
    status: str = Field(..., description="서비스 상태")
    service: str = Field(..., description="서비스 이름")
    version: str = Field(..., description="서비스 버전")


class ErrorResponse(BaseModel):
    """에러 응답 모델"""
    
    error: str = Field(..., description="에러 메시지")
    detail: Optional[str] = Field(None, description="상세 에러 정보")
    code: Optional[str] = Field(None, description="에러 코드")
