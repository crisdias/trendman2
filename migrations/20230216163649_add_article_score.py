"""
This module contains a Caribou migration.

Migration Name: add_article_score 
Migration Version: 20230216163649
"""

def upgrade(connection):
    # add your upgrade step here
    cursor = connection.cursor()

    # Create the "processed" table
    cursor.execute('''
        ALTER TABLE processed ADD COLUMN score INTEGER DEFAULT NULL;
    ''')
    pass

def downgrade(connection):
    # add your downgrade step here
    cursor = connection.cursor()

    # Create the "processed" table
    cursor.execute('''
        ALTER TABLE processed DROP COLUMN score;
    ''')
    pass
