package k_pop_romanizer.com.mcp_server.mcp.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class McpRequest {
    @JsonProperty("jsonrpc")
    private String jsonrpc = "2.0";
    
    private String id;
    private String method;
    private Object params;
}
