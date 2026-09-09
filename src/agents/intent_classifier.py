from google import genai
from google.genai import types
from google.genai.errors import ServerError
import time

from src.config.settings import GOOGLE_API_KEY, GEMINI_MODEL
from src.models.intents import Intent
from src.models.classification import IntentResponse
from src.agents.prompts import INTENT_CLASSIFIER_PROMPT


class IntentClassifier:

    def __init__(self):
        self.client = genai.Client(api_key=GOOGLE_API_KEY)

    def classify(
        self,
        user_query: str,
        conversation_history: list[dict] | None = None,
    ) -> Intent:
        """
        Classify a user request using Gemini.

        Conversation history is provided only to help resolve
        follow-up references such as "them", "that one", or
        "the latest one". Employee identity is controlled by
        the application and must never be inferred from history.

        Retries automatically if Gemini is temporarily unavailable.
        """

        conversation_context = ""

        if conversation_history:
            conversation_context = "\n\nPrevious conversation:\n"

            for message in conversation_history:
                role = message.get("role", "unknown")
                content = message.get("content", "")

                conversation_context += (
                    f"{role.upper()}: {content}\n"
                )

        classifier_input = (
            conversation_context
            + "\n\nCURRENT USER REQUEST:\n"
            + user_query
        )

        retries = 3

        for attempt in range(retries):
            try:

                response = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=classifier_input,
                    config=types.GenerateContentConfig(
                        system_instruction=INTENT_CLASSIFIER_PROMPT,
                        response_mime_type="application/json",
                        response_schema=IntentResponse,
                        temperature=0,
                    ),
                )

                return response.parsed.intent

            except Exception as exc:

                if attempt == retries - 1:
                    raise exc

                print(
                    f"Gemini busy... retrying "
                    f"({attempt + 1}/{retries})"
                )
