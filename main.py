import os

def clear_terminal():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Unix-based systems (Linux, macOS)
    else:
        os.system('clear')

class FlashCard():
    """
    A flashcard that has attributes:
    term: a string
    definition: a string
    """
    def __init__(self, term, definition):
        self.term = str(term)
        self.definition = str(definition)

if __name__ == '__main__':
    while True:
        flashcards = []
        while True:
            clear_terminal()
            flashcard_term = input('Please enter the term of your flashcard. Enter nothing to study: ')
            if flashcard_term == '':
                clear_terminal()
                break
            flashcard_definition = input('Please enter the definition of your flashcard: ')
            clear_terminal()
            flashcard = FlashCard(flashcard_term, flashcard_definition)
            flashcards.append(flashcard)

        attempts = 0
        while len(flashcards) > 0:
            for i, card in enumerate(flashcards):
                answer = input(f'What is the definition for the term {card.term}? ')
                if answer == card.definition:
                    clear_terminal()
                    print('Thats the correct answer!')
                    flashcards.pop(i)
                else:
                    clear_terminal()
                    print('Wrong, try again after studying the rest of the cards!')
            attempts += 1 
        
        print('You have finished studying!')
        print(f'It took you {attempts} attempts!')
        break
            

