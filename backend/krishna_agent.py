from openai import OpenAI
import os
from backend.vector_store import recall_similar, store_memory
from backend.gita_quotes import gita_verses
import random

# ✅ Use TogetherAI for chat
client = OpenAI(
    api_key=os.getenv("TOGETHER_API_KEY"),
    base_url="https://api.together.xyz/v1"
)

def get_gita_quote(topic):
    return random.choice(gita_verses.get(topic.lower(), []))

def get_krishna_response(user_input):
    topic = "dharma" if "dharma" in user_input.lower() else "karma"

    with open("prompts/krishna_prompt.txt") as f:
        krishna_prompt = f.read()

    past_memories = recall_similar(user_input)
    memory_context = "\n---\n".join(past_memories)

    user_prompt = f"""
Relevant past memories:
{memory_context}

Now respond to the user's question:
{user_input}
""".strip()

    response = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[
            {"role": "system", "content": krishna_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=512
    )

    answer = response.choices[0].message.content.strip()
    verse = get_gita_quote(topic)
    store_memory(user_input, answer)

    return f"{answer}\n\n📜 *Bhagavad Gita says:* {verse}" if verse else answer
