"""
Gemini Service - Integration with Google Gemini API for LLM responses
"""
import google.genai as genai
import logging
from typing import Optional
import os

logger = logging.getLogger(__name__)


class GeminiService:
    """Handles communication with Google Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini service
        
        Args:
            api_key: Google Gemini API key (if not provided, uses env variable)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not provided or set in environment")
        
        # Configure the API
        self.client = genai.Client(api_key=self.api_key)
        
        logger.info("Gemini service initialized successfully")
    
    def generate_response(
        self,
        prompt: str,
        context: str = "",
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> Optional[str]:
        """
        Generate response from Gemini API
        
        Args:
            prompt: User question
            context: Document context/retrieved information
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            Response text or None if request fails
        """
        try:
            # Prepare the system message with context
            system_message = "You are a helpful assistant that answers questions based on provided documents. Answer accurately, concisely, and only using information from the provided context. If the answer is not in the context, say 'I cannot find this information in the provided document.'"
            
            if context:
                full_prompt = f"""{system_message}

Context from the document:
{context}

User Question: {prompt}

Please provide a clear and accurate answer based only on the provided context."""
            else:
                full_prompt = f"""{system_message}

User Question: {prompt}"""
            
            logger.info(f"Sending request to Gemini API with prompt length: {len(full_prompt)} chars")
            
            # Generate response using the new API
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                    top_p=0.9,
                )
            )
            
            if response.text:
                logger.info(f"Received response from Gemini API: {len(response.text)} chars")
                return response.text
            
            # Check if there are candidates with content
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                if candidate.content and hasattr(candidate.content, 'parts') and candidate.content.parts:
                    part = candidate.content.parts[0]
                    if hasattr(part, 'text') and part.text:
                        logger.info(f"Received response from Gemini API: {len(part.text)} chars")
                        return part.text
            
            logger.error(f"Unexpected Gemini response format - no text found")
            return None
        
        except Exception as e:
            logger.error(f"Gemini API request failed: {type(e).__name__}: {str(e)}")
            return None
    
    def test_connection(self) -> bool:
        """
        Test connection to Gemini API
        
        Returns:
            True if connection is successful
        """
        try:
            logger.info("Testing Gemini API connection...")
            response = self.generate_response("Hi", max_tokens=100)
            if response is not None:
                logger.info("Gemini API connection test successful")
                return True
            else:
                logger.error("Gemini API connection test failed - no response received")
                return False
        except Exception as e:
            logger.error(f"Gemini API connection test failed: {type(e).__name__}: {str(e)}")
            return False
