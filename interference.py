import arcade
import random

"""
I use the follow 'magic' numbers throught:
4: number of suits, number of rows
13: number of cards in a suit, number of cards in a row
These numbers are well understood in the context of a deck of cards,
so I feel it's acceptable to use them hard-coded.
"""

# Constants for sizing
CARD_SCALE = 0.6

# How big are the cards?
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

# How much space do we leave at the edges?
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
# 'Blank' allows for playing spaces (will need to be ignored when creating deck)
CARD_VALUES = ["Blank", "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
# GAME_VALUES = ["Blank", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
#VALUES_INT = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "Blank": 0}
VALUES_INT = {value: index for index, value in enumerate(CARD_VALUES)} # allows us to check for consecutive values
#VALUES_INT["Blank"] = 0
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]
# Not needed for game, but makes printing for debigging nicer
SUIT_ICONS = {"Spades": "♠️", "Clubs": "♣️", "Hearts": "♥️", "Diamonds": "♦️"}

# For text
DEFAULT_LINE_HEIGHT = 45
DEFAULT_FONT_SIZE = 20

# Number of rounds
ROUNDS = 3

class Deck(arcade.SpriteList):
    "Deck spritelist. Will contain cards"
    
    def __init__(self):
        """Deck constructor"""
        # will add cards later
        super().__init__() # initialise the parent class

    def __str__(self):
        return " ".join(str(card) for card in self)
    
    def shuffle(self):
        """Shuffle a SpriteList of cards"""
        # random.shuffle doesn't work on a SpriteList, so need a custom method
        for pos1 in range(len(self)):
            pos2 = random.randrange(len(self))
            self.swap(pos1, pos2)


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

    def split_index(self):
        if self[0].value_int != 2:
            return 0
        suit = self[0].suit
        for i in range(1, len(self)):
            if self[i].suit != suit or self[i].value_int != i + 2:
                return i
        return len(self) - 1 # 12 (an ordered row with 2-K will still have a blank or other card at the end)

    def split(self, index):
        return self[:index], self[index:]

    def fill_row(self, deck):
        while len(self) < 13:
            self.append(deck.pop())
        return self

    def is_ordered(self):
        return self.split_index() == 12

class Rows(list):
    """A list of four `Row`s"""
    
    def __init__(self, rows):
        # initialise parent class (list) with list of rows
        super().__init__(rows)

    def __str__(self):
        out = ""
        for row in reversed(self):
            out += str(row) + "\n"
        return out

    def get_card_indices(self, card):
        """Get the row index, and index within row, for a card in rows"""

        for i, row in enumerate(self):
            if (card) in row:
                return i, row.index(card)

    def get_test_card(self, card):
        """Given a card, find the card before it in the row, if it exists"""
        card_row, card_index = self.get_card_indices(card)
        if card_index == 0:
            return None
        else:
            return self[card_row][card_index - 1]

    def is_valid_move(self, card1, card2):
        test_card = self.get_test_card(card2)

        # Move not valid if card1 is blank or if card2 is not blank
        if card1.value == "Blank" or card2.value != "Blank":
            return False

        # can move a 2 to the start of a row
        # (test_card is None)
        if not test_card and card1.value_int == 2:
            return True
        # can't move anything else to start of row
        elif not test_card:
            return False
        # same suit and consecutive values
        elif card1.suit == test_card.suit and test_card.value_int == (card1.value_int - 1):
            return True
        else:
            return False

    def swap_cards(self, card1, card2):
            # get row and index of card1 and card2
            card1_row, card1_index = self.get_card_indices(card1)
            card2_row, card2_index = self.get_card_indices(card2)
            print(f"card1 is in row {card1_row}, index {card1_index}")
            print(f"card2 is in row {card2_row}, index {card2_index}")

            # get positions
            card1_pos = card1.position
            card2_pos = card2.position

            # reset card_1 size
            card1.scale -= X_GAP_PCT 
            
            # swap positions (affects drawing)
            card1.position = card2_pos
            card2.position = card1_pos
            
            # swap in lists (affects game logic)
            if card1_row == card2_row:
                # If both cards are in the same row, swap them directly, using built-in swap method
                self[card1_row].swap(card1_index, card2_index)
            else:
                # if in different rows
                # temporarily remove the sprites from their positions
                # since can't have two of the same sprites in a SpriteList, 
                # so a direct swap doesn't work
                self[card1_row].pop(card1_index)
                self[card2_row].pop(card2_index)

                # Insert the sprites into their new positions
                self[card2_row].insert(card2_index, card1)
                self[card1_row].insert(card1_index, card2)

    def all_stuck(self):
        return all(row.is_stuck() for row in self)

    def ordered_unordered(self):
        indices = [row.split_index() for row in self]
        split_rows = [row.split(i) for row, i in zip(self, indices)]
        ordered = [item[0] for item in split_rows]
        unordered = [element for item in split_rows for element in item[1]]
        return ordered, unordered

    def all_ordered(self):
        return all(row.is_ordered() for row in self)
        
    def assign_positions(self):
        """Assign positions for a full deal"""
        for i, row in enumerate(self):
            for j in range(13):
                row[j].position = X_START + j * (CARD_WIDTH + X_GAP), Y_START + i * (CARD_HEIGHT + Y_GAP)


