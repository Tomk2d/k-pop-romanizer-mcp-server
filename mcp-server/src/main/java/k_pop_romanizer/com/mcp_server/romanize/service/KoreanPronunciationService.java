package k_pop_romanizer.com.mcp_server.romanize.service;

import k_pop_romanizer.com.mcp_server.utils.HangulSyllable;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 한국어 발음 규칙 적용 서비스
 * JavaScript의 koreanPronunciation.js를 Java로 포팅
 */
@Slf4j
@Service
public class KoreanPronunciationService {
    
    // 초성, 중성, 종성 테이블
    private static final String[] CHO = {"ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"};
    private static final String[] JUNG = {"ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"};
    private static final String[] JONG = {"","ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"};
    
    /**
     * 한글 분해
     */
    public HangulSyllable decomposeHangul(char ch) {
        int code = (int) ch;
        if (code < 0xAC00 || code > 0xD7A3) {
            return null;
        }
        
        int base = code - 0xAC00;
        int choIndex = base / 588;
        int jungIndex = (base % 588) / 28;
        int jongIndex = base % 28;
        
        return HangulSyllable.builder()
                .cho(CHO[choIndex])
                .jung(JUNG[jungIndex])
                .jong(JONG[jongIndex])
                .isNonHangul(false)
                .appliedRule(null)
                .build();
    }
    
    /**
     * 한글 합성
     */
    public String composeHangul(String cho, String jung, String jong) {
        int choIndex = findIndex(CHO, cho);
        int jungIndex = findIndex(JUNG, jung);
        int jongIndex = findIndex(JONG, jong);
        
        if (choIndex < 0 || jungIndex < 0 || jongIndex < 0) {
            return "";
        }
        
        return String.valueOf((char) (0xAC00 + choIndex * 588 + jungIndex * 28 + jongIndex));
    }
    
    private int findIndex(String[] array, String value) {
        for (int i = 0; i < array.length; i++) {
            if (array[i].equals(value)) {
                return i;
            }
        }
        return -1;
    }
    
