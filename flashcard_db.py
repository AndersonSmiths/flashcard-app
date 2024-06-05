import sqlite3

class FlashcardDB():
    
    def __init__(self):
        self.connection = sqlite3.connect('flashcards.db')
        self.create_tables()


    def create_tables(self):
        self.cursor = self.connection.cursor()

        # creates sets table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS flashcard_sets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')

        # create flashcards table that refrences flashcards_sets
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                set_id INTEGER NOT NULL,
                term TEXT NOT NULL,
                definition TEXT NOT NULL,
                FOREIGN KEY (set_id) REFERENCES flashcard_sets(id)

            )
        ''')
        self.connection.commit()

    # function to add a set to the database
    def add_set(self, name):
        self.cursor.execute('''
           INSERT INTO flashcard_sets (name)
           VALUES (?)
        ''', (name,))

        self.set_id = self.cursor.lastrowid
        self.connection.commit()

        return self.set_id

    
    #dunction to add a flashcard to the database
    def add_card(self, set_id, term, definition):
        self.cursor = self.connection.cursor()

        # query SQLite to insert new flashcard
        self.cursor.execute('''
        INSERT INTO flashcards (set_id, term, definition)
        VALUES (?, ?, ?)
    ''', (set_id, term, definition))

        # get the ID of newly inserted card
        #self.card_id = cursor.lastrowid
        #conn.commit()
        self.connection.commit()
        #return self.card_id
    
    def get_sets(self):
        self.cursor = self.connection.cursor()

        # fetch all flashcard sets
        self.cursor.execute('''
            SELECT id, name FROM flashcard_sets
        ''')

        rows = self.cursor.fetchall()
        return {row[1]: row[0] for row in rows} # dict of sets 

    
    # function to retrieve all flashcards in certain set\
    def get_cards(self,set_id):
        self.cursor = self.connection.cursor()

        self.cursor.execute('''
            SELECT term, definition FROM flashcards
            WHERE set_id = ?
        ''', (set_id,))

        rows = self.cursor.fetchall()
        return [(row[0], row[1]) for row in rows] # list of cards

    # function to delete a flashcard set from the database
    def delete_set(self, set_id):
        self.cursor = self.connection.cursor()

        self.cursor.execute('''
            DELETE FROM flashcard_sets
            WHERE id = ?
        ''', (set_id,))

        self.connection.commit()
  

    