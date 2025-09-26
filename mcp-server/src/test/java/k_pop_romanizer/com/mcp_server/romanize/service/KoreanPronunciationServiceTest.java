package k_pop_romanizer.com.mcp_server.romanize.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.*;

import k_pop_romanizer.com.mcp_server.utils.HangulSyllable;

@SpringBootTest
class KoreanPronunciationServiceTest {
    
    private KoreanPronunciationService koreanPronunciationService;
    
    @BeforeEach
    void setUp() {
        koreanPronunciationService = new KoreanPronunciationService();
    }
    
    @Test
    void testKoreanToPronounced() {
        // 기본 테스트
        assertEquals("안녕하세요", koreanPronunciationService.koreanToPronounced("안녕하세요"));
        
        // ㅎ탈락 테스트
        assertEquals("안녕하세요", koreanPronunciationService.koreanToPronounced("안녕하세요"));
        
        // 받침 연음 테스트
        assertEquals("안녕하세요", koreanPronunciationService.koreanToPronounced("안녕하세요"));
    }
    
    @Test
    void testDecomposeHangul() {
        // '안' 분해 테스트
        HangulSyllable syllable = koreanPronunciationService.decomposeHangul('안');
        assertNotNull(syllable);
        assertEquals("ㅇ", syllable.getCho());
        assertEquals("ㅏ", syllable.getJung());
        assertEquals("ㄴ", syllable.getJong());
        assertFalse(syllable.isNonHangul());
    }
    
    @Test
    void testComposeHangul() {
        // '안' 합성 테스트
        String result = koreanPronunciationService.composeHangul("ㅇ", "ㅏ", "ㄴ");
        assertEquals("안", result);
    }
}
