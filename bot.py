import os
import telegram
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import psycopg2

stupid_button = KeyboardButton('stupid')
fat_button = KeyboardButton('fat')
dumb_button = KeyboardButton('dumb')

keyboard = ReplyKeyboardMarkup([[stupid_button], [fat_button], [dumb_button]], resize_keyboard=True)

conn = psycopg2.connect(database="mydatabase", user="myusername", password="mypassword", host="localhost", port="5432")
cur = conn.cursor()

# Define the table
cur.execute('''CREATE TABLE user_calls
               (user_id INT PRIMARY KEY     NOT NULL,
                stupid_calls INT,
                fat_calls INT,
                dumb_calls INT);''')
conn.commit()

#  callback handler
def button_click_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    button_text = query.data

    cur.execute(f"UPDATE user_calls SET {button_text}_calls = {button_text}_calls + 1 WHERE user_id = {user_id}")
    conn.commit()

    if button_text == 'stupid':
        query.answer('look in a mirror')
    elif button_text == 'fat':
        query.answer('oh yes u are! Absolutely')
    elif button_text == 'dumb':
        query.answer('Meh! kind of self explanatory. u wont get it though...')

def main():
    updater = Updater(token=os.environ['TELEGRAM_BOT_TOKEN'], use_context=True)
    dispatcher = updater.dispatcher

    # command handlers
    def start_command_handler(update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        context.bot.send_message(chat_id=user_id, text='Welcome to Jester! Please accept one punishment lol', reply_markup=keyboard)

    start_handler = CommandHandler('start', start_command_handler)
    dispatcher.add_handler(start_handler)

    button_click_callback_handler = CallbackQueryHandler(button_click_handler)
    dispatcher.add_handler(button_click_callback_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
