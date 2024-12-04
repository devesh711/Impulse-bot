import os
import threading
import requests
from typing import Final
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Telegram Bot Token and Configuration
TOKEN: Final = '6800073194:AAEb3PrGZCQpeXRzoeOVINoyBVRZBhjpBLM'
BOT_USERNAME: Final = '@bot_impulse_bot'

# LeetCode API Configuration
LEETCODE_API_ENDPOINT = 'https://leetcode.com/graphql'
DAILY_CODING_CHALLENGE_QUERY = '''
query questionOfToday {
    activeDailyCodingChallengeQuestion {
        date
        userStatus
        link
        question {
            title
            titleSlug
        }
    }
}'''


def fetch_daily_coding_challenge():
    print('Fetching daily coding challenge from LeetCode API.')
    try:
        response = requests.post(
            LEETCODE_API_ENDPOINT,
            json={'query': DAILY_CODING_CHALLENGE_QUERY},
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error fetching LeetCode challenge: {e}')
        return None


# Command Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am awake.')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('What do you require?')


async def leetcode_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response_json = fetch_daily_coding_challenge()
    if response_json:
        challenge_info = response_json.get('data', {}).get('activeDailyCodingChallengeQuestion', {})
        if challenge_info:
            date = challenge_info.get('date')
            link = challenge_info.get('link')
            title = challenge_info.get('question', {}).get('title', 'No Title')

            response_text = f"Today's LeetCode Challenge ({date}):\n\nTitle: {title}\nLink: https://leetcode.com{link}"
        else:
            response_text = 'No LeetCode challenge available today.'
    else:
        response_text = 'Error fetching LeetCode challenge.'

    await update.message.reply_text(response_text)


# Message Handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text.lower()

    if 'hello' in text:
        response = 'Hello! What do you require?'
    elif 'leetcode' in text:
        await leetcode_command(update, context)
        return
    else:
        response = 'I do not comprehend this absurd sentence.'

    await update.message.reply_text(response)


# Error Handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Flask App for Health Check
health_app = Flask(__name__)

@health_app.route('/')
def health_check():
    return "Bot is alive and healthy!", 200


# Run Flask server in a separate thread
def run_flask():
    health_app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    print('Starting bot...')

    # Start Flask in a separate thread for health checks
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Initialize the Telegram bot
    app = Application.builder().token(TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('leetcode', leetcode_command))

    # Message Handlers
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error Handler
    app.add_error_handler(error_handler)

    # Polling
    print('Polling...')
    app.run_polling(poll_interval=3)
