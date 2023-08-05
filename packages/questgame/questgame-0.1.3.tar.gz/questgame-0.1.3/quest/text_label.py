import arcade
from quest.helpers import tint, shade
from textwrap import wrap

class TextLabel:
    """Draws text onto a specific part of the screen. 
    """
    width = 400
    font_size = 16
    line_height = 20
    padding = 6
    font_color = arcade.color.BLACK
    background_color = arcade.color.LIGHT_GRAY
    wrap_at = 40
    highlight = False

    def __init__(self, text, x_center, y_center):
        self.x_center = x_center
        self.y_center = y_center
        if self.wrap_at:
            self.text_lines = wrap(text, self.wrap_at)
        else:
            self.text_lines = [text]

    def draw(self):
        if self.background_color:
            arcade.draw_rectangle_filled(
                self.x_center, 
                self.y_center, 
                self.width,
                self.height(),
                tint(self.background_color) if self.highlight else self.background_color 
            )
        for i, line in enumerate(self.text_lines):
            arcade.draw_text(
                line, 
                self.text_x(),
                self.text_y(i),
                tint(self.font_color) if self.highlight else self.font_color,
                self.font_size
            )

    def height(self):
        return len(self.text_lines) * self.line_height + 2 * self.padding

    def text_x(self):
        return self.x_center - self.width / 2 + self.padding
    
    def text_y(self, line=0):
        y_top = self.y_center + self.height() / 2 
        return y_top - (line + 1) * (self.padding + self.line_height)

class TextLabelStack:
    """ Creates a stack of TextLabels
    """
    text_label_class = TextLabel
    margin = 10

    def __init__(self, text_for_labels, x_center, y_top):
        self.x_center = x_center
        self.y_top = y_top
        self.text_labels = []
        for i, text in enumerate(text_for_labels):
            label = self.text_label_class(
                text, 
                self.x_center,
                self.y_top - self.height()
            )
            label.y_center -= label.height() / 2
            self.text_labels.append(label)

    def height(self):
        label_heights = sum([label.height() for label in self.text_labels])
        margin_heights = (1 + len(self.text_labels)) * self.margin
        return label_heights + margin_heights

    def draw(self):
        for label in self.text_labels:
            label.draw()

    def get_highlight(self):
        for label_index, label in enumerate(self.text_labels):
            if label.highlight:
                return label_index

    def set_highlight(self, i):
        for label_index, label in enumerate(self.text_labels):
            label.highlight = (i == label_index)

    def __len__(self):
        return len(self.text_labels)
