import arcade
import random

"""
I use the follow 'magic' numbers throught:
4: number of suits, number of rows
13: number of cards in a suit, number of cards in a row
There numbers are well understood in the context of a deck of cards,
so I feel it's acceptable to use them hard-coded.
"""

# Screen title and size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Interference"

# Constants for sizing
CARD_SCALE = 0.6

# How big are the cards?
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

# How much space do we leave as a gap between the cards?
# Done as a percent of the card size.
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# The X of where to start putting things on the left side
START_X = CARD_WIDTH / 2 + CARD_WIDTH * HORIZONTAL_MARGIN_PERCENT

# The Y values for the bottom of the four rows
# Come back to calculate properly later
ROW_0_Y = 470
ROW_1_Y = 320
ROW_2_Y = 170
ROW_3_Y = 20

# Card constants
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]
# Not needed for game, but makes printing for debigging nicer
SUIT_ICONS = {"Spades": "♠️", "Clubs": "♣️", "Hearts": "♥️", "Diamonds": "♦️"}
VALUES_INT = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "Blank": 0}

class Card(arcade.Sprite):
    """Card sprite"""

    def __init__(self, value, suit, scale = 1):
        """Card constructor"""
    
        # Attributes
        self.suit = suit
        self.value = value
        self.value_int = VALUES_INT[self.value]

        # Image to use for the sprite
        self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"

        # Call the parent
        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")


    def __str__(self):
        return f"{self.value}{SUIT_ICONS[self.suit]}"

class Row(arcade.SpriteList):
    """A row of cards, which is a SpriteList"""

    def __init__(self, cards):
        """Row constructor"""
        super().__init__() # initialise the parent class
        self.extend(cards) # add the given cards to the row

class MyGame(arcade.Window):
    """Main application class"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Sprite list with all cards (regardless of row)
        self.deck = None

        arcade.set_background_color(arcade.color.AMAZON)

        # cards we need to consider each move
        self.card_1 = None # the first card clicked on
        self.blank_card = None # where we try to move the card (should be a blank)
        self.test_card = None # the card before the blank card, to check logic for valid move

        # sprite lists for each row
        self.row_0 = None  
        self.row_1 = None
        self.row_2 = None
        self.row_3 = None

        # list of lists (one for each row)
        self.rows = None

    def setup(self):
        """Seup up game here. Call this function to restart"""
        pass

def main():
    NineD = Card("9", "Diamonds")
    JackS = Card("J", "Spades")
    print(NineD)
    print(JackS)

if __name__ == "__main__":
    main()