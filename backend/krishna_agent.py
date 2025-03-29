from openai import OpenAI
from backend.gita_quotes import gita_verses
import random

client = OpenAI(
    api_key="cd16f2f3450f5a355254d0b09db4bf18cf2c554bfee1b065dabd8adb1f4cee3c",
    base_url="https://api.together.xyz/v1"
)

def get_gita_quote(topic):
    return random.choice(gita_verses.get(topic.lower(), []))

def get_krishna_response(user_input):
    topic = "dharma" if "dharma" in user_input.lower() else "karma"

    with open("prompts/krishna_prompt.txt") as f:
        krishna_prompt = f.read()

    response = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[
            {"role": "system", "content": krishna_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
        max_tokens=512
    )
    answer = response.choices[0].message.content
    verse = get_gita_quote(topic)
    return f"{answer}\n\n📜 *Bhagavad Gita says:* {verse}" if verse else answer
