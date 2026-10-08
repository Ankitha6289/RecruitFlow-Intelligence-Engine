# Test available models
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from config import Config
from groq import Groq

client = Groq(api_key=Config.GROQ_API_KEY)

# Try the models listed above
for model_id in [
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "qwen/qwen3.8-27b",
    "allam-2-7b",
]:
    try:
        resp = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": "Say exactly: chatbot_ok"}],
            max_tokens=10,
        )
        print(f"[WORKS] {model_id} -> {resp.choices[0].message.content!r}")
    except Exception as e:
        msg = str(e)[:120]
        print(f"[FAIL]  {model_id}: {msg}")
