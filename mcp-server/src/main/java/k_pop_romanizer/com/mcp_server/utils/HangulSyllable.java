package k_pop_romanizer.com.mcp_server.utils;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 한글 음절 정보를 담는 클래스
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class HangulSyllable {
    
    /**
     * 초성
     */
    private String cho;
    
    /**
     * 중성
     */
    private String jung;
    
    /**
     * 종성
     */
    private String jong;
    
    /**
     * 한글이 아닌 문자 여부
     */
    private boolean isNonHangul;
    
    /**
     * 적용된 발음 규칙
     */
    private String appliedRule;
}


