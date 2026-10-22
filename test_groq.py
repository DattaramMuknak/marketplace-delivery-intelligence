
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

api_key = os.getenv("GROQ_API_KEY", "").strip()

try:
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        timeout=30.0,
        max_retries=0,
    )

    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
        messages=[
            {"role": "user", "content": "Reply: Connection successful"}
        ],
        max_tokens=30,
    )

    print("SUCCESS:", response.choices[0].message.content)

except Exception as e:
    print("Error type:", type(e).__name__)
    print("Error details:", str(e))
    print("Underlying cause:", repr(e.__cause__))
    print("Context:", repr(e.__context__))
