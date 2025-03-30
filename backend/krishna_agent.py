from openai import OpenAI
from backend.gita_quotes import gita_verses
from backend.vector_store import recall_similar, store_memory
import random

# Together.ai OpenAI-compatible endpoint
client = OpenAI(
    api_key="cd16f2f3450f5a355254d0b09db4bf18cf2c554bfee1b065dabd8adb1f4cee3c",
    base_url="https://api.together.xyz/v1"
)

# Pick a relevant Gita verse
def get_gita_quote(topic):
    return random.choice(gita_verses.get(topic.lower(), []))

# Krishna response generator with memory
def get_krishna_response(user_input):
    topic = "dharma" if "dharma" in user_input.lower() else "karma"

    # Load system prompt
    with open("prompts/krishna_prompt.txt") as f:
        krishna_prompt = f.read()

    # Recall memory from ChromaDB
    past_memories = recall_similar(user_input)
    memory_context = "\n---\n".join(past_memories)

    # Inject memory into context
    user_prompt = f"""
Relevant past memories:
{memory_context}

Now respond to the user's question:
{user_input}
""".strip()

    # LLM call
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

    # Store memory
    store_memory(user_input, answer)

    return f"{answer}\n\n📜 *Bhagavad Gita says:* {verse}" if verse else answer
