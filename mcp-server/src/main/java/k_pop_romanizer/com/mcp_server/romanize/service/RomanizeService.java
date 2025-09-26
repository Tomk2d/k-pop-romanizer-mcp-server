package k_pop_romanizer.com.mcp_server.romanize.service;

import k_pop_romanizer.com.mcp_server.romanize.dto.RomanizeRequest;
import k_pop_romanizer.com.mcp_server.romanize.dto.RomanizeResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * 한국어 로마자 변환 메인 서비스
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class RomanizeService {
    
    private final RomanizerService romanizerService;
    
    /**
     * 한국어 텍스트를 로마자로 변환
     */
    public RomanizeResponse romanize(RomanizeRequest request) {
        log.info("로마자 변환 요청: mode={}, textLength={}", 
                request.getMode(), request.getKoreanText().length());
        
        if (request.getMode() == RomanizeRequest.RomanizeMode.SINGLE) {
            return romanizeSingle(request.getKoreanText());
        } else {
            return romanizeLyrics(request.getKoreanText());
        }
    }
    
    /**
     * 단문 변환
     */
    private RomanizeResponse romanizeSingle(String koreanText) {
        String romanizedText = romanizerService.koreanToRoman(koreanText);
        
        return RomanizeResponse.builder()
                .originalText(koreanText)
                .romanizedText(romanizedText)
                .mode("SINGLE")
                .build();
    }
    
    /**
     * 가사 변환 (여러 줄) - 한글-영어-줄바꿈 형태
     */
    private RomanizeResponse romanizeLyrics(String koreanText) {
        List<String> lines = Arrays.asList(koreanText.split("\n"));
        List<RomanizeResponse.RomanizedLine> romanizedLines = new ArrayList<>();
        
        for (int i = 0; i < lines.size(); i++) {
            String line = lines.get(i).trim();
            
            if (line.isEmpty()) {
                // 빈 줄 처리
                romanizedLines.add(RomanizeResponse.RomanizedLine.builder()
                        .koreanText("")
                        .romanizedText("")
                        .hasKorean(false)
                        .build());
            } else {
                boolean hasKorean = romanizerService.containsKorean(line);
                String romanizedLine;
                
                if (hasKorean) {
                    romanizedLine = romanizerService.koreanToRoman(line);
                } else {
                    romanizedLine = line; // 한국어가 아닌 경우 그대로
                }
                
                romanizedLines.add(RomanizeResponse.RomanizedLine.builder()
                        .koreanText(line)
                        .romanizedText(romanizedLine)
                        .hasKorean(hasKorean)
                        .build());
            }
        }
        
        return RomanizeResponse.builder()
                .originalText(koreanText)
                .romanizedText(null) // LYRICS 모드에서는 romanizedText 제거
                .romanizedLines(romanizedLines)
                .mode("LYRICS")
                .build();
    }
}
