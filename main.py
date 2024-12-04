import os
import requests
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes



TOKEN: Final = '6800073194:AAEb3PrGZCQpeXRzoeOVINoyBVRZBhjpBLM'
BOT_USERNAME: Final = '@bot_impulse_bot'

LEETCODE_API_ENDPOINT = 'https://leetcode.com/graphql'
DAILY_CODING_CHALLENGE_QUERY = '''
query questionOfToday {
    activeDailyCodingChallengeQuestion {
        date
        userStatus
        link
        question {
			title
			title
			titleSlug
			hasVideoSolution
			hasSolution
			topicTags {
				name
				id
				slug
			}
            title
			titleSlug
			hasVideoSolution
			hasSolution
			topicTags {
				name
				id
				slug
			}
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
        response = await leetcode_command(update, context)
        return
    else:
        response = 'I do not comprehend this absurd sentence.'

    await update.message.reply_text(response)


# Error Handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('leetcode', leetcode_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error_handler)

    print('Polling...')
    app.run_polling(poll_interval=3)
