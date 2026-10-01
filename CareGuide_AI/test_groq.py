from groq import Groq

client = Groq(
    api_key="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"
)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "Explain hypertension in one sentence."
        }
    ]
)

print(response.choices[0].message.content)
