import os
import anthropic
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class LLMEngine:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        self.client = anthropic.Anthropic(api_key=api_key)

    def generate_response(self, user_input, intent=None, context=None):

        # Optional memory/context support
        system_prompt = "You are a smart, concise assistant.Do not repeat the user's message.Give clear and short responses.If a reminder is confirmed, respond naturally"

        if context:
            system_prompt += f"\nHere is previous context:\n{context}"

        response = self.client.messages.create(
            model="claude-3-haiku-20240307",  # Fast + cheaper model
            max_tokens=300,
            temperature=0.5,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        return response.content[0].text.strip()