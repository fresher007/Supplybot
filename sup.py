import os
import threading
import asyncio
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask

# Retrieve the bot API token from an environment variable for security
BOT_TOKEN = os.environ.get("BOT_TOKEN")
# Replace with your bot's username
BOT_USERNAME = "Supplybot"

# Function to handle the /start command from a user
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payload = context.args[0] if context.args else None
    
    if payload:
        try:
            await update.message.reply_video(payload)
        except telegram.error.BadRequest:
            await update.message.reply_text("I couldn't find that video. Please check the link or try again.")
    else:
        await update.message.reply_text("Hello! To share a video, just send it to me. To retrieve a video, use the link I provide.")

# Function to handle video messages sent to the bot
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.video.file_id
    deep_link = f"https://t.me/{BOT_USERNAME}?start={file_id}"
    response_text = (
        f"Here is your video's file ID:\n\n`{file_id}`\n\n"
        f"Use this link to share it with others:\n\n`{deep_link}`"
    )
    await update.message.reply_text(response_text)

# Main function to set up and run the bot
def run_bot():
    print("Starting bot...")
    if not BOT_TOKEN:
        raise ValueError("The BOT_TOKEN environment variable is not set. Please set it before running the bot.")

    # Manually create a new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    
    print("Bot is running...")
    # The run_polling method needs to be run in the new event loop
    loop.run_until_complete(application.run_polling(allowed_updates=Update.ALL_TYPES))

if __name__ == "__main__":
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "Bot is running!"

    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)