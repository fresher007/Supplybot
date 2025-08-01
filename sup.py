import os
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Retrieve the bot API token from an environment variable for security
BOT_TOKEN = os.environ.get("BOT_TOKEN")
# Replace with your bot's username
BOT_USERNAME = "YourBotUsername"

# Function to handle the /start command from a user
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # The payload is the text after the /start command, which should be the file_id
    payload = context.args[0] if context.args else None
    
    if payload:
        # If a file_id is in the payload, send the video to the user
        try:
            await update.message.reply_video(payload)
        except telegram.error.BadRequest:
            # Handle cases where the file_id is invalid or no longer available
            await update.message.reply_text("I couldn't find that video. Please check the link or try again.")
    else:
        # If no payload, it's a regular /start command
        await update.message.reply_text("Hello! To share a video, just send it to me. To retrieve a video, use the link I provide.")

# Function to handle video messages sent to the bot
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extract the file_id from the video message
    file_id = update.message.video.file_id
    
    # Create the deep link with the file_id
    deep_link = f"https://t.me/{BOT_USERNAME}?start={file_id}"
    
    # Reply to the sender with the file_id and the deep link
    response_text = (
        f"Here is your video's file ID:\n\n`{file_id}`\n\n"
        f"Use this link to share it with others:\n\n`{deep_link}`"
    )
    
    await update.message.reply_text(response_text)

# Main function to set up and run the bot
def main():
    print("Starting bot...")
    
    # Ensure the bot token is available
    if not BOT_TOKEN:
        raise ValueError("The BOT_TOKEN environment variable is not set. Please set it before running the bot.")
    
    # Create the Application and pass your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register the handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    
    # Start the bot
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()