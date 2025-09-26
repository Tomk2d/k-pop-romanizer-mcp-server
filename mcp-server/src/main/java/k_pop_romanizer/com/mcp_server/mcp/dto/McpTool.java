package k_pop_romanizer.com.mcp_server.mcp.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.Builder;

import java.util.Map;

@Data
@Builder
public class McpTool {
    private String name;
    private String description;
    private Map<String, Object> inputSchema;
}
