from groq import Groq
from config.settings import GROQ_API_KEY

MODEL_NAME = "openai/gpt-oss-120b"

client = Groq(api_key=GROQ_API_KEY)


def generate_response(system_prompt: str, user_prompt: str) -> str:
    """Generate a response using the configured Groq model."""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content

    if not content or not content.strip():
        raise RuntimeError("The language model returned an empty response.")

    return content.strip()
