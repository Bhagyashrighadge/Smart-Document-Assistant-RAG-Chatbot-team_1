"""
Translator Service - Translate responses to Hindi and Marathi
"""
import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class TranslatorService:
    """Handles translation using Google Translate API (free tier)"""
    
    # Language codes
    LANGUAGES = {
        "en": "en",
        "hi": "hi",
        "mr": "mr"
    }
    
    @staticmethod
    def translate(text: str, target_language: str) -> Optional[str]:
        """
        Translate text to target language using MyMemory Translation API (free)
        
        Args:
            text: Text to translate
            target_language: Target language code (en, hi, mr)
            
        Returns:
            Translated text or original if translation fails
        """
        if target_language == "en":
            return text
        
        try:
            # Map our language codes to MyMemory API codes
            lang_map = {
                "hi": "hi",
                "mr": "mr"
            }
            
            target_code = lang_map.get(target_language)
            if not target_code:
                logger.warning(f"Unsupported language: {target_language}")
                return text
            
            # Using MyMemory Translation API (free, no key required)
            url = "https://api.mymemory.translated.net/get"
            params = {
                "q": text,
                "langpair": f"en|{target_code}"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get("responseStatus") == 200:
                translated_text = result.get("responseData", {}).get("translatedText")
                if translated_text:
                    return translated_text
            
            logger.warning(f"Translation API returned status: {result.get('responseStatus')}")
            return text
        
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return text
    
    @staticmethod
    def get_supported_languages() -> dict:
        """Get supported languages"""
        return TranslatorService.LANGUAGES
