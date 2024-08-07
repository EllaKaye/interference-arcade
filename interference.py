import arcade
import random

"""
I use the follow 'magic' numbers throught:
4: number of suits, number of rows
13: number of cards in a suit, number of cards in a row
There numbers are well understood in the context of a deck of cards,
so I feel it's acceptable to use them hard-coded.
"""

# Constants for sizing
CARD_SCALE = 0.6

# How big are the cards?
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

# How much space do we leave as a gap between the cards?
# Done as a percent of the card size.
X_MARGIN = CARD_WIDTH
Y_MARGIN = CARD_WIDTH

# Gaps between rows and columns
X_GAP_PCT = 0.1
X_GAP = X_GAP_PCT * CARD_WIDTH
Y_GAP = 0.35 * CARD_HEIGHT

# The X of where to start putting things on the left side
X_START = X_MARGIN + CARD_WIDTH / 2

# The Y values for the bottom (row 0) of the four rows
Y_START = Y_MARGIN + CARD_HEIGHT / 2 

# Screen title and size
SCREEN_WIDTH = 2 * X_MARGIN + 13 * CARD_WIDTH + 12 * X_GAP
SCREEN_HEIGHT = 2 * Y_MARGIN + 4 * CARD_HEIGHT + 3 * Y_GAP
SCREEN_TITLE = "Interference"

# Card constants
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
GAME_VALUES = ["Blank", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]
# Not needed for game, but makes printing for debigging nicer
SUIT_ICONS = {"Spades": "♠️", "Clubs": "♣️", "Hearts": "♥️", "Diamonds": "♦️"}
VALUES_INT = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "Blank": 0}
#VALUES_INT = {value: index for index, value in enumerate(CARD_VALUES)}

class Card(arcade.Sprite):
    """Card sprite"""

    def __init__(self, suit, value, scale = 1):
        """Card constructor"""
    
        # Attributes
        self.suit = suit
        self.value = value
        self.value_int = VALUES_INT[self.value]

        # Image to use for the sprite
        self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"

        # Call the parent
        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")


    def set_visibility(self):
        """Set visibility for the card. Needs to be called after card initialised in setup"""
        if self.value in ["A", "Blank"]:
            self.visible = False

    def __str__(self):
        if (self.value == "Blank"):
            return "__"
        elif (self.suit in CARD_SUITS):
            return f"{self.value}{SUIT_ICONS[self.suit]}"


class Row(arcade.SpriteList):
    """A row of cards, which is a SpriteList"""

    def __init__(self, cards):
        """Row constructor"""
        super().__init__() # initialise the parent class
        self.extend(cards) # add the given cards to the row


    def __str__(self):
        return " ".join(str(card) for card in self)

    def is_stuck(self):
        """A Row is stuck if all Blanks are after Kings"""

        last_card_was_K = False

        for card in self:
            if card.value == "K":
                last_card_was_K = True
            elif card.value == "Blank":
                if not last_card_was_K:
                    return False # Found a Blank not after a King
                # if we see a Blank after a K, or another Blank, do nothing
            else:
                last_card_was_K = False # reset flag for any other card

        # We have looped over row and found all Blanks after Kings
        return True


class MyGame(arcade.Window):
    """Main application class"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.AMAZON)

        # Sprite list with all cards (regardless of row)
        self.deck = None

        # cards we need to consider each move
        self.card_1 = None # the first card clicked on
        self.card_2 = None # where we try to move the card (should be a Blank)
        self.test_card = None # the card before the Blank card, to check logic for valid move

        # list of lists (one for each row)
        self.rows = None

        # Game state
        self.round = 1 # 3 rounds allowed, always start new game on round 1
        self.round_over = None # need to allow for (unlikely) case that round is dealt over, so don't set to False in setup
        self.game_over = False

    def setup(self):
        """Seup up game here. Call this function to restart"""
        
        # create the deck as a SpriteList, and fill with cards
        # N.B. assign positions later, once they're in rows
        # need to create Aces and assign them images, then swap to Blank,
        # otherwise they don't get a hitbox
        self.deck = arcade.SpriteList()
        for card_suit in CARD_SUITS:
            for card_value in CARD_VALUES:
                card = Card(card_suit, card_value, CARD_SCALE)
                card.set_visibility()
                self.deck.append(card)

        # replace Aces with Blanks
        for card in self.deck:
            if card.value == "A":
                card.value = "Blank"

        # shuffle the deck
        self.shuffle(self.deck)

        # split the deck into four lists (the `in` clause) 
        # then assign these to Row class 
        self.rows = [Row(row) for row in [self.deck[i*13:(i+1)*13] for i in range(4)]]
        
        for row in self.rows:
            print(row)

        # check for (extremely unlikely case) that deal results in round over
        # set the value, in either case
        self.round_over = all(row.is_stuck() for row in self.rows)

        # give each card a position, so it can be drawn
        for i, row in enumerate(self.rows):
            for j in range(13):
                row[j].position = X_START + j * (CARD_WIDTH + X_GAP), Y_START + i * (CARD_HEIGHT + Y_GAP)


    def shuffle(self, cards: arcade.SpriteList):
        """Shuffle a SpriteList of cards"""
        # random.shuffle doesn't work on a SpriteList, so need a custom method
        for pos1 in range(len(cards)):
            pos2 = random.randrange(len(cards))
            cards.swap(pos1, pos2)

    def get_card_indices(self, card):
        """Get the row index, and index within row, for a card in rows"""

        for i, row in enumerate(self.rows):
            if (card) in row:
                return i, row.index(card)


    def on_draw(self):
        self.clear()

        for row in self.rows:
            row.draw()

    
    def on_mouse_press(self, x, y, button, modifiers):

        card = None

        card_list = arcade.get_sprites_at_point((x, y), self.deck)
        # if we clicked on a card, extract the card from the list
        if card_list:
            card = card_list[0]
            print(f"Card: {card}") 
        
        # if no cards selected and click on card, set card_1
        if card and card.value != "Blank" and not self.card_1 and not self.card_2:
            self.card_1 = card
            self.card_1.scale += X_GAP_PCT
            print(f"Card 1: {self.card_1}")
        
        # if card_1 selected and click on card, change card_1
        elif card and card.value != "Blank" and self.card_1 and not self.card_2:
            self.card_1.scale -= X_GAP_PCT
            self.card_1 = card
            self.card_1.scale += X_GAP_PCT
            print(f"New card 1: {self.card_1}")

        # if card_1 selected and click on card, set card_2
        elif card and card.value == "Blank" and self.card_1 and not self.card_2:
            self.card_2 = card
            print(f"Card 2: {self.card_2}")

            # get row and index of card_2
            card_2_row, card_2_index = self.get_card_indices(self.card_2)
            print(f"card_2 is in row {card_2_row}, index {card_2_index}")

            # get row and index of test_card (if one exists, i.e. card_2 not at beginning of row)

                # get test_card
            
                # check if move is valid

                    # if valid:

                        # swap card_1 and card_2 in rows list

                        # swap position of card_1 and card_2 in the window (and reset card_1 size)

                        # reset card_1 and card_2 to None


def main():
    window = MyGame()
    window.setup()
    arcade.run()
    #NineD = Card("9", "Diamonds")
    #print(NineD)

if __name__ == "__main__":
    main()