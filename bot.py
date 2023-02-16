import os
import json
import sqlite3
import time
import atexit
import requests

from dotenv   import load_dotenv
from datetime import datetime
from mastodon import get_all_data
from utils    import pp, array_from_file
from setup    import setup

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler

import caribou




def handle_exit():
    print("\n\n\n*** Received SIGHUP, closing database before exiting.")
    conn.close()
    print("Bye!")

def run_loop():
    sources         = array_from_file('./data/sources.json')
    ignored_domains = array_from_file('./data/ignore.json')
    sent_links      = 0

    for source in sources:
        print(f'\n\n*** Source: {source}')
        source_domain = source.split('/')[2]
        data = get_all_data(source, 20)

        print(f'Rows: {len(data)}')

        for row in data:
            url = row['url']
            url_domain = url.split('/')[2]
            url_domain = url_domain.replace('www.', '')

            # if url is in ignore.json
            if url_domain in ignored_domains:
                continue


            cursor.execute('''SELECT * FROM processed WHERE url = ?''', (url,))
            # if url is not in processed
            if cursor.fetchone() is None:
                sent_links += 1
                if sent_links > MAXLINKS:
                    break
                print(url)
                cursor.execute('''INSERT INTO processed(url, first_source, language, date_created)
                                VALUES(?, ?, ?, ?)''', (url, source_domain, '', datetime.now()))
                conn.commit()

                # send url to telegram
                # requests.get(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHATID}&text={url}')


def telegram_react(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    data = query.data
    message = query.message.text

    # Check which button was pressed
    if data == '👍':
        context.bot.send_message(chat_id=user.id, text=f"{user.username} liked the message: {message}")
    elif data == '👎':
        context.bot.send_message(chat_id=user.id, text=f"{user.username} disliked the message: {message}")


def setup_telegram(token):
    # Initialize the bot and add handlers
    updater = Update(token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(telegram_react))

    # Start the bot
    updater.start_polling()
    updater.idle()




# --------------------------





load_dotenv()
TOKEN    = os.getenv("TOKEN")
CHATID   = os.getenv("CHATID")
MAXLINKS = int(os.getenv("MAXLINKS"))
WAIT     = int(os.getenv("WAIT"))

setup_telegram(TOKEN)

atexit.register(handle_exit)

# check if data/trendman.db exists, if not call setup()
db_path = './data/trendman.db'
if not os.path.exists(db_path):
    print('Setting up database')
    setup( import_data = True )



migrations_path = './migrations'

# upgrade to most recent version
caribou.upgrade(db_path, migrations_path)

# upgrade to a specific version
caribou.upgrade(db_path, migrations_path)

# downgrade to a specific version
caribou.downgrade(db_path, migrations_path)

conn = sqlite3.connect('./data/trendman.db')
cursor = conn.cursor()



# run the loop infinitely, wait WAIT minutes between each run
while True:
    run_loop()
    print(f'\nWaiting {WAIT} minutes')
    time.sleep(WAIT * 60)


