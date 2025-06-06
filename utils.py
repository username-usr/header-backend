import os
import httpx
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# Validate API key
if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY environment variable is not set")


HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "",
    "X-Title": "Excel AI App"
}


async def call_ai_cellmap(prompt: str, model: str) -> dict:
    system_msg = (
        "You are a spreadsheet assistant. Output only a JSON object where keys are cell coordinates "
        "(like c1r1 for column 1 row 1), and values are cell contents. "
        "Example: {\"c1r1\": \"Math\", \"c1r2\": \"Science\"}. "
        "Do not include explanations or markdown formatting. Just valid JSON."
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient() as client:
        try:
            print(f"Sending request to OpenRouter with prompt: {prompt}, model: {model}")
            res = await client.post(BASE_URL, json=payload, headers=HEADERS, timeout=30.0)
            
            # Check for 401 Unauthorized explicitly
            if res.status_code == 401:
                raise Exception("OpenRouter API authentication failed: Invalid or missing API key")
            
            res.raise_for_status()  # Raises for 4xx/5xx errors

            # Extract the content
            response_json = res.json()
            content = response_json["choices"][0]["message"]["content"].strip()

            print("🧠 AI raw response:", content)

            # Clean markdown wrapping if any
            if content.startswith("```json"):
                content = content.removeprefix("```json").strip()
            if content.startswith("```"):
                content = content.removeprefix("```").strip()
            if content.endswith("```"):
                content = content.removesuffix("```").strip()

            # Handle empty or invalid response
            if not content:
                raise ValueError("AI returned empty response.")

            # Try parsing JSON
            try:
                parsed = json.loads(content)
                if not isinstance(parsed, dict):
                    raise ValueError("AI response is not a valid cell map (not a JSON object).")
                return parsed
            except json.JSONDecodeError as e:
                print("❌ JSON decode error:", str(e))
                print("🔍 Content that failed to decode:", content)
                raise ValueError("AI response is not valid JSON.")

        except httpx.RequestError as e:
            print("❌ Network Error:", str(e))
            raise Exception(f"Network error contacting OpenRouter: {str(e)}")
        except Exception as e:
            print("❌ Final Error:", str(e))
            raise Exception(f"Failed to get usable data from OpenRouter: {str(e)}")