from datetime import datetime
import sqlite3
import json


def setup(import_data = False):

    # Connect or create the database
    conn = sqlite3.connect('./data/trendman.db')
    # Create a cursor
    cursor = conn.cursor()

    # Create the "processed" table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed (
            url TEXT,
            first_source TEXT,
            language TEXT,
            date_created TEXT
        )
    ''')

    cursor.execute('''CREATE INDEX IF NOT EXISTS url 
                    ON processed(url);
    ''')

    conn.commit()

    if import_data:
        # read the data from data/processed-urls.json into array
        with open('./data/processed-urls.json') as f:
            data = json.load(f)

        for url in data:
        # insert data into table
            now = datetime.now()
            cursor.execute('''INSERT INTO processed(url, first_source, language, date_created)
                              VALUES(?, ?, ?, ?)''', (url, '', '', now))
                        



        # Commit the changes and close the connection
        conn.commit()
        conn.close()
