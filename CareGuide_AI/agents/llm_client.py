from groq import Groq

from config.settings import GROQ_API_KEY, MODEL_NAME


client = Groq(api_key=GROQ_API_KEY)


def generate_response(system_prompt: str, user_prompt: str) -> str:
    """Generate a response with the configured Groq model."""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content or ""
