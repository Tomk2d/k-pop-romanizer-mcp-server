#!/usr/bin/env python3
"""
MCP Gateway - 중앙집중형 MCP 서버
모든 MCP 요청을 받아서 적절한 백엔드 서비스로 라우팅
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional, Union
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
    id: Optional[Union[str, int]] = None
    method: str
    params: Optional[Dict[str, Any]] = None

class McpResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: Union[str, int]
    result: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None
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
            "description": "한국어 텍스트를 음성으로 변환하여 MP3 파일로 다운로드합니다. url 형태로 제공 되고, 해당 url 로 다운로드 할 수 있습니다.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "변환할 한국어 텍스트. 여러 줄 텍스트인 경우 줄바꿈(\\n)을 절대 제거하지 말고 그대로 포함하세요!"
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
            "description": "한국어 텍스트를 음성으로 변환하여 실시간 스트리밍합니다. url 형태로 제공 되고, 해당 url 로 스트리밍 할 수 있습니다.",
            "inputSchema": {
                "type": "object", 
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "변환할 한국어 텍스트. 여러 줄 텍스트인 경우 줄바꿈(\\n)을 절대 제거하지 말고 그대로 포함하세요!"
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

@app.post("/mcp")
async def handle_mcp_post_request(request: McpRequest):
    """MCP POST 요청 처리 (JSON-RPC 2.0)"""
    try:
        logger.info(f"MCP 요청 수신: {request.method}")
        
        if request.method == "initialize":
            # MCP 초기화 응답 (JSON-RPC 2.0 형식)
            return {
                "jsonrpc": "2.0",
                "id": request.id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "K-Pop Romanizer MCP Server",
                        "version": "1.0.0"
                    }
                }
            }
        
        elif request.method == "notifications/initialized":
            # MCP 초기화 완료 알림 (응답 불필요)
            logger.info("MCP 클라이언트 초기화 완료")
            return None  # 알림에는 응답하지 않음
        
        elif request.method == "tools/list":
            # 모든 도구 목록 통합 (JSON-RPC 2.0 형식)
            all_tools = get_romanize_tools() + get_tts_tools()
            return {
                "jsonrpc": "2.0", 
                "id": request.id,
                "result": {"tools": all_tools}
            }
        
        elif request.method == "tools/call":
            tool_name = request.params.get("name")
            logger.info(f"도구 호출: {tool_name}")
            
            # 로마자 변환 도구
            if tool_name.startswith("romanize_"):
                result = await call_romanize_server(request)
                return {
                    "jsonrpc": "2.0",
                    "id": request.id,
                    "result": {"content": [{"type": "text", "text": str(result)}]}
                }
            # TTS 도구
            elif tool_name.startswith("tts_"):
                result = await call_tts_server(request)
                return {
                    "jsonrpc": "2.0",
                    "id": request.id,
                    "result": {"content": [{"type": "text", "text": str(result)}]}
                }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request.id,
                    "error": {"code": -32601, "message": f"알 수 없는 도구: {tool_name}"}
                }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request.id,
                "error": {"code": -32601, "message": f"지원하지 않는 메서드: {request.method}"}
            }
    
    except Exception as e:
        logger.error(f"MCP 요청 처리 오류: {str(e)}")
        return {
            "jsonrpc": "2.0",
            "id": getattr(request, 'id', 'unknown'),
            "error": {"code": -32603, "message": "Internal error", "data": str(e)}
        }

@app.get("/mcp")
async def handle_mcp_get_request_simple():
    """MCP GET 요청 처리 (PlayMCP 호환성) - 간단한 경로"""
    # 모든 도구 목록 반환 (MCP 표준 형식)
    all_tools = get_romanize_tools() + get_tts_tools()
    return {
        "tools": all_tools
    }

@app.get("/mcp/jsonrpc")
async def handle_mcp_get_request():
    """MCP GET 요청 처리 (PlayMCP 호환성)"""
    # 모든 도구 목록 반환 (MCP 표준 형식)
    all_tools = get_romanize_tools() + get_tts_tools()
    return {
        "tools": all_tools
    }

@app.post("/mcp/jsonrpc")
async def handle_mcp_request(request: McpRequest):
    """MCP JSON-RPC 요청 처리"""
    try:
        logger.info(f"MCP 요청 수신: {request.method}")
        
        if request.method == "initialize":
            # MCP 초기화 응답
            return {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "K-Pop Romanizer MCP Server",
                    "version": "1.0.0"
                }
            }
        
        elif request.method == "tools/list":
            # 모든 도구 목록 통합 (MCP Inspector 호환)
            all_tools = get_romanize_tools() + get_tts_tools()
            return {"tools": all_tools}
        
        elif request.method == "tools/call":
            tool_name = request.params.get("name")
            arguments = request.params.get("arguments", {})
            
            if tool_name.startswith("romanize_"):
                # 로마자 변환 서버로 전달
                result = await call_romanize_server(request)
                return {"content": [{"type": "text", "text": str(result)}]}
            elif tool_name.startswith("tts_"):
                # TTS 서버로 전달
                result = await call_tts_server(request)
                return {"content": [{"type": "text", "text": str(result)}]}
            else:
                return {"error": f"알 수 없는 도구: {tool_name}"}
        
        else:
            return {"error": f"지원하지 않는 메서드: {request.method}"}
    
    except Exception as e:
        logger.error(f"MCP 요청 처리 중 오류: {str(e)}")
        return {"error": f"Internal error: {str(e)}"}

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
            # GET 방식 TTS 다운로드: 브라우저에서 바로 다운로드 가능
            import urllib.parse
            
            # 파라미터 추출
            text = arguments.get("text", "변환할 텍스트를 주세요")
            voice = arguments.get("voice", "ko-KR-SunHiNeural")
            rate = arguments.get("rate", "+0%")
            volume = arguments.get("volume", "+0%")
            pitch = arguments.get("pitch", "+0Hz")
            
            # URL 인코딩 (모든 파라미터)
            encoded_text = urllib.parse.quote(text)
            encoded_voice = urllib.parse.quote(voice)
            encoded_rate = urllib.parse.quote(rate)
            encoded_volume = urllib.parse.quote(volume)
            encoded_pitch = urllib.parse.quote(pitch)
            
            # 완성된 GET URL 생성
            download_url = f"https://k-pop-romanizer.duckdns.org/tts/api/v1/tts/synthesize?text={encoded_text}&voice={encoded_voice}&rate={encoded_rate}&volume={encoded_volume}&pitch={encoded_pitch}"
            
            return McpResponse(
                id=request.id,
                result={
                    "content": [{
                        "type": "text",
                        "text": f"""💾 **TTS 다운로드 URL**
                                    {download_url}
                                    💡 위 URL을 클릭하거나 브라우저 주소창에 복사해서 붙여넣으면 MP3 파일이 다운로드됩니다!"""
                    }]
                }
            )
        
        elif tool_name == "tts_stream":
            # GET 방식 TTS 스트리밍: 브라우저 주소창에서 바로 재생 가능
            import urllib.parse
            
            # 파라미터 추출
            text = arguments.get("text", "안녕하세요")
            voice = arguments.get("voice", "ko-KR-SunHiNeural")
            rate = arguments.get("rate", "+0%")
            volume = arguments.get("volume", "+0%")
            pitch = arguments.get("pitch", "+0Hz")
            
            # URL 인코딩 (모든 파라미터)
            encoded_text = urllib.parse.quote(text)
            encoded_voice = urllib.parse.quote(voice)
            encoded_rate = urllib.parse.quote(rate)
            encoded_volume = urllib.parse.quote(volume)
            encoded_pitch = urllib.parse.quote(pitch)
            
            # 완성된 GET URL 생성
            stream_url = f"https://k-pop-romanizer.duckdns.org/tts/api/v1/tts/stream?text={encoded_text}&voice={encoded_voice}&rate={encoded_rate}&volume={encoded_volume}&pitch={encoded_pitch}"
            
            return McpResponse(
                id=request.id,
                result={
                    "content": [{
                        "type": "text",
                        "text": f"""🎵 **TTS 재생 URL**
                                    {stream_url}
                                    💡 위 URL을 클릭하거나 브라우저 주소창에 복사해서 붙여넣으면 바로 재생됩니다!"""
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
