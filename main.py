from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


TOKEN: Final = '6800073194:AAEb3PrGZCQpeXRzoeOVINoyBVRZBhjpBLM'
BOT_USERNAME: Final = '@bot_impulse_bot'

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am awake.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('What do you require?')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom order!')


#Responses 

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'What do you require?'

    if 'how are you?' in processed:
        return 'I await orders.'

    if 'why is your name impulse?' in processed:
        return 'Why do you care?'

    if 'what can you do?' in processed:
        return 'Whatever the backend is capable of.'

    if 'what are my daily tasks?' in processed:
        return 'Leetcode. Course Study. Updating this bot. Gaining weight.'

    print('No matching condition found for text:', text)
    return 'I do not have to comprehend this absurd sentence.'

async def handle_message(update:Update, context:ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}:"{text}"')

    if message_type == 'supergroup':
        if '@bot_impulse_bot' in text:
            new_text: str = text.replace('@bot_impulse_bot', '').strip()
            response: str = handle_response(new_text)
    else:
        response: str = handle_response(text)
    
    print('Bot:',response)
    await update.message.reply_text(response)

async def error(update:Update, context:ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused errpr {context.error}')

if __name__ == '__main__':

    print('Whatever is the hurry...')
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('custom',custom_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    #Errors
    app.add_error_handler(error)

    #polls the bot
    print('Polling..')
    app.run_polling(poll_interval=3)

