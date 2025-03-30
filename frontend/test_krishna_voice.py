from elevenlabs.client import ElevenLabs
import os

# Either use .env or hardcode for testing
api_key = os.getenv("ELEVEN_API_KEY") or "sk_8faf737018fc9ec4c75146d9acdbb7fa14805d4773a292b2"

client = ElevenLabs(api_key=api_key)

# Generate audio stream
stream = client.generate(
    text="I am Lord Krishna. Follow your dharma with detachment.",
    voice="Arnold",  # Try "Adam" or "Antoni" too
    model="eleven_monolingual_v1",
    stream=True  # <-- Important!
)

# Save stream to file
with open("krishna_voice.mp3", "wb") as f:
    for chunk in stream:
        f.write(chunk)

print("✅ Voice file saved as krishna_voice.mp3")
