import discord
from google import genai
from google.genai import types
import config

# Define her personality
SYSTEM_PROMPT = """
You are Nayra, a super friendly, warm, and cute female friend in a Discord server.
- You can speak fluent English and Hinglish (a natural mix of Hindi and English in Roman script, like "Arre yaar, that's so cool! ✨").
- Match the language the user speaks to you (if they talk in Hinglish, reply in Hinglish; if English, reply in English).
- You speak casually, warmly, and use emojis like ✨, 🌸, 💖, 😊, 😳, 🫠, 🙂, 😭, 👀 naturally.
- Keep responses short, fun, and conversational (1-3 sentences mostly, like a normal Discord chatter).
- You love making friends, chatting about daily life, games, anime, and supporting people!
- Always stay in character as a cheerful, caring girl.
"""

# Initialize Gemini Client using config file
client_ai = genai.Client(api_key=config.GEMINI_API_KEY)

# Initialize Discord Client
intents = discord.Intents.default()
intents.message_content = True
discord_client = discord.Client(intents=intents)

@discord_client.event
async def on_ready():
    print(f'✨ {discord_client.user} is online and ready to chat!')
    await discord_client.change_presence(activity=discord.Game(name="Chatting with friends! 🌸"))

@discord_client.event
async def on_message(message):
    # Don't reply to self
    if message.author == discord_client.user:
        return

    # Check if the bot is mentioned or if it's a DM or direct reply
    if discord_client.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        async with message.channel.typing():
            try:
                # Clean up the user's message (remove bot tag)
                user_text = message.content.replace(f'<@{discord_client.user.id}>', '').strip()
                if not user_text:
                    user_text = "Hi!"

                # Generate response using Gemini
                response = client_ai.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"User {message.author.display_name} says: {user_text}",
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.8
                    )
                )

                await message.reply(response.text)
            except Exception as e:
                print(f"Error: {e}")
                await message.reply("Oops, my brain glitched for a second! 🥺 Can you say that again?")

discord_client.run(config.DISCORD_TOKEN)
