"""애플리케이션 설정 관리"""

from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # 서버 설정
    host: str = Field(default="0.0.0.0", description="서버 호스트")
    port: int = Field(default=8000, description="서버 포트")
    debug: bool = Field(default=False, description="디버그 모드")
    
    # 로깅 설정
    log_level: str = Field(default="INFO", description="로그 레벨")
    log_format: str = Field(default="json", description="로그 포맷 (json/text)")
    
    # CORS 설정
    allowed_origins: List[str] = Field(
        default=["chrome-extension://*", "http://localhost:3000"],
        description="허용된 오리진 목록"
    )
    
    # TTS 설정
    default_voice: str = Field(
        default="ko-KR-SunHiNeural",
        description="기본 음성"
    )
    max_text_length: int = Field(
        default=5000,
        description="최대 텍스트 길이"
    )
    
    # API 설정
    api_v1_prefix: str = Field(default="/api/v1", description="API v1 프리픽스")
    title: str = Field(default="Edge TTS Server", description="API 제목")
    description: str = Field(
        default="Microsoft Edge TTS 서비스를 활용한 텍스트-음성 변환 서버",
        description="API 설명"
    )
    version: str = Field(default="1.0.0", description="API 버전")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# 전역 설정 인스턴스
settings = Settings()
