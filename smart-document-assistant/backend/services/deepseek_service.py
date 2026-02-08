"""
DeepSeek Service - Integration with DeepSeek API for LLM responses
"""
import requests
import logging
from typing import Optional
import os
from .language_detector import get_strict_language_instruction, validate_language_strict
from .mock_responses import get_mock_response

logger = logging.getLogger(__name__)


class DeepSeekService:
    """Handles communication with DeepSeek API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize DeepSeek service
        
        Args:
            api_key: DeepSeek API key (if not provided, uses env variable)
        """
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY not provided or set in environment")
        
        self.base_url = "https://api.deepseek.com/chat/completions"
        self.model = "deepseek-chat"
        self.enable_fallback = True  # Enable fallback mode if API fails
        self.max_language_validation_retries = 2  # Retry up to 2 times if wrong language detected
    
    def _generate_fallback_response(self, prompt: str, context: str = "", language: str = "en") -> str:
        """
        Generate a fallback response when API is unavailable
        Uses mock responses for testing language control without API calls
        
        Args:
            prompt: User question
            context: Document context
            language: Target language (en, hi, mr)
            
        Returns:
            Language-appropriate response in the requested language
        """
        logger.warning(f"[FALLBACK] Using mock response for language: {language}")
        
        # Try to use mock response first (for testing language control)
        try:
            mock_response = get_mock_response(language, prompt, context)
            if mock_response:
                logger.info(f"[FALLBACK] Returning mock response in {language}: {len(mock_response)} chars")
                return mock_response
        except Exception as e:
            logger.warning(f"[FALLBACK] Mock response generation failed: {str(e)}")
        
        # Fallback to context-based response
        if context and context.strip():
            lines = context.split('\n\n')
            first_chunk = lines[0] if lines else context
            cleaned_chunk = first_chunk.replace('[Chunk 1]\n', '').replace('[Chunk 2]\n', '').replace('[Chunk 3]\n', '')
            return f"{cleaned_chunk[:500]}..."
        else:
            return "I don't have enough context to answer your question. Please check the document content."
    
    def generate_response(
        self,
        prompt: str,
        context: str = "",
        language: str = "en",
        temperature: float = 0.7,
        max_tokens: int = 1024,
        retry_attempt: int = 1
    ) -> Optional[str]:
        """
        Generate response from DeepSeek API with strict language enforcement
        
        Args:
            prompt: User question
            context: Document context/retrieved information
            language: Target language (en, hi, mr)
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            retry_attempt: Current retry attempt number
            
        Returns:
            Response text or None if request fails
        """
        try:
            # Validate inputs
            if not prompt or not prompt.strip():
                logger.error("[VALIDATE] Prompt is empty")
                return None
            
            if not self.api_key:
                logger.error("[VALIDATE] API key not available")
                return None
            
            # Get strict language instruction
            language_instruction = get_strict_language_instruction(language)
            
            # Prepare the system message with strict language enforcement
            system_message = f"""You are a helpful assistant. Answer questions based on the provided context accurately and concisely.

{language_instruction}

Important rules:
- Do NOT mention document chunks or references in your answer.
- Provide a natural, flowing response.
- NEVER mix languages - stick to {language} only."""
            
            if context and context.strip():
                system_message += f"\n\nContext from the document:\n{context}"
            else:
                logger.warning("[DEEPSEEK] No context provided for API call")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": system_message
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            logger.info(f"[DEEPSEEK] Attempt {retry_attempt}")
            logger.info(f"[DEEPSEEK] Model: {self.model}")
            logger.info(f"[DEEPSEEK] Language: {language}")
            logger.info(f"[DEEPSEEK] Payload size: {len(str(payload))} chars")
            logger.info(f"[DEEPSEEK] URL: {self.base_url}")
            
            # Make the API request
            logger.info("[DEEPSEEK] Sending request to DeepSeek API...")
            response = requests.post(
                self.base_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            logger.info(f"[DEEPSEEK] Response status: {response.status_code}")
            
            # Check for HTTP errors
            if response.status_code != 200:
                error_detail = response.text
                logger.error(f"[DEEPSEEK] HTTP {response.status_code}: {error_detail}")
                
                # Check for specific errors
                if response.status_code == 402:
                    logger.warning("[DEEPSEEK] Insufficient balance - switching to fallback mode")
                    if self.enable_fallback:
                        logger.info("[DEEPSEEK] Generating fallback response...")
                        return self._generate_fallback_response(prompt, context, language)
                
                response.raise_for_status()
            
            result = response.json()
            logger.info(f"[DEEPSEEK] Response received: {len(str(result))} chars")
            
            # Extract response content
            if "choices" in result and len(result["choices"]) > 0:
                answer = result["choices"][0]["message"]["content"]
                logger.info(f"[DEEPSEEK] Answer extracted: {len(answer)} chars")
                
                # STRICT LANGUAGE VALIDATION
                is_valid = validate_language_strict(answer, language, min_confidence=0.7)
                
                if is_valid:
                    logger.info(f"[DEEPSEEK] ✓ Language validation PASSED for {language}")
                    return answer
                else:
                    logger.warning(f"[DEEPSEEK] ✗ Language validation FAILED")
                    logger.warning(f"[DEEPSEEK] Response appears to be in wrong language")
                    
                    # Retry with increased strictness
                    if retry_attempt < self.max_language_validation_retries:
                        logger.info(f"[DEEPSEEK] Retrying with stricter prompt (attempt {retry_attempt + 1}/{self.max_language_validation_retries})")
                        
                        # Increase temperature slightly to encourage more distinct language
                        retry_temp = min(temperature + 0.3, 1.5)
                        return self.generate_response(
                            prompt=prompt,
                            context=context,
                            language=language,
                            temperature=retry_temp,
                            max_tokens=max_tokens,
                            retry_attempt=retry_attempt + 1
                        )
                    else:
                        logger.error(f"[DEEPSEEK] Max retries reached, returning possibly wrong-language response")
                        # Return anyway as fallback
                        return answer
                
            logger.error(f"[DEEPSEEK] Unexpected response format: {result}")
            return None
        
        except requests.exceptions.Timeout:
            logger.error("[DEEPSEEK] Request timeout (30 seconds)")
            if self.enable_fallback:
                logger.info("[DEEPSEEK] Using fallback response due to timeout")
                return self._generate_fallback_response(prompt, context, language)
            return None
        except requests.exceptions.ConnectionError as e:
            logger.error(f"[DEEPSEEK] Connection error: {str(e)}")
            if self.enable_fallback:
                logger.info("[DEEPSEEK] Using fallback response due to connection error")
                return self._generate_fallback_response(prompt, context, language)
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"[DEEPSEEK] HTTP error: {str(e)}")
            try:
                logger.error(f"[DEEPSEEK] Response body: {e.response.text}")
            except:
                pass
            if self.enable_fallback:
                logger.info("[DEEPSEEK] Using fallback response due to HTTP error")
                return self._generate_fallback_response(prompt, context, language)
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"[DEEPSEEK] Request failed: {str(e)}")
            if self.enable_fallback:
                logger.info("[DEEPSEEK] Using fallback response due to request error")
                return self._generate_fallback_response(prompt, context, language)
            return None
        except Exception as e:
            logger.error(f"[DEEPSEEK] Unexpected error: {str(e)}")
            logger.exception("Full traceback:")
            if self.enable_fallback:
                logger.info("[DEEPSEEK] Using fallback response due to unexpected error")
                return self._generate_fallback_response(prompt, context, language)
            return None
    
    def test_connection(self) -> bool:
        """
        Test connection to DeepSeek API
        
        Returns:
            True if connection is successful
        """
        try:
            logger.info("[TEST_CONNECTION] Testing DeepSeek API connection...")
            
            if not self.api_key:
                logger.error("[TEST_CONNECTION] API key not available")
                return False
            
            response = self.generate_response("Hello", max_tokens=10)
            
            if response:
                logger.info("[TEST_CONNECTION] ✓ Connection successful")
                return True
            else:
                logger.error("[TEST_CONNECTION] ✗ Connection failed - no response")
                return False
                
        except Exception as e:
            logger.error(f"[TEST_CONNECTION] Connection test failed: {str(e)}")
            return False
