from PIL import Image
import xml.etree.ElementTree as ET
from itertools import product, chain
from pathlib import Path
from enum import Flag, auto
from math import sqrt
import re

def tint(color, ratio=0.25):
    """Creates a tint of a color by scaling it toward pure white.

    Arguments:
        color (int, int, int): The base color.
        ratio (float): A value between 0 and 1. 0 would have no effect; 
            1 would be pure white.
    """
    return tuple(round(255 - (255 - c) * (1 - ratio)) for c in color)

def shade(color, ratio=0.25):
    """Creates a shade of a color by scaling it toward pure black.

    Arguments:
        color (int, int, int): The base color.
        ratio (float): A value between 0 and 1. 0 would have no effect; 
            1 would be pure black.
    """
    return tuple(round(c * (1 - ratio)) for c in color)

class Direction(Flag):
    """Direction lets you talk about directions like `Direction.DOWN`, `Direction.UPLEFT`
    or using compass directions such as `Direction.NE`.
    """

    NONE = 0
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    UPRIGHT = UP | RIGHT
    UPLEFT = UP | LEFT
    DOWNLEFT = DOWN | LEFT
    DOWNRIGHT = DOWN | RIGHT

    E = RIGHT
    N = UP
    S = DOWN
    W = LEFT
    NE = N | E
    NW = N | W
    SW = S | W
    SE = S | E

    PRIMARY_AXIS = LEFT | RIGHT

    @classmethod
    def from_vector(cls, vector, diagonal=True):
        """Converts an (x, y) tuple into a direction. 

            >>> Direction.from_vector((-1, 0))
            Direction.LEFT
            >>> Direction.from_vector((0.4, 0.6))
            Direction.UPRIGHT

        Arguments: 
            vector (float, float): An (x, y) tuple.
            diagonal (bool): Whether to include diagonal directions. Defaults to True.

        Returns:
            A Direction.
        """
        vx, vy = vector
        result = cls.NONE
        if vx < 0: 
            result |= cls.LEFT
        if vx > 0: 
            result |= cls.RIGHT
        if vy < 0:
            result |= cls.DOWN
        if vy > 0:
            result |= cls.UP
        if result.is_diagonal() and not diagonal:
            result &= cls.PRIMARY_AXIS
        return result

    def is_diagonal(self):
        """Returns whether the Direction is diaognal.

            >>> Direction.NW.is_diagonal()
            True
        """
        return self in [self.NE, self.NW, self.SW, self.SE]

    def to_vector(self, normalized=False):
        """Converts the Direction into an (x, y) tuple.

        Arugments: 
            normalized (bool): Whether to normalize the vector so that its 
                magintude is 1. Defaults to False, in which case x and y are
                each either 0 or 1.
        """
        vx, vy = 0, 0
        if self & self.RIGHT:
            vx += 1
        if self & self.UP:
            vy += 1
        if self & self.LEFT:
            vx -= 1
        if self & self.DOWN:
            vy -= 1
        if normalized:
            vx, vy = normalize((vx, vy))
        return vx, vy

class SpriteListList:
    """Allows multiple SpriteLists to be treated as if they were a single SpriteList.
    """
    def __init__(self, sprite_lists):
        self.sprite_lists = sprite_lists

    def chain_sprite_lists(self):
        return chain.from_iterable(self.sprite_lists)

    def __iter__(self):
        return iter(self.chain_sprite_lists())

    def update(self):
        for sprite_list in self.chain_sprite_lists():
            sprite_list.update()

def tileset_to_collection(image_path, tile_size, output_dir, name="tileset", create_tsx=True):
    """Splits a tileset image into separate files.

    Quest relies on Arcade, which only works with collections of images. 
    A lot of game art is provided as a single tile image. This function can help split
    it out.

    Args:
        image_path: Path to an image containing a grid of tiles.
        tile_size: Size in pixels of each tile.
        output_dir: Directory for output files (there may be a lot of them).
        name: Name of the tileset.
        create_tsx: If True, also creates a tsx file which can be opened as a
            :doc:`Tileset <tiled:manual/editing-tilesets>` using 
            :doc:`Tiled <tiled:manual/introduction>`.

    """
    img = Image.open(image_path)
    width, height = img.size
    cols, rows = width // tile_size, height // tile_size
    for i, j in product(range(cols), range(rows)):
        left = i * tile_size
        upper = j * tile_size
        right = left + tile_size
        lower = upper + tile_size
        tile = img.crop((left, upper, right, lower))
        output_path = Path(output_dir) / "img_{}_{}.png".format(j, i)
        tile.save(output_path)

    if create_tsx:
        tileset = empty_tileset(tile_size, cols, rows, name)
        for ix, (j, i) in enumerate(product(range(rows), range(cols))):
            add_tile(tileset, ix, "img_{}_{}.png".format(j, i))
        with open(Path(output_dir) / "{}.tsx".format(name), 'wb') as f:
            ET.ElementTree(tileset).write(f, encoding="UTF-8", xml_declaration=True)

