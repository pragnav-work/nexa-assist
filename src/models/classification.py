from pydantic import BaseModel
from src.models.intents import Intent


class IntentResponse(BaseModel):
    intent: Intent