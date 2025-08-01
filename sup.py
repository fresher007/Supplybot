import os
import threading
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask

# Retrieve the bot API token from an environment variable for security
BOT_TOKEN = os.environ.get("BOT_TOKEN")
# Replace with your bot's username
BOT_USERNAME = "Suppllyubot"

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

# Flask server to run in a background thread
def run_flask_server():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "Bot is running!"

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# Main function to set up and run the bot
if __name__ == "__main__":
    print("Starting bot...")

    if not BOT_TOKEN:
        raise ValueError("The BOT_TOKEN environment variable is not set. Please set it before running the bot.")

    # Start the Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask_server)
    flask_thread.start()

    # Create the Application and pass your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register the handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    
    # Start the bot's polling loop in the main thread
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)