def empty_tileset(tile_size, cols, rows, name):
    tileset = ET.Element("tileset")
    tileset.set('version', "1.2")
    tileset.set('tiledversion',"1.3.1")
    tileset.set('name', name)
    tileset.set('tilewidth', str(cols))
    tileset.set('tileheight', str(rows))
    tileset.set('tilecount', str(cols * rows))
    tileset.set('columns', "0")
    grid = ET.SubElement(tileset, "grid")
    grid.set('orientation', "orthagonal")
    grid.set('width', "1")
    grid.set('height', "1")
    return tileset

def add_tile(tileset, tile_id, img_path):
    tile_element = ET.SubElement(tileset, 'tile')
    tile_element.set('id', str(tile_id) )
    img_element = ET.SubElement(tile_element, 'image')
    img_element.set('width', tileset.get('tilewidth'))
    img_element.set('height', tileset.get('tileheight'))
    img_element.set('source', img_path)

def normalize(vector):
    return scale(vector, 1)

def scale(vector, magnitude):
    vx, vy = vector
    old_magnitude = sqrt(vx * vx + vy * vy) if vx * vx + vy * vy else 0
    factor = magnitude / old_magnitude
    return vx * factor, vy * factor
    
class SimpleInkParser:
    """Parses a simple subset of Ink syntax into a JSON-like data structure. 

    The ink must meet the following constraints:

    - Must be valid Ink.
    - All content must be in a knot. Knots must be delimited 
      with three equal signs on either side of the knot name.
    - The only syntax allowed is knot declarations, sticky choices
      (+) and diverts (->). Diverts are only allowed following a sticky
      choice.
    """
    def parse(self, ink):
        """Reads a story written in a subset of Ink syntax (described above) and returns a
        data structure of content and choices, also described above.
        """
        dialogue = {}
        knots = self.split_knots(ink)
        for line_num, knot_name, knot_ink in knots:
            content, options = self.parse_knot_ink(line_num, knot_ink)
            if len(options) == 0:
                raise ValueError("line {}: Knot {} has no options".format(line_num, knot_name))
            if knot_name in dialogue.keys():
                raise ValueError("line {}: Knot {} already defined".format(line_num, knot_name))
            dialogue[knot_name] = {"content": content, "options": options}
        return dialogue

    def parse_knot_ink(self, line_num, ink):
        """Reads lines of code in a knot and returns a list of content and a dict of options.
        """
        content, options = self.split_content_from_options(ink)
        content = [c.strip() for c in content]
        content = self.split_and_join(content, lambda c: not c)
        parsed_content = [c.strip() for c in content if c.strip()]
        options = [o.strip() for o in options]
        options = self.split_and_join(options, lambda o: re.match("\s*\+", o))
        parsed_options = {}
        for option in options[1:]: 
            match = re.match("\s*\+(?P<text>.*)\->\s*(?P<knot>[a-zA-Z_]+)", option)
            if not match: 
                raise ValueError("line {}: Error reading option in knot.".format(line_num))
            parsed_options[match.group('text').strip()] = match.group('knot')
        return parsed_content, parsed_options

    def split_and_join(self, strings, condition):
        """Splits a list of strings on a condition and joins the results. For example, 

            >>> vowel = lambda l: l in 'aeiou'
            >>> split_and_join(list('abcdefghijklmnop'))
            ['a', 'bcde', 'fghi', 'jklmno', 'p']
        """
        splits = [i for i, s in enumerate(strings) if condition(s)]
        return [' '.join(strings[i:j]) for i, j in zip([0] + splits, splits + [len(strings)])]

    def split_content_from_options(self, ink):
        content, options = [], []
        for line in ink:
            if any(options) or re.match("\s*\+", line):
                options.append(line)
            else:
                content.append(line)
        return content, options

    def split_knots(self, ink):
        knots = []
        current_name = None
        current_ink = []
        for i, line in enumerate(ink):
            name = self.parse_knot_declaration(line)
            # The first knot has not started yet 
            if name is None and current_name is None:
                continue
            # Starting the first knot
            elif name is not None and current_name is None:
                current_name = name
            # Starting a new knot
            elif name is not None:
                if len(current_ink) == 0:
                    raise ValueError("Expected knot content at line {}".format(i))
                starting_line_num = i - len(current_ink)
                knots.append((starting_line_num, current_name, current_ink))
                current_name = name
                current_ink = []
            # Continuing inside a knot
            else:
                current_ink.append(line)
        # At end of file, the final knot's contents
        if len(current_ink) == 0:
            raise ValueError("Expected knot content at line {}".format(i))
        starting_line_num = i - len(current_ink) - 1
        knots.append((starting_line_num, current_name, current_ink))
        return knots
                
    def parse_knot_declaration(self, line):
        "Returns knot name if found"
        match = re.match("===\s+([a-zA-Z_]+)\s+===", line)
        return match.group(1) if match else None


