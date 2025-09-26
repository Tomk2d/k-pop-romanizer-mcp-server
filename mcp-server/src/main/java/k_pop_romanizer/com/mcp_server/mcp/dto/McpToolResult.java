package k_pop_romanizer.com.mcp_server.mcp.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.Builder;

import java.util.List;
import java.util.Map;

@Data
@Builder
public class McpToolResult {
    private List<Map<String, Object>> content;
    private boolean isError;
    private String errorMessage;
}
