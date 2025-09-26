package k_pop_romanizer.com.mcp_server.romanize.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * 한국어 로마자 변환 응답 DTO
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class RomanizeResponse {
    
    /**
     * 원본 한국어 텍스트
     */
    private String originalText;
    
    /**
     * 변환된 로마자 텍스트 (SINGLE 모드에서만 사용)
     */
    @JsonInclude(JsonInclude.Include.NON_NULL)
    private String romanizedText;
    
    /**
     * 가사 모드일 때 각 줄별 변환 결과
     */
    @JsonInclude(JsonInclude.Include.NON_NULL)
    private List<RomanizedLine> romanizedLines;
    
    /**
     * 변환 모드
     */
    private String mode;
    
    /**
     * 로마자 변환 한 줄 정보
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class RomanizedLine {
        private String koreanText;
        private String romanizedText;
        private boolean hasKorean;
    }
}
