package k_pop_romanizer.com.mcp_server.romanize.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class RomanizerServiceTest {
    
    private RomanizerService romanizerService;
    
    @BeforeEach
    void setUp() {
        KoreanPronunciationService koreanPronunciationService = new KoreanPronunciationService();
        romanizerService = new RomanizerService(koreanPronunciationService);
    }
    
    @Test
    void testKoreanToRoman() {
        // 기본 테스트
        String result = romanizerService.koreanToRoman("안녕하세요");
        assertNotNull(result);
        assertFalse(result.isEmpty());
        
        // 빈 문자열 테스트
        assertEquals("", romanizerService.koreanToRoman(""));
        assertEquals("", romanizerService.koreanToRoman(null));
        
        // 공백 포함 테스트
        String resultWithSpace = romanizerService.koreanToRoman("안녕 하세요");
        assertNotNull(resultWithSpace);
    }
    
    @Test
    void testContainsKorean() {
        // 한국어 포함 테스트
        assertTrue(romanizerService.containsKorean("안녕하세요"));
        assertTrue(romanizerService.containsKorean("Hello 안녕"));
        assertTrue(romanizerService.containsKorean("ㅎㅏㅣ"));
        
        // 한국어 미포함 테스트
        assertFalse(romanizerService.containsKorean("Hello World"));
        assertFalse(romanizerService.containsKorean("123456"));
        assertFalse(romanizerService.containsKorean(""));
        assertFalse(romanizerService.containsKorean(null));
    }
}
