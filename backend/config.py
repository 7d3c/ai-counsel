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
# Claude: claude-3-5-sonnet, claude-3-opus, claude-3-sonnet, claude-3-haiku
# Gemini: gemini-1.5-flash, gemini-1.5-pro, gemini-2.0-flash
# OpenAI: gpt-4o, gpt-4o-mini, o1, o1-mini, o3-mini
# Grok: grok-beta, grok-2-1212
COUNCIL_MODELS = [
    "gpt-4o",
    "gemini-1.5-flash",
    "claude-3-5-sonnet",
    "grok-beta",
]

# Chairman model - synthesizes final response
# Can be any model from the list above
CHAIRMAN_MODEL = "gemini-1.5-flash"

# Data directory for conversation storage
DATA_DIR = "data/conversations"
