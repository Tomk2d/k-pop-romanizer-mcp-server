#!/usr/bin/env python3
"""
MCP Gateway - 중앙집중형 MCP 서버
모든 MCP 요청을 받아서 적절한 백엔드 서비스로 라우팅
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import httpx
import asyncio
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MCP Gateway",
    description="중앙집중형 MCP 서버 - 모든 MCP 요청을 백엔드 서비스로 라우팅",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 백엔드 서비스 URL
ROMANIZE_SERVER_URL = "http://romanize-service:8080"
TTS_SERVER_URL = "http://tts-service:8000"  # 컨테이너 내부에서는 8000 포트 사용

# MCP 요청/응답 모델
class McpRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: str
    method: str
    params: Optional[Dict[str, Any]] = None

class McpResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None

# MCP 도구 정의
def get_romanize_tools() -> List[Dict[str, Any]]:
    """로마자 변환 도구 목록"""
    return [
        {
            "name": "romanize_single",
            "description": "한국어 단문을 로마자로 변환합니다. 줄바꿈이 없는 짧은 문장에 적합합니다.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "변환할 한국어 텍스트 (단문)"
                    }
                },
                "required": ["text"]
            }
        },
        {
            "name": "romanize_lyrics",
            "description": "한국어 가사를 로마자로 변환합니다. 줄바꿈이 있는 가사나 긴 텍스트에 적합하며, 한글-영어-줄바꿈 형태로 출력됩니다.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "변환할 한국어 가사 텍스트 (여러 줄 가능)"
                    }
                },
                "required": ["text"]
            }
        }
    ]

def get_tts_tools() -> List[Dict[str, Any]]:
    """TTS 도구 목록"""
    return [
        {
            "name": "tts_synthesize",
            "description": "한국어 텍스트를 음성으로 변환하여 MP3 파일로 다운로드합니다.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "변환할 텍스트"
                    },
                    "voice": {
                        "type": "string",
                        "description": "음성 선택",
                        "default": "ko-KR-SunHiNeural"
                    },
                    "rate": {
                        "type": "string",
                        "description": "말하기 속도",
                        "default": "+0%"
                    },
                    "volume": {
                        "type": "string",
                        "description": "볼륨",
                        "default": "+0%"
                    },
                    "pitch": {
                        "type": "string",
                        "description": "음높이",
                        "default": "+0Hz"
                    }
                },
                "required": ["text"]
            }
        },
        {
            "name": "tts_stream",
            "description": "한국어 텍스트를 음성으로 변환하여 실시간 스트리밍합니다.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "변환할 텍스트"
                    },
                    "voice": {
                        "type": "string",
                        "description": "음성 선택",
                        "default": "ko-KR-SunHiNeural"
                    }
                },
                "required": ["text"]
            }
        }
    ]

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy", "service": "MCP Gateway"}

@app.post("/mcp/jsonrpc")
async def handle_mcp_request(request: McpRequest) -> McpResponse:
    """MCP JSON-RPC 요청 처리"""
    try:
        logger.info(f"MCP 요청 수신: {request.method}")
        
        if request.method == "tools/list":
            # 모든 도구 목록 통합
            all_tools = get_romanize_tools() + get_tts_tools()
            return McpResponse(
                id=request.id,
                result={"tools": all_tools}
            )
        
        elif request.method == "tools/call":
            tool_name = request.params.get("name")
            arguments = request.params.get("arguments", {})
            
            if tool_name.startswith("romanize_"):
                # 로마자 변환 서버로 전달
                return await call_romanize_server(request)
            elif tool_name.startswith("tts_"):
                # TTS 서버로 전달
                return await call_tts_server(request)
            else:
                raise HTTPException(status_code=400, detail=f"알 수 없는 도구: {tool_name}")
        
        else:
            raise HTTPException(status_code=400, detail=f"지원하지 않는 메서드: {request.method}")
    
    except Exception as e:
        logger.error(f"MCP 요청 처리 중 오류: {str(e)}")
        return McpResponse(
            id=request.id,
            error={
                "code": -32603,
                "message": "Internal error",
                "data": str(e)
            }
        )

async def call_romanize_server(request: McpRequest) -> McpResponse:
    """로마자 변환 서버 호출"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ROMANIZE_SERVER_URL}/mcp/jsonrpc",
                json=request.dict()
            )
            response.raise_for_status()
            return McpResponse(**response.json())
    except Exception as e:
        logger.error(f"로마자 변환 서버 호출 실패: {str(e)}")
        return McpResponse(
            id=request.id,
            error={
                "code": -32603,
                "message": "로마자 변환 서버 오류",
                "data": str(e)
            }
        )

async def call_tts_server(request: McpRequest) -> McpResponse:
    """TTS 서버 호출"""
    try:
        tool_name = request.params.get("name")
        arguments = request.params.get("arguments", {})
        
        if tool_name == "tts_synthesize":
            # TTS 서버의 REST API 호출
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{TTS_SERVER_URL}/api/v1/tts/synthesize",
                    json=arguments
                )
                response.raise_for_status()
                
                # MCP 응답 형식으로 변환
                return McpResponse(
                    id=request.id,
                    result={
                        "content": [{
                            "type": "text",
                            "text": f"음성 파일이 생성되었습니다.\n다운로드: {TTS_SERVER_URL}/api/v1/tts/synthesize\n파일명: audio.mp3"
                        }]
                    }
                )
        
        elif tool_name == "tts_stream":
            # TTS 스트리밍 링크 제공
            return McpResponse(
                id=request.id,
                result={
                    "content": [{
                        "type": "text",
                        "text": f"음성 스트리밍: {TTS_SERVER_URL}/api/v1/tts/stream"
                    }]
                }
            )
        
        else:
            raise HTTPException(status_code=400, detail=f"알 수 없는 TTS 도구: {tool_name}")
    
    except Exception as e:
        logger.error(f"TTS 서버 호출 실패: {str(e)}")
        return McpResponse(
            id=request.id,
            error={
                "code": -32603,
                "message": "TTS 서버 오류",
                "data": str(e)
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
