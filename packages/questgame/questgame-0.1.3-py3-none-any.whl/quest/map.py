import arcade
from quest.errors import NoLayerError, MultipleLayersError
from quest.sprite import QuestSprite
from quest.shim import process_layer
from math import floor

RED = 0
GREEN = 0
BLUE = 0

def clamp(bounds, val):
    low, high = bounds
    return max(low, min(high, val))

class Map:
    """Implements a map for a level or stage in the game.

    Each QuestGame may have multiple Maps. Each Map represents a game map with 
    multiple layers, allowing the map to describe walls, loot, and multiple layers
    of background imagery.

    Attributes:
        background_color: a 3-tuple of integers for red, green, blue. Each from 0-255.
            The :py:mod:`arcade:color` module also predefines many colors.
        tile_scaling: Factor by which to scale all map tiles. Default is 1.
    """
    background_color = (RED, GREEN, BLUE)
    tile_scaling = 1

    def __init__(self):
        """Initialize a Map with an empty layers list.
        """
        self.layers = []

    def add_layer(self, layer):
        """Add a layer the the layers list.

        Checks to make sure the layer's name is unique.

        Args:
            layer: The MapLayer to add.
        """
        for existing_layer in self.layers:
            if existing_layer.name == layer.name:
                raise ValueError("Map already has a layer named {}".format(layer.name))
        self.layers.append(layer)

    def get_layer_by_name(self, layer_name):
        """Looks up a map layer by name. 

        There should only be one layer with each name. If there is not exactly one layer,
        raises an error. 

        Args:
            layer_name: The name of the layer.

        Returns: The layer.
        """
        layers = [layer for layer in self.layers if layer.name == layer_name]
        if len(layers) == 0:
            raise NoLayerError("Map has no layer named {} (layers are: {})".format(layer_name, 
                    ", ".join(layer.name for layer in self.layers)))
        elif len(layers) > 1: 
            raise MultipleLayersError("Map has more than one layer named {}".format(layer_name))
        else:
            return layers[0]

class TiledMap(Map):
    """A subclass of Map which loads its layers from a TMX file. Each layer has a collection of tiles. 
    When TiledMap is initialized, a sprite is created for each of these tiles. The sprite's image and
    position are read from the tile layer data. The sprite's class (which can determine its behavior)
    can be set using the `sprite_classes` argument. 
    
    Use TiledMap when you want to design your map using
    [Tiled](https://www.mapeditor.org/). This app saves maps as TMX files.

    Arguments:
        filename (str): Path to the .tmx tilemap file
        sprite_classes: {layer_name: SpriteClass} dict specifying the sprite class
            that should be used for each layer. 
    """
    def __init__(self, filename, sprite_classes=None):
        super().__init__()
        tilemap = arcade.tilemap.read_tmx(filename)
        for layer_name, sprite_class in sprite_classes.items():
            sprite_list = process_layer(sprite_class, tilemap, layer_name, self.tile_scaling)
            layer = MapLayer(layer_name, sprite_list)
            self.add_layer(layer)

class MapLayer:
    """
    Each Map is made up of one or more MapLayers. 

    Arguments:
        name (str): The layer name. 
        sprite_list: An optional :py:class:`arcade.SpriteList`.
    """
    def __init__(self, name, sprite_list=None):
        self.name = name
        self.sprite_list = sprite_list or arcade.SpriteList()

    def draw(self):
        """Renders the layer by calling 
        """
        self.sprite_list.draw()

    def clear(self):
        """Delete all this layer's sprites.
        """
        while len(self.sprite_list) > 0:
            self.sprite_list.pop()

class GridMapLayer(MapLayer):
    """
    A MapLayer which is aware of grid coordinates. GridMapLayers are useful in situations when you 
    want to place sprites programmatically. Several methods are provided to support calculations
    about sprite positions with respect to the grid. This cam be simpler than working in pixel positions. 
    For example, the maze example program generates a maze
    and then uses a GridMapLayer to place the walls of the maze. 
    
    Arguments:
        name (str): Layer name.
        columns (int): Number of columns in the grid.
        rows (int): Number of rows in the grid.
        pixel_width (int): Width of the grid in pixels.
        pixel_height (int): Height of the grid in pixels.
        sprite_filename (str): Path to sprite image file. Only needed if you will be creating sprites
            on this grid layer.
        sprite_class: Class of sprites to create on this layer.

    """

    sprite_class = QuestSprite

    def __init__(self, name, columns, rows, pixel_width, pixel_height, sprite_filename=None, sprite_class=None):
        super().__init__(name)
        self.columns = columns
        self.rows = rows
        self.pixel_width = pixel_width
        self.pixel_height = pixel_height
        self.sprite_filename = sprite_filename
        if sprite_class:
            self.sprite_class = sprite_class

    def add_sprite(self, grid_x, grid_y, sprite=None):
        """Adds a sprite at a given grid position.

        Arguments:
            grid_x (int): The x-coordinate of the grid position 
            grid_y (int): The y-coordinate of the grid position 
            sprite (QuestSprite): (Optional) sprite to add to this layer and place at this grid position. If no
                sprite is given, a new sprite will be created.
        """
        sprite = sprite or self.create_sprite()
        sprite.left, sprite.bottom = self.get_pixel_position((grid_x, grid_y))
        self.sprite_list.append(sprite)

    def create_sprite(self):
        """Creates a sprite with image `self.sprite_filename` and class `self.sprite_class`. 
        """
        if self.sprite_filename is None:
            raise ValueError("Can't add sprites to GridMapLayer unless sprite_filename is defined.")
        return self.sprite_class(self.sprite_filename)

    def get_pixel_position(self, grid_position, center=True):
        """Converts pixel coordinates to grid coordinates.

        Arguments:
            grid_position (int, int): x and y grid coordinates 
            center (bool): By default, returns the pixel position of the center
            of the grid tile. When False, returns the pixel position of the lower
            left corner of the grid tile.

        Returns:
            (float, float) pixel position.
        """
        grid_x, grid_y = grid_position
        pixel_x = self.pixel_width * (grid_x / self.columns)
        pixel_y = self.pixel_height * (grid_y / self.rows)
        if center:
            pixel_x += (self.pixel_width / self.columns) / 2
            pixel_y += (self.pixel_height / self.rows) / 2
        return pixel_x, pixel_y

    def get_grid_position(self, pixel_position):
        """Converts grid position to pixel position. 

        Any pixel position within a grid tile will be converted to that
        grid tile's coordinates.

        Arguments: 
            pixel_position (float, float): x and y pixel coordinates.

        Returns:
            (float, float) grid position.
        """
        pixel_x, pixel_y = pixel_position
        grid_x = pixel_x // (self.pixel_width / self.columns)
        grid_y = pixel_y // (self.pixel_height / self.rows)
        return grid_x, grid_y

    def position_in_grid(self, grid_position):
        """Returns whether or not `grid_position` is within the grid.

        Arguments:
            grid_position (int, int): x and y grid coordinates 
        """
        grid_x, grid_y = grid_position
        return grid_x >= 0 and grid_x < self.columns and grid_y >= 0 and grid_y < self.rows
