from typing import Optional
from app.core.config import settings
import os

class LLMEngine:
    """Abstraction over LLM providers.

    Supports 'openai' and 'local' providers (local is a placeholder).
    """

    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or settings.LLM_PROVIDER
        if self.provider == 'openai':
            try:
                import openai
                openai.api_key = os.getenv('OPENAI_API_KEY')
                self._client = openai
            except Exception:
                self._client = None
        else:
            # Local LLM placeholder
            self._client = None

    def build_prompt(self, question: str, context: str) -> str:
        """Construct a prompt that includes retrieved context."""
        prompt = (
            "You are an assistant that answers user questions based on provided context.\n"
            "Context:\n" + context + "\n\n" + "Question: " + question + "\nAnswer:"
        )
        return prompt

    def generate_answer(self, question: str, context: str) -> str:
        """Generate an answer using the selected provider.

        For `openai` uses ChatCompletion; for `local` returns a placeholder.
        """
        prompt = self.build_prompt(question, context)
        if self.provider == 'openai' and self._client is not None:
            try:
                resp = self._client.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                    n=1,
                    temperature=0.2,
                )
                return resp['choices'][0]['message']['content'].strip()
            except Exception as e:
                return f"[LLM error] {e}"
        else:
            # Local LLM placeholder (easy to replace with a real call)
            return "This is a placeholder answer from the local LLM. Replace with implementation."
