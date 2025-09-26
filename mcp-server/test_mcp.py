#!/usr/bin/env python3
"""
MCP 서버 테스트 스크립트
"""

import requests
import json

# MCP 서버 URL
BASE_URL = "http://localhost:8080/mcp"

def test_health():
    """헬스 체크 테스트"""
    print("=== 헬스 체크 테스트 ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print()

def test_get_tools():
    """도구 목록 조회 테스트"""
    print("=== 도구 목록 조회 테스트 ===")
    response = requests.get(f"{BASE_URL}/tools")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_jsonrpc_tools_list():
    """JSON-RPC로 도구 목록 조회 테스트"""
    print("=== JSON-RPC 도구 목록 조회 테스트 ===")
    payload = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "tools/list",
        "params": {}
    }
    response = requests.post(f"{BASE_URL}/jsonrpc", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_romanize_single():
    """단문 변환 테스트"""
    print("=== 단문 변환 테스트 ===")
    payload = {
        "text": "안녕하세요"
    }
    response = requests.post(f"{BASE_URL}/tools/romanize_single/execute", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_romanize_lyrics():
    """가사 변환 테스트"""
    print("=== 가사 변환 테스트 ===")
    payload = {
        "text": "안녕하세요\n반갑습니다"
    }
    response = requests.post(f"{BASE_URL}/tools/romanize_lyrics/execute", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_jsonrpc_romanize_single():
    """JSON-RPC로 단문 변환 테스트"""
    print("=== JSON-RPC 단문 변환 테스트 ===")
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
    response = requests.post(f"{BASE_URL}/jsonrpc", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

if __name__ == "__main__":
    print("MCP 서버 테스트 시작...")
    print("=" * 50)
    
    try:
        test_health()
        test_get_tools()
        test_jsonrpc_tools_list()
        test_romanize_single()
        test_romanize_lyrics()
        test_jsonrpc_romanize_single()
        
        print("모든 테스트 완료!")
    except Exception as e:
        print(f"테스트 중 오류 발생: {e}")
