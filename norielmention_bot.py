from http.client import responses
from typing import Final, Set
from telegram import Update
from telegram.ext import Application, CommandHandler, filters, ContextTypes, MessageHandler
from telegram.constants import ParseMode

TOKEN = 'TOKEN HERE'
BOT_USERNAME: Final = '@norielmention_bot'
MENTIONED_USERNAMES: Final = ['']


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("HELLO! Use the '@norielmention_bot' to mention everyone in this Group Chat.")

# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text


    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type in ['group', 'supergroup']:
        if BOT_USERNAME in text:
            mentions = [f"{username}" for username in MENTIONED_USERNAMES]
            response = "\n".join(mentions) + "\n\nRead the announcement from this message. Thank you!\n\n"
            await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
        else:
            return  # Do not respond if bot is not mentioned
    else:  # For private chats
        response: str = handle_response(text)
        print('Bot:', response)
        await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Errors
    app.add_error_handler(error)

    # Poll the bot
    print('Polling...')
    app.run_polling(poll_interval=3)
