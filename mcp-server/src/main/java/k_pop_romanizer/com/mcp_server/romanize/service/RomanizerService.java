package k_pop_romanizer.com.mcp_server.romanize.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import k_pop_romanizer.com.mcp_server.utils.HangulSyllable;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;

/**
 * 한국어 로마자 변환 서비스
 * JavaScript의 romanizer.js를 Java로 포팅
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class RomanizerService {
    
    private final KoreanPronunciationService koreanPronunciationService;
    
    // 로마자 변환 테이블
    private static final Map<String, String> ROMA_CHO = new HashMap<>();
    private static final Map<String, String> ROMA_JUNG = new HashMap<>();
    private static final Map<String, String> ROMA_JONG = new HashMap<>();
    
    // 한국어 포함 여부 확인을 위한 정규식
    private static final Pattern KOREAN_PATTERN = Pattern.compile("[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]");
    
    static {
        // 초성 로마자 매핑
        ROMA_CHO.put("ㄱ", "k");
        ROMA_CHO.put("ㄲ", "kk");
        ROMA_CHO.put("ㄴ", "n");
        ROMA_CHO.put("ㄷ", "d");
        ROMA_CHO.put("ㄸ", "tt");
        ROMA_CHO.put("ㄹ", "r");
        ROMA_CHO.put("ㅁ", "m");
        ROMA_CHO.put("ㅂ", "b");
        ROMA_CHO.put("ㅃ", "pp");
        ROMA_CHO.put("ㅅ", "s");
        ROMA_CHO.put("ㅆ", "ss");
        ROMA_CHO.put("ㅇ", "");
        ROMA_CHO.put("ㅈ", "j");
        ROMA_CHO.put("ㅉ", "jj");
        ROMA_CHO.put("ㅊ", "ch");
        ROMA_CHO.put("ㅋ", "k");
        ROMA_CHO.put("ㅌ", "t");
        ROMA_CHO.put("ㅍ", "p");
        ROMA_CHO.put("ㅎ", "h");
        
        // 중성 로마자 매핑
        ROMA_JUNG.put("ㅏ", "a");
        ROMA_JUNG.put("ㅐ", "ae");
        ROMA_JUNG.put("ㅑ", "ya");
        ROMA_JUNG.put("ㅒ", "yae");
        ROMA_JUNG.put("ㅓ", "eo");
        ROMA_JUNG.put("ㅔ", "e");
        ROMA_JUNG.put("ㅕ", "yeo");
        ROMA_JUNG.put("ㅖ", "ye");
        ROMA_JUNG.put("ㅗ", "o");
        ROMA_JUNG.put("ㅘ", "wa");
        ROMA_JUNG.put("ㅙ", "wae");
        ROMA_JUNG.put("ㅚ", "oe");
        ROMA_JUNG.put("ㅛ", "yo");
        ROMA_JUNG.put("ㅜ", "u");
        ROMA_JUNG.put("ㅝ", "wo");
        ROMA_JUNG.put("ㅞ", "we");
        ROMA_JUNG.put("ㅟ", "wi");
        ROMA_JUNG.put("ㅠ", "yu");
        ROMA_JUNG.put("ㅡ", "eu");
        ROMA_JUNG.put("ㅢ", "ui");
        ROMA_JUNG.put("ㅣ", "i");
        
        // 종성 로마자 매핑
        ROMA_JONG.put("", "");
        ROMA_JONG.put("ㄱ", "k");
        ROMA_JONG.put("ㄲ", "k");
        ROMA_JONG.put("ㄳ", "k");
        ROMA_JONG.put("ㄴ", "n");
        ROMA_JONG.put("ㄵ", "n");
        ROMA_JONG.put("ㄶ", "n");
        ROMA_JONG.put("ㄷ", "t");
        ROMA_JONG.put("ㄹ", "l");
        ROMA_JONG.put("ㄺ", "k");
        ROMA_JONG.put("ㄻ", "m");
        ROMA_JONG.put("ㄼ", "p");
        ROMA_JONG.put("ㄽ", "l");
        ROMA_JONG.put("ㄾ", "l");
        ROMA_JONG.put("ㄿ", "p");
        ROMA_JONG.put("ㅀ", "l");
        ROMA_JONG.put("ㅁ", "m");
        ROMA_JONG.put("ㅂ", "p");
        ROMA_JONG.put("ㅄ", "p");
        ROMA_JONG.put("ㅅ", "t");
        ROMA_JONG.put("ㅆ", "t");
        ROMA_JONG.put("ㅇ", "ng");
        ROMA_JONG.put("ㅈ", "t");
        ROMA_JONG.put("ㅊ", "t");
        ROMA_JONG.put("ㅋ", "k");
        ROMA_JONG.put("ㅌ", "t");
        ROMA_JONG.put("ㅍ", "p");
        ROMA_JONG.put("ㅎ", "t");
    }
    
    /**
     * 한글을 로마자로 변환
     */
    public String koreanToRoman(String text) {
        if (text == null || text.trim().isEmpty()) {
            return "";
        }
        
        log.debug("한국어 로마자 변환 시작: {}", text);
        
        // 발음 규칙 적용
        String pronounced = koreanPronunciationService.koreanToPronounced(text);
        
        StringBuilder result = new StringBuilder();
        for (char ch : pronounced.toCharArray()) {
            HangulSyllable syllable = koreanPronunciationService.decomposeHangul(ch);
            if (syllable != null) {
                String cho = ROMA_CHO.getOrDefault(syllable.getCho(), "");
                String jung = ROMA_JUNG.getOrDefault(syllable.getJung(), "");
                String jong = ROMA_JONG.getOrDefault(syllable.getJong(), "");
                result.append(cho).append(jung).append(jong);
            } else {
                result.append(ch); // 공백, 문장부호 그대로
            }
        }
        
        String romanized = result.toString();
        log.debug("한국어 로마자 변환 완료: {} -> {}", text, romanized);
        
        return romanized;
    }
    
    /**
     * 한국어가 포함되어 있는지 확인
     */
    public boolean containsKorean(String text) {
        if (text == null || text.trim().isEmpty()) {
            return false;
        }
        return KOREAN_PATTERN.matcher(text).find();
    }
}
