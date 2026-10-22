
import traceback
from openai import OpenAI

try:
    client = OpenAI(
        api_key="test",
        base_url="https://api.groq.com/openai/v1",
        max_retries=0,
        timeout=10,
    )
    client.models.list()
except Exception:
    traceback.print_exc()
