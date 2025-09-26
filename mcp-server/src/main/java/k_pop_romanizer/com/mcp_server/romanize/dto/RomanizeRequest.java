package k_pop_romanizer.com.mcp_server.romanize.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;

/**
 * 한국어 로마자 변환 요청 DTO
 */
@Data
public class RomanizeRequest {
    
    @NotBlank(message = "변환할 한국어 텍스트를 입력해주세요.")
    @Size(max = 1000, message = "텍스트는 1000자를 초과할 수 없습니다.")
    private String koreanText;
    
    /**
     * 변환 모드 (SINGLE: 단문, LYRICS: 가사)
     */
    private RomanizeMode mode = RomanizeMode.SINGLE;
    
    public enum RomanizeMode {
        SINGLE, LYRICS
    }
}
