package k_pop_romanizer.com.mcp_server.mcp.controller;

import k_pop_romanizer.com.mcp_server.mcp.dto.McpRequest;
import k_pop_romanizer.com.mcp_server.mcp.dto.McpResponse;
import k_pop_romanizer.com.mcp_server.mcp.dto.McpTool;
import k_pop_romanizer.com.mcp_server.mcp.dto.McpToolResult;
import k_pop_romanizer.com.mcp_server.mcp.service.McpServerService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/mcp")
@RequiredArgsConstructor
public class McpController {

    private final McpServerService mcpServerService;

    @PostMapping("/jsonrpc")
    public ResponseEntity<McpResponse> handleJsonRpc(@RequestBody McpRequest request) {
        try {
            McpResponse response = new McpResponse();
            response.setId(request.getId());
            
            switch (request.getMethod()) {
                case "tools/list":
                    response.setResult(Map.of("tools", mcpServerService.getAvailableTools()));
                    break;
                case "tools/call":
                    Map<String, Object> params = (Map<String, Object>) request.getParams();
                    String toolName = (String) params.get("name");
                    Map<String, Object> arguments = (Map<String, Object>) params.get("arguments");
                    
                    McpToolResult result = mcpServerService.executeTool(toolName, arguments);
                    response.setResult(Map.of("content", result.getContent()));
                    break;
                default:
                    McpResponse.McpError error = new McpResponse.McpError();
                    error.setCode(-32601);
                    error.setMessage("Method not found");
                    response.setError(error);
                    break;
            }
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("JSON-RPC 요청 처리 중 오류 발생", e);
            McpResponse response = new McpResponse();
            response.setId(request.getId());
            McpResponse.McpError error = new McpResponse.McpError();
            error.setCode(-32603);
            error.setMessage("Internal error");
            response.setError(error);
            return ResponseEntity.ok(response);
        }
    }

    @GetMapping("/tools")
    public ResponseEntity<List<McpTool>> getTools() {
        try {
            List<McpTool> tools = mcpServerService.getAvailableTools();
            return ResponseEntity.ok(tools);
        } catch (Exception e) {
            log.error("도구 목록 조회 중 오류 발생", e);
            return ResponseEntity.internalServerError().build();
        }
    }

    @PostMapping("/tools/{toolName}/execute")
    public ResponseEntity<McpToolResult> executeTool(
            @PathVariable String toolName,
            @RequestBody Map<String, Object> arguments) {
        try {
            McpToolResult result = mcpServerService.executeTool(toolName, arguments);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            log.error("도구 실행 중 오류 발생: {}", toolName, e);
            return ResponseEntity.internalServerError().build();
        }
    }

    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("MCP Server is healthy");
    }
}