class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Interference", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                        arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Press I for instructions", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                        arcade.color.GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Click or press ENTER to start a new game", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150,
                        arcade.color.GRAY, font_size=20, anchor_x="center")

        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed"""

        # show instructions
        if key == arcade.key.I:
            instructions_view = InstructionView()
            self.window.show_view(instructions_view)

        # start a new game
        if key == arcade.key.ENTER:
            game_view = GameView()
            self.window.show_view(game_view)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)

class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()
        self.text_box = None
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Instructions Screen", 20, SCREEN_HEIGHT - 35,
                        arcade.color.BLACK, font_size=20, anchor_x="left")
        arcade.draw_text("long_text", 20, SCREEN_HEIGHT - 75,
                        arcade.color.GRAY, font_size=20, width = SCREEN_WIDTH-20, anchor_x="left", multiline=True)

        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed"""

        # start a new game
        if key == arcade.key.ENTER:
            game_view = GameView()
            self.window.show_view(game_view)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


class GameView(arcade.View):
    """Main application class"""

    def __init__(self):
        super().__init__()

        # Sprite list with all cards (regardless of row)
        self.deck = None

        # cards we need to consider each move
        self.card_1 = None # the first card clicked on
        self.blank = None # where we try to move the card (should be a Blank)

        # list of lists (one for each row)
        self.rows = None

        # Game state
        self.round = None # 3 rounds allowed, always start new game on round 1
        self.round_over = None # need to allow for (unlikely) case that round is dealt over, so don't set to False in setup
        self.game_over = None
        self.success = None # if all rows are ordered

        # For displaying user interface messages
        self.round_message = None
        self.round_message_text = None
        self.message = None

        # Call setup to initialize the game
        self.setup()

    def setup(self):
        """Seup up game here. Call this function to restart"""
        # Game state
        self.round = 1
        self.round_message_text = f"Round {self.round} of {ROUNDS}"
        self.game_over = False

        # deselect any selected cards
        # e.g. if call new game in middle of another game
        if self.card_1:
            self.card_1.scale -= X_GAP_PCT
        self.card_1 = self.blank = None

        # create the deck as a SpriteList, and fill with cards
        # N.B. assign positions later, once they're in rows
        # need to create Aces and assign them images, then swap to Blank,
        # otherwise they don't get a hitbox
        #self.deck = arcade.SpriteList()
        self.deck = Deck()
        for card_suit in CARD_SUITS:
            for card_value in CARD_VALUES[1:]: # don't create 'Blank' cards
                card = Card(card_suit, card_value, CARD_SCALE)
                card.set_visibility()
                self.deck.append(card)

        # replace Aces with Blanks
        for card in self.deck:
            if card.value == "A":
                card.value = "Blank"

        # shuffle the deck
        self.deck.shuffle()

        # split the deck into four lists (the `in` clause) 
        # then assign these to Row class 
        #self.rows = [Row(row) for row in [self.deck[i*13:(i+1)*13] for i in range(4)]]
        self.rows = Rows([Row(row) for row in [self.deck[i*13:(i+1)*13] for i in range(4)]])

        #print("Rows:")
        #print(self.rows)

        # round message
        start_x = X_MARGIN
        start_y = SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 1.5
        self.round_message = arcade.Text(self.round_message_text,
                        start_x,
                        start_y,
                        arcade.color.WHITE,
                        font_size=DEFAULT_FONT_SIZE)
                        #width=SCREEN_WIDTH,
                        #align="left"
        #self.round_message.scale = 0.5

        # check for (extremely unlikely case) that deal results in round over
        # set the value, in either case
        self.round_over = self.rows.all_stuck()

        # give each card a position, so it can be drawn
        self.rows.assign_positions()

    def on_show_view(self):
        """Called whenever this view is shown"""
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        self.clear()

        self.round_message.draw()

        # manually reset viewport
        # this is necessary to overcome a weird effect where drawing the text 
        # causes an annimation effect that makes all the drawing shrink towards the bottom left corner
        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

        for row in self.rows:
            row.draw()

    def on_mouse_press(self, x, y, button, modifiers):

        # click shouldn't register anything if the round is over
        if self.round_over or self.game_over:
            return

        card = None

        card_list = arcade.get_sprites_at_point((x, y), self.deck)
        # if we clicked on a card, extract the card from the list
        if card_list:
            card = card_list[0]
            #print(f"Card: {card}") 
        
        # if no card to swap selected and click on card, set card_1
        if card and card.value != "Blank" and not self.card_1 and not self.blank:
            self.card_1 = card
            self.card_1.scale += X_GAP_PCT
            print(f"Card 1: {self.card_1}")
        
        # if card_1 selected and click on card, change card_1
        elif card and card.value != "Blank" and self.card_1 and not self.blank:
            self.card_1.scale -= X_GAP_PCT
            self.card_1 = card
            self.card_1.scale += X_GAP_PCT
            print(f"New card 1: {self.card_1}")

        # if card_1 selected and click on Blank, set blank
        elif card and card.value == "Blank" and self.card_1 and not self.blank:
            self.blank = card
            print(f"Blank: {self.blank}")

            # if we have a card and a blank, and valid move, then swap
            if self.card_1 and self.blank and self.rows.is_valid_move(self.card_1, self.blank):
                self.rows.swap_cards(self.card_1, self.blank)
                self.card_1 = self.blank = None

                # check game state after successful swap
                self.round_over = self.rows.all_stuck()
                if self.round_over:
                    self.success = self.rows.all_ordered()
                    if self.success:
                        print("Game won!")
                        #self.round_message_text = "Success!"
                        self.game_over = True
                        game_over_view = GameOverView(True)  # Pass True for success
                        self.window.show_view(game_over_view)
                    elif self.round == ROUNDS and not self.success:
                        self.game_over = True
                        print("Game over")
                        #self.round_message_text = "Game over"
                        game_over_view = GameOverView(False)  # Pass False when over without success
                        self.window.show_view(game_over_view)
                    else:
                        print("Round over")
                        #self.round_message_text = "Round over"
                        self.show_round_over()

                    
                    self.round_message.text = self.round_message_text
                

            # otherwise move is not valid
            else:
                print("Not a valid move")
                self.card_1.scale -= X_GAP_PCT
                self.card_1 = self.blank = None
                
            #print("After swap:")
            #print(self.rows)

    def new_round(self):

        if self.round == ROUNDS:
            game_over_view = GameOverView(False)  # Pass False when over without success
            self.window.show_view(game_over_view)
            print("Out of rounds")
            return

        self.round_over = False
        self.round += 1

        # deselect any selected cards
        if self.card_1:
            self.card_1.scale -= X_GAP_PCT
        self.card_1 = self.blank = None

        # Update, then refresh, the round message
        self.round_message_text = f"Round {self.round} of {ROUNDS}"
        self.round_message.text = self.round_message_text

        print(f"Round {self.round}")

        ordered, unordered = self.rows.ordered_unordered()
        self.rows = Rows([Row(row) for row in ordered])

        # separate out blanks for the rest
        blanks = [card for card in unordered if card.value == "Blank"]
        value_cards = [card for card in unordered if card.value != "Blank"]

        # create and shuffle a deck of the unordered cards
        unordered_deck = Deck()
        unordered_deck.extend(value_cards)
        unordered_deck.shuffle()

        # deal the blanks
        for row in self.rows:
            row.append(blanks.pop())

        # deal the rest of the cards
        for row in self.rows:
            row.fill_row(unordered_deck)

        # reassign positions so new round gets drawn appropriately
        self.rows.assign_positions()
        
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed"""
        
        # start a new round
        if key == arcade.key.R:
            self.new_round()

        # start a new game
        if key == arcade.key.ENTER:
            self.setup()

        # show instructions
        if key == arcade.key.I:
            instructions_view = InstructionView()
            self.window.show_view(instructions_view)

    def show_round_over(self):
        round_over_view = RoundOverView(self)
        self.window.show_view(round_over_view)


class RoundOverView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        # Store reference to the game view that created this round over view
        self.game_view = game_view

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("ROUND OVER", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                        arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click or press R to start new round", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                        arcade.color.GRAY, font_size=20, anchor_x="center")

        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            # Start new round in the existing game view
            self.game_view.new_round()
            # Switch back to the game view
            self.window.show_view(self.game_view)
            # Call on_show_view to reset the background color
            self.game_view.on_show_view()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
            # Start new round in the existing game view
            self.game_view.new_round()
            # Switch back to the game view
            self.window.show_view(self.game_view)
            # Call on_show_view to reset the background color
            self.game_view.on_show_view()


class GameOverView(arcade.View):
    def __init__(self, success):
        super().__init__()
        self.success = success

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMAZON if self.success else arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        message = "CONGRATULATIONS!" if self.success else "GAME OVER"
        arcade.draw_text(message, 
                        SCREEN_WIDTH / 2, 
                        SCREEN_HEIGHT / 2,
                        arcade.color.GOLD if self.success else arcade.color.WHITE, 
                        font_size=50, 
                        anchor_x="center")
        
        subtext = "You successfully ordered all the cards!" if self.success else "Better luck next time!"
        arcade.draw_text(subtext,
                        SCREEN_WIDTH / 2, 
                        SCREEN_HEIGHT / 2 - 75,
                        arcade.color.WHITE if self.success else arcade.color.GRAY, 
                        font_size=20, 
                        anchor_x="center")
        
        arcade.draw_text("Click or press ENTER to start a new game", 
                        SCREEN_WIDTH / 2, 
                        SCREEN_HEIGHT / 2 - 150,
                        arcade.color.WHITE if self.success else arcade.color.GRAY, 
                        font_size=20, 
                        anchor_x="center")

        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game_view = GameView()
            self.window.show_view(game_view)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Different Views Example")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()
    #NineD = Card("9", "Diamonds")
    #print(NineD)

if __name__ == "__main__":
    main()