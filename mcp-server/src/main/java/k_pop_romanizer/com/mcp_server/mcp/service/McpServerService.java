package k_pop_romanizer.com.mcp_server.mcp.service;

import k_pop_romanizer.com.mcp_server.mcp.dto.McpTool;
import k_pop_romanizer.com.mcp_server.mcp.dto.McpToolResult;
import k_pop_romanizer.com.mcp_server.romanize.service.RomanizeService;
import k_pop_romanizer.com.mcp_server.romanize.dto.RomanizeRequest;
import k_pop_romanizer.com.mcp_server.romanize.dto.RomanizeResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
@RequiredArgsConstructor
@Slf4j
public class McpServerService {

    private final RomanizeService romanizeService;

    public List<McpTool> getAvailableTools() {
        return Arrays.asList(
            McpTool.builder()
                .name("romanize_single")
                .description("한국어 단문을 로마자(영어 발음)로 변환합니다. 줄바꿈이 없는 문장에 적합합니다.")
                .inputSchema(Map.of(
                    "type", "object",
                    "properties", Map.of(
                        "text", Map.of(
                            "type", "string",
                            "description", "변환할 한국어 텍스트"
                        )
                    ),
                    "required", Arrays.asList("text")
                ))
                .build(),
            McpTool.builder()
                .name("romanize_lyrics")
                .description("한국어 가사를 로마자(영어 발음)로 변환합니다. 줄바꿈이 있는 문단에 적합합니다.")
                .inputSchema(Map.of(
                    "type", "object",
                    "properties", Map.of(
                        "text", Map.of(
                            "type", "string",
                            "description", "변환할 한국어 가사 텍스트"
                        )
                    ),
                    "required", Arrays.asList("text")
                ))
                .build()
        );
    }

    public McpToolResult executeTool(String toolName, Map<String, Object> arguments) {
        try {
            switch (toolName) {
                case "romanize_single":
                    return executeRomanizeSingle(arguments);
                case "romanize_lyrics":
                    return executeRomanizeLyrics(arguments);
                default:
                    return McpToolResult.builder()
                            .isError(true)
                            .errorMessage("알 수 없는 도구: " + toolName)
                            .build();
            }
        } catch (Exception e) {
            log.error("도구 실행 중 오류 발생: {}", toolName, e);
            return McpToolResult.builder()
                    .isError(true)
                    .errorMessage("도구 실행 중 오류가 발생했습니다: " + e.getMessage())
                    .build();
        }
    }

    private McpToolResult executeRomanizeSingle(Map<String, Object> arguments) {
        String koreanText = (String) arguments.get("text");
        
        RomanizeRequest request = new RomanizeRequest();
        request.setKoreanText(koreanText);
        request.setMode(RomanizeRequest.RomanizeMode.SINGLE);
        
        RomanizeResponse response = romanizeService.romanize(request);
        
        return McpToolResult.builder()
                .content(Arrays.asList(Map.of(
                        "type", "text",
                        "text", response.getRomanizedText()
                )))
                .isError(false)
                .build();
    }

    private McpToolResult executeRomanizeLyrics(Map<String, Object> arguments) {
        String koreanText = (String) arguments.get("text");
        
        RomanizeRequest request = new RomanizeRequest();
        request.setKoreanText(koreanText);
        request.setMode(RomanizeRequest.RomanizeMode.LYRICS);
        
        RomanizeResponse response = romanizeService.romanize(request);
        
        StringBuilder result = new StringBuilder();
        for (RomanizeResponse.RomanizedLine line : response.getRomanizedLines()) {
            result.append(line.getKoreanText()).append("\n");
            result.append(line.getRomanizedText()).append("\n");
        }
        
        return McpToolResult.builder()
                .content(Arrays.asList(Map.of(
                        "type", "text",
                        "text", result.toString()
                )))
                .isError(false)
                .build();
    }
}
