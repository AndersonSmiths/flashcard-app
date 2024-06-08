import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from flashcard_db import FlashcardDB

class FlashcardApp():
    """
    A flashcard application that helps the user
    memorize terms and definitions via spaced repition

    Attributes
        root: a tkinter root
    """
    def __init__(self, root):

        # setting up database
        self.db = FlashcardDB()

        self.root = root

        # creating main window 
        self.root.title("Flashcard App")
        self.root.geometry('500x400')

        # create variables
        self.create_variables()

        # create notebook/tabs + buttons
        self.generate_notebook() # self initializes notebook
        self.set_tab()
        self.study_tab()


        # style/color
        #TODO

    def create_variables(self):
        self.set_name = tk.StringVar()
        self.term = tk.StringVar()
        self.definition = tk.StringVar()
        self.card_index = 0
        self.current_tabs = []


    def generate_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        
        # sets frame
        self.generate_set_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.generate_set_frame, text='Create Set')

        # entry widgets
        ttk.Label(self.generate_set_frame, text='Set Name: ').pack(padx=5, pady=5)
        ttk.Entry(self.generate_set_frame, textvariable=self.set_name, width=30).pack(padx=5, pady=5)

        ttk.Label(self.generate_set_frame, text='Term: ').pack(padx=5, pady=5)
        ttk.Entry(self.generate_set_frame, textvariable=self.term, width=30).pack(padx=5, pady=5)

        ttk.Label(self.generate_set_frame, text='Definition: ').pack(padx=5, pady=5)
        ttk.Entry(self.generate_set_frame, textvariable=self.definition, width=30).pack(padx=5, pady=5)

        # add word button (add_word)
        self.add_word_button = ttk.Button(self.generate_set_frame, text='Add Term', command=self.add_term).pack(padx=5, pady=10)

        # save set button (create_set)
        self.save_set_button = ttk.Button(self.generate_set_frame, text='Save Set', command=self.create_and_populate_set).pack(padx=5, pady=10)
        

        
    def set_tab(self):
        self.select_set_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.select_set_frame, text='Select Set')

        self.sets_combobox = ttk.Combobox(self.select_set_frame, state='readonly')
        self.sets_combobox.pack(padx=5, pady=5)
        self.populate_sets_combobox()

        # select set button (select_set)
        self.select_set_button = ttk.Button(self.select_set_frame, text='Select Set', command=self.select_set).pack(padx=5, pady=5)

        # delete set button
        self.delete_set_button = ttk.Button(self.select_set_frame, text='Delete Set', command=self.delete_selected_set).pack(padx=5, pady=5)

    def study_tab(self):
        self.flashcards_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.flashcards_frame, text='Study' )

        # display term  and definition on flashcard
        self.term_label = ttk.Label(self.flashcards_frame, text='', font=('TkDefaultFont', 24))
        self.term_label.pack(padx=5,pady=10)

        self.definition_label = ttk.Label(self.flashcards_frame, text='')
        self.definition_label.pack(padx=5, pady=5)

        # flip flashcards (flip_card)
        self.flip_card_button = ttk.Button(self.flashcards_frame, text='Flip', command=self.flip_card).pack(side='left',padx=5,pady=5)

        # button to view next card (next_card)
        self.next_card_button = ttk.Button(self.flashcards_frame, text='Next', command=self.next_card).pack(side='right', padx=5,pady=5)

        # button to view previous card previous_card
        self.previous_card_button = ttk.Button(self.flashcards_frame, text='Previous Card', command=self.prev_card).pack(side='left',padx=5,pady=5)

    
    def populate_sets_combobox(self):
        all_sets = self.db.get_sets()
        print(f"Available sets: {all_sets}")  # Debugging statement to show available sets
        self.sets_combobox['values'] = list(all_sets.keys())
        if all_sets:
            self.sets_combobox.current(0)


    def create_and_populate_set(self):
        self.create_set()
        self.populate_sets_combobox()

    # adds word to a set 
    def add_term(self):
        set_name = self.set_name.get()
        term = self.term.get()
        definition = self.definition.get()

        if set_name and term and definition:
            sets = self.db.get_sets()
            if set_name not in sets:
                set_id = self.db.add_set(set_name)
            else:
                set_id = sets[set_name]

            self.db.add_card(set_id, term, definition)
            self.term.set('')
            self.definition.set('')


    # creates a set
    def create_set(self):
        set_name = self.set_name.get()
        if set_name:
            existing_sets = self.db.get_sets()
            print(f"Existing sets before adding: {existing_sets}")  # Debugging statement
            if set_name not in existing_sets:
                set_id = self.db.add_set(set_name)
                print(f"Added set with ID: {set_id}")  # Debugging statement
                self.set_name.set('')
                self.term.set('')
                self.definition.set('')
                self.populate_sets_combobox()
            else:
                print("Set already exists.")  # Debugging statement if the set already exists
        else:
            print("Set name is empty.")  # Debugging statement if the set name is empty


    def delete_selected_set(self):
        set_name = self.sets_combobox.get()
        if set_name:
            result = messagebox.askyesno('Confirmation', f'Are you sure you want to delete the set "{set_name}"?')
            if result:
                set_id = self.db.get_sets()[set_name]
                self.db.delete_set(set_id)
                self.populate_sets_combobox()  # Update the combobox
                self.clear_flashcard_display()


                # clears combobox after last set is deleted
                if not self.db.get_sets():
                    self.sets_combobox.set('')


    # allows for set selection
    def select_set(self):
        set_name = self.sets_combobox.get()
        if set_name:
            set_id = self.db.get_sets()[set_name]
            cards = self.db.get_cards(set_id)
            self.display_flashcards(cards)
        else:
            self.clear_flashcard_display()

    # displays flashcards
    def display_flashcards(self, cards):
        self.card_index = 0
        self.current_cards = cards
        if cards:
            self.show_card()
        else:
            self.clear_flashcard_display()


    # clears flashcard display
    def clear_flashcard_display(self):
        self.term_label.config(text='')
        self.definition_label.config(text='')


    # shows cards when other function request so
    def show_card(self):
        if self.current_cards:
            term, _ = self.current_cards[self.card_index]
            self.term_label.config(text=term)
            self.definition_label.config(text='')
        else:
            self.clear_flashcard_display()


    # flips card both ways 
    def flip_card(self):
        if self.current_cards:
            _, definition = self.current_cards[self.card_index]
            self.definition_label.config(text=definition)

    # changes card to next index in set
    def next_card(self):
        if self.current_cards:
            self.card_index = min(self.card_index + 1, len(self.current_cards) - 1)
            self.show_card()

    # changes card to previous index in set
    def prev_card(self):
        if self.current_cards:
            self.card_index = max(self.card_index - 1, 0)
            self.show_card()
