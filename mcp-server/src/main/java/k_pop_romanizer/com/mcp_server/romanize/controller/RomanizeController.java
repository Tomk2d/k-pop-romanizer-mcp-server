package k_pop_romanizer.com.mcp_server.romanize.controller;

import k_pop_romanizer.com.mcp_server.romanize.dto.RomanizeRequest;
import k_pop_romanizer.com.mcp_server.romanize.dto.RomanizeResponse;
import k_pop_romanizer.com.mcp_server.romanize.dto.SimpleTextRequest;
import k_pop_romanizer.com.mcp_server.romanize.service.RomanizeService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * 한국어 로마자 변환 MCP 서버 컨트롤러
 */
@Slf4j
@RestController
@RequestMapping("/api/v1/romanize")
@RequiredArgsConstructor
public class RomanizeController {
    
    private final RomanizeService romanizeService;
    
    /**
     * 단문 변환 (줄바꿈이 없는 문장)
     */
    @PostMapping("/sentence")
    public ResponseEntity<RomanizeResponse> romanizeSingle(@Valid @RequestBody SimpleTextRequest request) {
        log.info("단문 로마자 변환 API 호출: textLength={}", request.getText().length());
        
        try {
            RomanizeRequest romanizeRequest = new RomanizeRequest();
            romanizeRequest.setKoreanText(request.getText());
            romanizeRequest.setMode(RomanizeRequest.RomanizeMode.SINGLE);
            
            RomanizeResponse response = romanizeService.romanize(romanizeRequest);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("단문 로마자 변환 중 오류 발생", e);
            return ResponseEntity.internalServerError().build();
        }
    }
    
    /**
     * 가사 변환 (줄바꿈이 있는 문단 단위) - 한글-영어-줄바꿈 형태
     */
    @PostMapping("/lyrics")
    public ResponseEntity<RomanizeResponse> romanizeLyrics(@Valid @RequestBody SimpleTextRequest request) {
        log.info("가사 로마자 변환 API 호출: textLength={}", request.getText().length());
        
        try {
            RomanizeRequest romanizeRequest = new RomanizeRequest();
            romanizeRequest.setKoreanText(request.getText());
            romanizeRequest.setMode(RomanizeRequest.RomanizeMode.LYRICS);
            
            RomanizeResponse response = romanizeService.romanize(romanizeRequest);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("가사 로마자 변환 중 오류 발생", e);
            return ResponseEntity.internalServerError().build();
        }
    }
    
    /**
     * 헬스 체크
     */
    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("Romanize service is healthy");
    }
}
