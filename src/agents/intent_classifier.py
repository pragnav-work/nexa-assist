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

    def classify(self, user_query: str) -> Intent:
        """
        Classify a user request using Gemini.
        Retries automatically if Gemini is temporarily unavailable.
        """

        retries = 3

        for attempt in range(retries):
            try:

                response = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=user_query,
                    config=types.GenerateContentConfig(
                        system_instruction=INTENT_CLASSIFIER_PROMPT,
                        response_mime_type="application/json",
                        response_schema=IntentResponse,
                        temperature=0,
                    ),
                )

                return response.parsed.intent

            except ServerError:

                if attempt < retries - 1:
                    print(f"Gemini busy... retrying ({attempt+1}/{retries})")
                    time.sleep(2)
                else:
                    return Intent.UNKNOWN

            except Exception as e:
                print(f"Intent classification failed: {e}")

                if attempt < retries - 1:
                    time.sleep(2)
                else:
                    return Intent.UNKNOWN