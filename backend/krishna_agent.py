import os
import random
import sys

from openai import OpenAI
from backend.gita_quotes import gita_verses

# Load vector memory functions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.vector_store import recall_similar, store_memory

# Together.ai client using OpenAI-compatible API
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.together.xyz/v1"
)

# Pick a Gita quote for the topic
def get_gita_quote(topic):
    return random.choice(gita_verses.get(topic.lower(), []))

# Krishna response generator with memory + Gita wisdom
def get_krishna_response(user_input):
    topic = "dharma" if "dharma" in user_input.lower() else "karma"

    # Load Krishna’s system prompt
    with open("prompts/krishna_prompt.txt") as f:
        krishna_prompt = f.read()

    # 🧠 Recall memory using FAISS
    past_memories = recall_similar(user_input)
    memory_context = "\n---\n".join(past_memories)

    # Create contextual prompt with memory
    user_prompt = f"""
Relevant past memories:
{memory_context}

Now respond to the user's question:
{user_input}
""".strip()

    # 🧠 Call Together AI (Mixtral model)
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

    # 🔒 Store current Q&A to FAISS memory
    store_memory(user_input, answer)

    return f"{answer}\n\n📜 *Bhagavad Gita says:* {verse}" if verse else answer
