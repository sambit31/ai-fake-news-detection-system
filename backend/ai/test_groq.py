
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Connect to Groq
client = Groq(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": "Reply with exactly: Groq connection successful!"
            }
        ],
        temperature=0
    )

    print("\n========== GROQ RESPONSE ==========")
    print(response.choices[0].message.content)
    print("\nGroq API connection successful!")

except Exception as e:
    print("\nGroq API connection failed:")
    print(str(e))
