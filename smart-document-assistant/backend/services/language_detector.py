"""
Language Detection and Validation Utility
Ensures strict language enforcement in responses
"""
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

# Language patterns for detection
LANGUAGE_PATTERNS = {
    "en": {
        "name": "English",
        "script": "Latin",
        # Common English stop words
        "markers": ["the", "a", "is", "are", "at", "to", "for", "of", "and", "or", "in", "on", "with", "this", "that"]
    },
    "hi": {
        "name": "हिंदी (Hindi)",
        "script": "Devanagari",
        # Devanagari characters range: U+0900 to U+097F
        "char_range": (0x0900, 0x097F),
        # Common Hindi stop words
        "markers": ["है", "को", "में", "का", "यह", "वह", "और", "या", "के", "की", "जो", "कि"]
    },
    "mr": {
        "name": "मराठी (Marathi)",
        "script": "Devanagari",
        # Devanagari characters range: U+0900 to U+097F
        "char_range": (0x0900, 0x097F),
        # Common Marathi stop words
        "markers": ["आहे", "को", "मध्ये", "चा", "ही", "ते", "आणि", "किंवा", "कोण", "जे", "जी"]
    }
}


def detect_language(text: str) -> Tuple[str, float]:
    """
    Detect the language of given text using heuristics
    
    Args:
        text: Text to analyze
        
    Returns:
        Tuple of (detected_language, confidence)
        - detected_language: 'en', 'hi', 'mr'
        - confidence: 0.0 to 1.0, where 1.0 is highest confidence
    """
    if not text or not text.strip():
        return "en", 0.0  # Default to English with low confidence
    
    # Count scripts
    devanagari_chars = 0
    latin_chars = 0
    other_chars = 0
    total_chars = len(text)
    
    for char in text:
        code = ord(char)
        
        # Check for Devanagari script (used by both Hindi and Marathi)
        if 0x0900 <= code <= 0x097F:
            devanagari_chars += 1
        # Check for Latin script
        elif (0x0041 <= code <= 0x005A) or (0x0061 <= code <= 0x007A):
            latin_chars += 1
        elif code > 127:  # Other non-ASCII
            other_chars += 1
    
    # Calculate percentages
    devanagari_pct = devanagari_chars / total_chars if total_chars > 0 else 0
    latin_pct = latin_chars / total_chars if total_chars > 0 else 0
    
    logger.info(f"[LANGUAGE_DETECTION] Devanagari: {devanagari_pct:.2%}, Latin: {latin_pct:.2%}")
    
    # Decision logic
    if devanagari_pct > 0.5:
        # Devanagari script - could be Hindi or Marathi
        # Use content analysis (markers) to distinguish
        hindi_score = sum(1 for marker in LANGUAGE_PATTERNS["hi"]["markers"] if marker in text)
        marathi_score = sum(1 for marker in LANGUAGE_PATTERNS["mr"]["markers"] if marker in text)
        
        if marathi_score > hindi_score:
            confidence = min(0.95, 0.5 + marathi_score * 0.1)
            return "mr", confidence
        else:
            confidence = min(0.95, 0.5 + hindi_score * 0.1)
            return "hi", confidence
    elif latin_pct > 0.5:
        # Latin script - English
        confidence = min(0.95, 0.5 + latin_pct)
        return "en", confidence
    else:
        # Mixed or unclear - check for specific markers
        en_score = sum(1 for marker in LANGUAGE_PATTERNS["en"]["markers"] if marker.lower() in text.lower())
        hi_score = sum(1 for marker in LANGUAGE_PATTERNS["hi"]["markers"] if marker in text)
        mr_score = sum(1 for marker in LANGUAGE_PATTERNS["mr"]["markers"] if marker in text)
        
        scores = {"en": en_score, "hi": hi_score, "mr": mr_score}
        # Find language with highest score
        max_score = max(scores.values()) if scores.values() else 0
        detected = next((lang for lang, score in scores.items() if score == max_score), "en")
        confidence = scores[detected] / (sum(scores.values()) + 1) if sum(scores.values()) > 0 else 0.3
        
        return detected, min(confidence, 0.9)


def is_response_in_language(response: str, expected_language: str) -> Tuple[bool, str, float]:
    """
    Validate if response is in the expected language
    
    Args:
        response: Response text to validate
        expected_language: Expected language code ('en', 'hi', 'mr')
        
    Returns:
        Tuple of (is_valid, detected_language, confidence)
    """
    if not response or not response.strip():
        logger.warning("[LANGUAGE_VALIDATION] Empty response")
        return False, "unknown", 0.0
    
    detected_lang, confidence = detect_language(response)
    
    is_valid = detected_lang == expected_language
    
    logger.info(f"[LANGUAGE_VALIDATION] Expected: {expected_language}, Detected: {detected_lang}, Confidence: {confidence:.2%}, Valid: {is_valid}")
    
    return is_valid, detected_lang, confidence


def validate_language_strict(
    response: str,
    expected_language: str,
    min_confidence: float = 0.6
) -> bool:
    """
    Strict validation - returns True only if confident about language match
    
    Args:
        response: Response text to validate
        expected_language: Expected language code
        min_confidence: Minimum confidence threshold (default 0.6)
        
    Returns:
        True if response is definitely in expected language, False otherwise
    """
    is_valid, detected_lang, confidence = is_response_in_language(response, expected_language)
    
    # Strict check: must match AND have high confidence
    is_strict_valid = is_valid and confidence >= min_confidence
    
    logger.info(f"[STRICT_VALIDATION] Result: {is_strict_valid} (confidence: {confidence:.2%}, threshold: {min_confidence:.2%})")
    
    return is_strict_valid


def get_strict_language_instruction(language: str) -> str:
    """
    Get strict language instruction for LLM prompt
    
    Args:
        language: Language code ('en', 'hi', 'mr')
        
    Returns:
        Language instruction string
    """
    instructions = {
        "en": (
            "IMPORTANT: You MUST answer ONLY in English. "
            "Do not mix languages. Do not use Hindi or Marathi. "
            "Every word must be in English."
        ),
        "hi": (
            "महत्वपूर्ण: आप केवल हिंदी में उत्तर दें। "
            "भाषाओं को मिश्रित न करें। अंग्रेजी या मराठी का उपयोग न करें। "
            "हर शब्द हिंदी में होना चाहिए।"
        ),
        "mr": (
            "महत्वाचे: तुम्ही फक्त मराठीतच उत्तर द्या। "
            "भाषा मिश्रित करू नका। इंग्रजी किंवा हिंदी वापरू नका। "
            "प्रत्येक शब्द मराठीत असला पाहिजे।"
        )
    }
    
    return instructions.get(language, instructions["en"])


def log_language_decision(
    language: str,
    context_size: int,
    question: str,
    detected_in_response: str,
    is_valid: bool
) -> None:
    """
    Log language decision for debugging
    
    Args:
        language: Requested language
        context_size: Size of context provided
        question: User question
        detected_in_response: Detected language in response
        is_valid: Whether validation passed
    """
    status = "✓ VALID" if is_valid else "✗ INVALID"
    logger.info(f"""
[LANGUAGE_SUMMARY]
  Requested Language: {language}
  Question Length: {len(question)} chars
  Context Size: {context_size} chars
  Detected in Response: {detected_in_response}
  Validation: {status}
""")
