"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys for different providers
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")

# Council members - list of model identifiers
# Available models:
# Claude: claude-sonnet-4.5, claude-sonnet-4, claude-opus-4
# Gemini: gemini-2.0-flash, gemini-2.5-flash, gemini-3-pro
# OpenAI: gpt-4o, gpt-4o-mini, gpt-5.1, o1, o1-mini
# Grok: grok-beta, grok-4
COUNCIL_MODELS = [
    "gpt-4o",
    "gemini-2.0-flash",
    "claude-sonnet-4.5",
    "grok-beta",
]

# Chairman model - synthesizes final response
# Can be any model from the list above
CHAIRMAN_MODEL = "gemini-2.0-flash"

# Data directory for conversation storage
DATA_DIR = "data/conversations"