    /**
     * 발음 규칙 적용
     */
    public List<HangulSyllable> applyPronunciationRules(List<HangulSyllable> syllables) {
        for (int i = 0; i < syllables.size(); i++) {
            HangulSyllable current = syllables.get(i);
            HangulSyllable next = (i + 1 < syllables.size()) ? syllables.get(i + 1) : null;
            
            if (current.isNonHangul()) {
                continue; // 공백/특수문자는 건너뜀
            }
            
            // (1) ㅎ 관련 규칙 (ㅎ, ㄶ, ㅀ)
            if (isHRelatedJong(current.getJong()) && next != null && !next.isNonHangul()) {
                String nextCho = next.getCho();
                if ("ㅇ".equals(nextCho)) {
                    if ("ㅀ".equals(current.getJong())) {
                        current.setJong("ㄹ");
                    } else if ("ㄶ".equals(current.getJong())) {
                        current.setJong("ㄴ");
                    } else {
                        current.setJong("");
                    }
                    current.setAppliedRule("ㅎ탈락");
                } else if (isAspiratedConsonant(nextCho)) {
                    if ("ㄱ".equals(nextCho)) next.setCho("ㅋ");
                    if ("ㄷ".equals(nextCho)) next.setCho("ㅌ");
                    if ("ㅂ".equals(nextCho)) next.setCho("ㅍ");
                    if ("ㅀ".equals(current.getJong())) {
                        current.setJong("ㄹ");
                    } else if ("ㄶ".equals(current.getJong())) {
                        current.setJong("ㄴ");
                    } else {
                        current.setJong("");
                    }
                    current.setAppliedRule("ㅎ+자음격음화");
                }
            }
            
            // (2) 자음군 단순화
            if (current.getAppliedRule() == null) {
                Map<String, String> simplifyMap = new HashMap<>();
                simplifyMap.put("ㄳ", "ㄱ");
                simplifyMap.put("ㄵ", "ㄴ");
                simplifyMap.put("ㄺ", "ㄱ");
                simplifyMap.put("ㄻ", "ㅁ");
                simplifyMap.put("ㄼ", "ㅂ");
                simplifyMap.put("ㄽ", "ㄹ");
                simplifyMap.put("ㄾ", "ㄹ");
                simplifyMap.put("ㄿ", "ㅂ");
                simplifyMap.put("ㅄ", "ㅂ");
                
                if (simplifyMap.containsKey(current.getJong())) {
                    current.setJong(simplifyMap.get(current.getJong()));
                }
            }
            
            // (3) 구개음화 (받침 ㄷ/ㅌ + '이')
            if (isDOrT(current.getJong()) && next != null && !next.isNonHangul() 
                && "ㅇ".equals(next.getCho()) && "ㅣ".equals(next.getJung())) {
                if ("ㄷ".equals(current.getJong())) {
                    next.setCho("ㅈ");
                }
                if ("ㅌ".equals(current.getJong())) {
                    next.setCho("ㅊ");
                }
                current.setJong("");
                current.setAppliedRule("구개음화");
            }
            
            // (4) 비음화 (받침 ㄱ/ㄷ/ㅂ + ㄴ/ㅁ)
            if (isGOrDOrB(current.getJong()) && next != null && !next.isNonHangul() 
                && isNOrM(next.getCho())) {
                if ("ㄱ".equals(current.getJong())) {
                    current.setJong("ㅇ");
                }
                if ("ㄷ".equals(current.getJong())) {
                    current.setJong("ㄴ");
                }
                if ("ㅂ".equals(current.getJong())) {
                    current.setJong("ㅁ");
                }
                current.setAppliedRule("비음화");
            }
            
            // (4-1) 받침 ㅂ + ㄷ → [ㅁ+ㄸ] (깊다 → 깁따)
            if ("ㅂ".equals(current.getJong()) && next != null && !next.isNonHangul() 
                && "ㄷ".equals(next.getCho())) {
                current.setJong("ㅁ");
                next.setCho("ㄸ"); // ㄷ → ㄸ 경음화
                current.setAppliedRule("ㅂ+ㄷ변형");
            }
            
            // (5) 유음화 (ㄴ+ㄹ, ㄹ+ㄴ)
            if ("ㄴ".equals(current.getJong()) && next != null && !next.isNonHangul() 
                && "ㄹ".equals(next.getCho())) {
                current.setJong("ㄹ");
                current.setAppliedRule("유음화");
            }
            if ("ㄹ".equals(current.getJong()) && next != null && !next.isNonHangul() 
                && "ㄴ".equals(next.getCho())) {
                next.setCho("ㄹ");
                current.setAppliedRule("유음화");
            }
            
            // (6) 받침 연음
            if (current.getJong() != null && !current.getJong().isEmpty() 
                && next != null && !next.isNonHangul() && "ㅇ".equals(next.getCho())) {
                next.setCho(current.getJong());
                current.setJong("");
                current.setAppliedRule("받침연음");
            }
        }
        return syllables;
    }
    
    /**
     * 메인 변환 함수
     */
    public String koreanToPronounced(String text) {
        List<HangulSyllable> decomposed = new ArrayList<>();
        
        for (char ch : text.toCharArray()) {
            HangulSyllable syllable = decomposeHangul(ch);
            if (syllable != null) {
                decomposed.add(syllable);
            } else {
                decomposed.add(HangulSyllable.builder()
                        .cho("")
                        .jung(String.valueOf(ch))
                        .jong("")
                        .isNonHangul(true)
                        .build());
            }
        }
        
        List<HangulSyllable> applied = applyPronunciationRules(decomposed);
        
        StringBuilder result = new StringBuilder();
        for (HangulSyllable syllable : applied) {
            if (syllable.isNonHangul()) {
                result.append(syllable.getJung());
            } else {
                result.append(composeHangul(syllable.getCho(), syllable.getJung(), syllable.getJong()));
            }
        }
        
        return result.toString();
    }
    
    // 헬퍼 메서드들
    private boolean isHRelatedJong(String jong) {
        return "ㅎ".equals(jong) || "ㄶ".equals(jong) || "ㅀ".equals(jong);
    }
    
    private boolean isAspiratedConsonant(String cho) {
        return "ㄱ".equals(cho) || "ㄷ".equals(cho) || "ㅂ".equals(cho);
    }
    
    private boolean isDOrT(String jong) {
        return "ㄷ".equals(jong) || "ㅌ".equals(jong);
    }
    
    private boolean isGOrDOrB(String jong) {
        return "ㄱ".equals(jong) || "ㄷ".equals(jong) || "ㅂ".equals(jong);
    }
    
    private boolean isNOrM(String cho) {
        return "ㄴ".equals(cho) || "ㅁ".equals(cho);
    }
}
