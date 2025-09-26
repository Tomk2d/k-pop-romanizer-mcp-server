#!/usr/bin/env python3
"""
통합 MCP 서비스 테스트 스크립트
"""

import requests
import json

# MCP Gateway URL
GATEWAY_URL = "http://localhost:8000"

def test_health():
    """헬스 체크 테스트"""
    print("=== MCP Gateway 헬스 체크 테스트 ===")
    response = requests.get(f"{GATEWAY_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print()

def test_mcp_tools_list():
    """MCP 도구 목록 조회 테스트"""
    print("=== MCP 도구 목록 조회 테스트 ===")
    payload = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "tools/list",
        "params": {}
    }
    response = requests.post(f"{GATEWAY_URL}/mcp/jsonrpc", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_romanize_single():
    """로마자 단문 변환 테스트"""
    print("=== 로마자 단문 변환 테스트 ===")
    payload = {
        "jsonrpc": "2.0",
        "id": "2",
        "method": "tools/call",
        "params": {
            "name": "romanize_single",
            "arguments": {
                "text": "안녕하세요"
            }
        }
    }
    response = requests.post(f"{GATEWAY_URL}/mcp/jsonrpc", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_romanize_lyrics():
    """로마자 가사 변환 테스트"""
    print("=== 로마자 가사 변환 테스트 ===")
    payload = {
        "jsonrpc": "2.0",
        "id": "3",
        "method": "tools/call",
        "params": {
            "name": "romanize_lyrics",
            "arguments": {
                "text": "안녕하세요\n반갑습니다"
            }
        }
    }
    response = requests.post(f"{GATEWAY_URL}/mcp/jsonrpc", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_tts_synthesize():
    """TTS 음성 변환 테스트"""
    print("=== TTS 음성 변환 테스트 ===")
    payload = {
        "jsonrpc": "2.0",
        "id": "4",
        "method": "tools/call",
        "params": {
            "name": "tts_synthesize",
            "arguments": {
                "text": "안녕하세요",
                "voice": "ko-KR-SunHiNeural"
            }
        }
    }
    response = requests.post(f"{GATEWAY_URL}/mcp/jsonrpc", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_tts_stream():
    """TTS 스트리밍 테스트"""
    print("=== TTS 스트리밍 테스트 ===")
    payload = {
        "jsonrpc": "2.0",
        "id": "5",
        "method": "tools/call",
        "params": {
            "name": "tts_stream",
            "arguments": {
                "text": "안녕하세요",
                "voice": "ko-KR-SunHiNeural"
            }
        }
    }
    response = requests.post(f"{GATEWAY_URL}/mcp/jsonrpc", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

if __name__ == "__main__":
    print("통합 MCP 서비스 테스트 시작...")
    print("=" * 50)
    
    try:
        test_health()
        test_mcp_tools_list()
        test_romanize_single()
        test_romanize_lyrics()
        test_tts_synthesize()
        test_tts_stream()
        
        print("모든 테스트 완료!")
    except Exception as e:
        print(f"테스트 중 오류 발생: {e}")
