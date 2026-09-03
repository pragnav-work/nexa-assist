"""
Application configuration for NexaAssist.

This module loads environment variables and exposes
application-wide configuration values.
"""

import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found. "
        "Please create a .env file and add your Gemini API key."
    )

# Gemini model to be used across the application
GEMINI_MODEL = "gemini-2.5-flash"