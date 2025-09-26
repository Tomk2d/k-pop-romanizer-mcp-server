package k_pop_romanizer.com.mcp_server.romanize.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import k_pop_romanizer.com.mcp_server.romanize.dto.RomanizeRequest;
import k_pop_romanizer.com.mcp_server.romanize.service.RomanizeService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(RomanizeController.class)
class RomanizeControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private RomanizeService romanizeService;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    // testRomanize() - 주석 처리 (해당 엔드포인트가 주석 처리됨)
    
    @Test
    void testRomanizeSingle() throws Exception {
        // When & Then
        mockMvc.perform(post("/api/v1/romanize/sentence")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"text\":\"안녕하세요\"}"))
                .andExpect(status().isOk());
    }
    
    @Test
    void testRomanizeLyrics() throws Exception {
        // When & Then
        mockMvc.perform(post("/api/v1/romanize/lyrics")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"text\":\"안녕하세요\\n반갑습니다\"}"))
                .andExpect(status().isOk());
    }
    
    @Test
    void testHealth() throws Exception {
        // When & Then
        mockMvc.perform(get("/api/v1/romanize/health"))
                .andExpect(status().isOk())
                .andExpect(content().string("Romanize service is healthy"));
    }
}
