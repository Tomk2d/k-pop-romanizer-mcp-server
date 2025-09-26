package k_pop_romanizer.com.mcp_server.romanize.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;

/**
 * 간단한 텍스트 요청 DTO
 */
@Data
public class SimpleTextRequest {
    
    @NotBlank(message = "변환할 텍스트를 입력해주세요.")
    @Size(max = 1000, message = "텍스트는 1000자를 초과할 수 없습니다.")
    private String text;
}
