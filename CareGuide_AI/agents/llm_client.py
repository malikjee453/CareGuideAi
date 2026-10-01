from groq import Groq
from config.settings import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)


def generate_response(system_prompt, user_prompt):

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": "Say hello"
            }
        ],
    )

    return response.choices[0].message.content
