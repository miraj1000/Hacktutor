# ============================================================
# HackTutor configuration
# API key কখনো source code বা GitHub-এ লিখবে না।
# Render-এর Environment Variables-এ GEMINI_API_KEY সেট করো।
# ============================================================

import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
