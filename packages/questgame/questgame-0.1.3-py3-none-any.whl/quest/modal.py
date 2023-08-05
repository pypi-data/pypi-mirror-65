# Modal
# -------------------
# A modal window is a "pop-up" that creates a mode--it pauses the game until the 
# window

import arcade
from quest.text_label import TextLabelStack

class Modal:
    """ A modal window is a pop-up that pauses the game until it is resolved.
    It is called a Modal because it puts the game into a new mode. 

    Arguments: 
        game: The game which the Modal is part of.
    """
    width = 400
    height = 400
    background_color = arcade.color.LIGHT_GRAY

    def __init__(self, game):
        self.game = game
        self.x_center = 0
        self.y_center = 0
        self.set_text_labels()
        self.set_option_labels()

    def update_position(self, x, y):
        self.x_center = x
        self.y_center = y
        self.set_text_labels()
        self.set_option_labels()

    def set_text_labels(self):
        self.text_labels = TextLabelStack(
            ["Sorry to bother you with this modal.", "But it's important."], 
            self.x_center,
            self.y_center + self.height / 2
        )

    def set_option_labels(self):
        self.option_labels = TextLabelStack(
            ["OK", "Fine"],
            self.x_center,
            self.y_center + 100
        )
        self.option_labels.set_highlight(0)

    def choose_option(self, value):
        """When a button is clicked, it calls choose_option with its value.
        """
        self.game.close_modal()

    def on_key_release(self, key, modifiers):
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            i = (self.option_labels.get_highlight() + 1) % len(self.option_labels)
            self.option_labels.set_highlight(i)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            i = (self.option_labels.get_highlight() - 1) % len(self.option_labels)
            self.option_labels.set_highlight(i)
        elif key == arcade.key.ENTER:
            self.choose_option(self.option_labels.get_highlight())

    def on_draw(self):
        arcade.draw_rectangle_filled(
            self.x_center, 
            self.y_center, 
            self.width, 
            self.height, 
            self.background_color
        )
        self.text_labels.draw()
        self.option_labels.draw()

class DialogueModal(Modal):
    """A modal window powered by a Dialogue object.
    """
    def __init__(self, game, dialogue):
        self.dialogue = dialogue
        super().__init__(game)

    def set_text_labels(self):
        self.text_labels = TextLabelStack(
            self.dialogue.get_content(),
            self.x_center,
            self.y_center + self.height / 2
        )

    def set_option_labels(self):
        self.option_labels = TextLabelStack(
            self.dialogue.get_options(),
            self.x_center,
            self.y_center 
        )
        self.option_labels.set_highlight(0)

    def choose_option(self, value):
        self.dialogue.choose(value)
        if self.dialogue.running:
            self.set_text_labels()
            self.set_option_labels()
        else:
            self.game.close_modal()
