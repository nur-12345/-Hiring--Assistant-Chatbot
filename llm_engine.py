from groq import Groq
from config import GROK_API_KEY

client = Groq(api_key=GROK_API_KEY)

def call_llm(system_prompt, user_prompt, temperature=0.3):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"LLM Error: {str(e)}"
