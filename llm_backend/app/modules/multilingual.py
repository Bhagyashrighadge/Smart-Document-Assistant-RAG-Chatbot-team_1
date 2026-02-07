from typing import Protocol
from abc import abstractmethod
from langdetect import detect
import os

class TranslatorStrategy(Protocol):
    @abstractmethod
    def translate(self, text: str, target_lang: str) -> str:
        ...

class GoogleTranslateStrategy:
    def __init__(self):
        try:
            from google.cloud import translate_v2 as translate
            self.client = translate.Client()
        except Exception:
            self.client = None

    def translate(self, text: str, target_lang: str) -> str:
        if not self.client:
            # fallback: return original text
            return text
        result = self.client.translate(text, target_language=target_lang)
        return result.get('translatedText', text)

class IndicNLPStrategy:
    def __init__(self):
        # Indic NLP libraries often require extra setup; keep simple fallback
        self.available = False

    def translate(self, text: str, target_lang: str) -> str:
        # Placeholder: real integration would call Indic NLP or a local model
        return text

class MultilingualManager:
    """Detect language and translate using selected strategy."""

    def __init__(self, provider: str = 'google'):
        self.provider = provider
        if provider == 'google':
            self.strategy = GoogleTranslateStrategy()
        else:
            self.strategy = IndicNLPStrategy()

    def detect_language(self, text: str) -> str:
        try:
            lang = detect(text)
            # Map 'hi' and 'mr' as possible outputs from langdetect
            return lang
        except Exception:
            return 'en'

    def translate(self, text: str, target_lang: str) -> str:
        if target_lang == 'en':
            return text
        return self.strategy.translate(text, target_lang)
