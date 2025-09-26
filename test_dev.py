#!/usr/bin/env python3
"""
개발 환경 통합 MCP 서비스 테스트 스크립트
"""

import requests
import json
import time
import subprocess
import sys

# 서비스 URL들
MCP_GATEWAY_URL = "http://localhost:8000"
ROMANIZE_SERVICE_URL = "http://localhost:8080"
TTS_SERVICE_URL = "http://localhost:8001"  # TTS는 8001 포트 사용

def check_service_health(url, service_name, health_path="/health"):
    """서비스 헬스 체크"""
    try:
        response = requests.get(f"{url}{health_path}", timeout=5)
        if response.status_code == 200:
            print(f"✅ {service_name}: 정상")
            return True
        else:
            print(f"❌ {service_name}: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {service_name}: 연결 실패 - {str(e)}")
        return False

def wait_for_services():
    """모든 서비스가 준비될 때까지 대기"""
    print("🔄 서비스 시작 대기 중...")
    
    services = [
        (MCP_GATEWAY_URL, "MCP Gateway", "/health"),
        (ROMANIZE_SERVICE_URL, "Romanize Service", "/mcp/health"),
        (TTS_SERVICE_URL, "TTS Service", "/health")
    ]
    
    max_attempts = 30  # 5분 대기
    for attempt in range(max_attempts):
        print(f"시도 {attempt + 1}/{max_attempts}")
        
        all_healthy = True
        for url, name, health_path in services:
            if not check_service_health(url, name, health_path):
                all_healthy = False
                break
        
        if all_healthy:
            print("🎉 모든 서비스가 정상적으로 시작되었습니다!")
            return True
        
        time.sleep(10)
    
    print("❌ 서비스 시작 시간 초과")
    return False

def test_mcp_tools_list():
    """MCP 도구 목록 조회 테스트"""
    print("\n=== MCP 도구 목록 조회 테스트 ===")
    payload = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "tools/list",
        "params": {}
    }
    
    try:
        response = requests.post(f"{MCP_GATEWAY_URL}/mcp/jsonrpc", json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            tools = data.get("result", {}).get("tools", [])
            print(f"총 {len(tools)}개의 도구 발견:")
            for tool in tools:
                print(f"  - {tool['name']}: {tool['description']}")
        else:
            print(f"Error: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_romanize_single():
    """로마자 단문 변환 테스트"""
    print("\n=== 로마자 단문 변환 테스트 ===")
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
    
    try:
        response = requests.post(f"{MCP_GATEWAY_URL}/mcp/jsonrpc", json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "result" in data:
                content = data["result"].get("content", [])
                for item in content:
                    if item.get("type") == "text":
                        print(f"결과: {item['text']}")
            else:
                print(f"Error: {data}")
        else:
            print(f"Error: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_romanize_lyrics():
    """로마자 가사 변환 테스트"""
    print("\n=== 로마자 가사 변환 테스트 ===")
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
    
    try:
        response = requests.post(f"{MCP_GATEWAY_URL}/mcp/jsonrpc", json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "result" in data:
                content = data["result"].get("content", [])
                for item in content:
                    if item.get("type") == "text":
                        print(f"결과:\n{item['text']}")
            else:
                print(f"Error: {data}")
        else:
            print(f"Error: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_tts_synthesize():
    """TTS 음성 변환 테스트"""
    print("\n=== TTS 음성 변환 테스트 ===")
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
    
    try:
        response = requests.post(f"{MCP_GATEWAY_URL}/mcp/jsonrpc", json=payload, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response data: {data}")  # 디버깅용
            if "result" in data and data["result"]:
                content = data["result"].get("content", [])
                for item in content:
                    if item.get("type") == "text":
                        print(f"결과: {item['text']}")
            else:
                print(f"Error: {data}")
        else:
            print(f"Error: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def run_docker_compose():
    """Docker Compose 실행"""
    print("🚀 Docker Compose로 서비스 시작 중...")
    try:
        result = subprocess.run(
            ["docker-compose", "up", "-d"],
            capture_output=True,
            text=True,
            cwd="."
        )
        
        if result.returncode == 0:
            print("✅ Docker Compose 실행 성공")
            return True
        else:
            print(f"❌ Docker Compose 실행 실패: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Docker Compose 실행 오류: {str(e)}")
        return False

def main():
    """메인 테스트 함수"""
    print("🧪 개발 환경 통합 MCP 서비스 테스트")
    print("=" * 50)
    
    # 1. Docker Compose 실행
    if not run_docker_compose():
        sys.exit(1)
    
    # 2. 서비스 헬스 체크 대기
    if not wait_for_services():
        print("❌ 서비스 시작 실패")
        sys.exit(1)
    
    # 3. MCP 테스트 실행
    print("\n🧪 MCP 기능 테스트 시작...")
    
    tests = [
        ("MCP 도구 목록", test_mcp_tools_list),
        ("로마자 단문 변환", test_romanize_single),
        ("로마자 가사 변환", test_romanize_lyrics),
        ("TTS 음성 변환", test_tts_synthesize)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} 테스트 ---")
        if test_func():
            passed += 1
            print(f"✅ {test_name} 통과")
        else:
            print(f"❌ {test_name} 실패")
    
    # 4. 결과 요약
    print(f"\n📊 테스트 결과: {passed}/{total} 통과")
    
    if passed == total:
        print("🎉 모든 테스트 통과!")
        print("\n🌐 서비스 URL:")
        print(f"  - MCP Gateway: {MCP_GATEWAY_URL}")
        print(f"  - Romanize Service: {ROMANIZE_SERVICE_URL}")
        print(f"  - TTS Service: {TTS_SERVICE_URL}")
    else:
        print("❌ 일부 테스트 실패")
        sys.exit(1)

if __name__ == "__main__":
    main()
