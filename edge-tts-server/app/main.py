"""FastAPI 애플리케이션 메인 모듈"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging import configure_logging, get_logger
from app.models.schemas import HealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """애플리케이션 생명주기 관리"""
    # 시작 시 실행
    configure_logging()
    logger = get_logger(__name__)
    logger.info("Edge TTS Server 시작", version=settings.version)
    
    yield
    
    # 종료 시 실행
    logger.info("Edge TTS Server 종료")


# FastAPI 애플리케이션 생성
app = FastAPI(
    title=settings.title,
    description=settings.description,
    version=settings.version,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/", response_model=HealthResponse)
async def root() -> HealthResponse:
    """루트 엔드포인트 - 서비스 상태 확인"""
    return HealthResponse(
        status="healthy",
        service=settings.title,
        version=settings.version
    )


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """헬스 체크 엔드포인트"""
    return HealthResponse(
        status="healthy",
        service=settings.title,
        version=settings.version
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """HTTP 예외 핸들러"""
    logger = get_logger(__name__)
    logger.warning(
        "HTTP 예외 발생",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url.path)
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """일반 예외 핸들러"""
    logger = get_logger(__name__)
    logger.error(
        "예상치 못한 오류 발생",
        error=str(exc),
        path=request.url.path,
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "내부 서버 오류가 발생했습니다.",
            "status_code": 500,
            "path": str(request.url.path)
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
