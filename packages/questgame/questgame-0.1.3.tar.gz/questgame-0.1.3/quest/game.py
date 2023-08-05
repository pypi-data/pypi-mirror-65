import arcade
from quest.engines import ContinuousPhysicsEngine
from quest.errors import NoMapError, NoLayerError
from quest.sprite import Player
from time import time


class QuestGame(arcade.Window):
    """Implements a top-down video game with a character on a map.

    :py:class:`QuestGame` is the central class in the :doc:`../index`,
    which is built on top of :doc:`arcade:index`. :py:class:`QuestGame`
    is a subclass of :py:class:`arcade:arcade.Window`.
    To create your own game, create a subclass of :py:class:`QuestGame`
    and then override whatever you need to change from the default behavior.

    When :py:class:`QuestGame` is initialized, it sets up the player, the maps,
    the walls, the NPCs, the physics engine, and centers the viewport on the player.
    Rather than overriding :py:meth:`__init__`, consider overriding just the setup
    functions you need to change.

    Attributes:
        screen_width: Width in pixels of the game window.
        screen_height: Height in pixels of the game window.
        left_viewport_margin: Minimum distance (in pixels) between the
            player sprite and the left edge of the viewport.
        right_viewport_margin: Minimum distance (in pixels) between the
            player sprite and the right edge of the viewport.
        bottom_viewport_margin: Minimum distance (in pixels) between the
            player sprite and the bottom edge of the viewport.
        top_viewport_margin: Minimum distance (in pixels) between the
            player sprite and the top edge of the viewport.
        screen_title: Title of the game window (displayed top center)
        player_scaling: Factor by which to scale the player sprite.
        player_sprite_image: Filepath for the player sprite.
        player_speed: In pixels per update. (By default, the game runs
            at 60 hertz, so update is called every 1/60 second.)
        player_initial_x: Initial x-coordinate for player center.
        player_initial_y: Initial y-coordinate for player center.
        view_bottom: y-coordinate of the bottom edge of the current viewport
        view_left: x-coordinate of the left edge of the current viewport
    """
    screen_width = 600
    screen_height = 600
    left_viewport_margin = 100
    right_viewport_margin = 100
    bottom_viewport_margin = 100
    top_viewport_margin = 100
    screen_title = "Quest"
    player_scaling = 1
    player_sprite_image = None
    player_speed = 10
    player_initial_x = 0
    player_initial_y = 0
    view_bottom = 0
    view_left = 0

    def __init__(self):
        """Initializes the game window and sets up other classes.
        """
        super().__init__(self.screen_width, self.screen_height, self.screen_title)
        self.running = False
        self.setup_maps()
        if len(self.maps) > 0:
            self.set_current_map(0)
        self.setup_player()
        self.setup_walls()
        self.setup_npcs()
        self.setup_physics_engine()
        self.center_view_on_player()
        self.current_modal = None

    def run(self):
        """Starts the game.
        """
        self.start_time = time()
        self.running = True
        arcade.run()

    def setup_maps(self):
        """Sets up the game maps.

        self.maps should be assigned to a list of :py:class:`Map` objects, which get
        initialized here. Each map represents a 'level' or 'scene' of the game.
        Once the list of maps is created, use :py:meth:`set_current_map` to
        set one of the maps as the initial current map.
        This method will need to be overridden by any game using a map.
        For more details, see :ref:`creating_maps`
        """
        self.maps = []

    def setup_player(self):
        """Creates the player sprite.

        Initializes a sprite for the player, assigns its starting position,
        and appends the player sprite to a SpriteList (Arcade likes to work
        with sprites in SpriteLists).
        """
        self.player = Player(self.player_sprite_image, self.player_scaling)
        self.player.center_x = self.player_initial_x
        self.player.center_y = self.player_initial_y
        self.player.speed = self.player_speed
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

    def setup_walls(self):
        """Does any neccessary setup for NPCs.
        """
        self.wall_list = arcade.SpriteList()

    def setup_npcs(self):
        """Does any neccessary setup for NPCs.
        """
        self.npc_list = arcade.SpriteList()

    def add_map(self, game_map):
        """Adds a map to the list of maps.

        Arguments:
            game_map: A quest.map.Map object.
        """
        self.maps.append(game_map)
        if len(self.maps) == 1:
            self.set_current_map(0)

    def get_current_map(self):
        """Gets the current game map.

        The current map is tracked using ``current_map_index``.

        Returns:
            The current Map.
        """
        if self.current_map_index is None:
            raise NoMapError("The game has no maps")
        return self.maps[self.current_map_index]

    def set_current_map(self, index):
        """Sets the current game map.

        Checks to make sure ``index`` is valid, and then stores it as
        ``current_map_index``.
        """
        if index < 0 or index >= len(self.maps):
            raise ValueError("Cannot set current map to {}; there are {} maps.".format(
                    index, len(self.maps)))
        self.current_map_index = index

    def setup_physics_engine(self):
        """Sets up the physics engine.

        Initializes the physics engine that will be used in the game.
        A physics engine resolves interactions between sprites according to a
        set of rules. The :doc:`arcade:index` :py:class:`arcade:PhysicsEngineSimple`
        just keeps the player sprite from bumping into walls. More complicated
        physics engines could implement collisions, gravity, or even realistic
        3-dimensional interactions.

        By default, :py:class:`QuestGame` uses :py:class:`arcade:PhysicsEngineSimple`
        to prevent the player sprite from colliding or passing through any
        sprites on a map layer with the ``wall`` role. If there are no
        :py:class:`MapLayer` with the ``wall`` role, uses the
        :py:class:`NullPhysicsEngine` instead. Don't override this method
        unless you understand Arcade's physics engines pretty well.
        """
        self.physics_engine = ContinuousPhysicsEngine(self)

    def on_update(self, delta_time):
        """Updates the game's state.

        At every tick, the game needs to be updated. The physics engine
        updates sprite positions, and then sprite callbacks are executed.
        Finally, the viewport is scrolled. Note that `on_update` changes the
        state of the game, but does not draw anything to the screen.

        Args:
            delta_time: How much time has passed since the last update.
        """
        if self.running:
            for npc in self.npc_list:
                npc.on_update(self)
            self.physics_engine.update()
            self.scroll_viewport()

    def on_draw(self):
        """Draws the screen.

        At every tick, just after `on_update`, the whole screen needs to be
        redrawn. This involves drawing the background color, each map layer
        with the `display` role, the NPC's, the player, and any message that
        needs to be displayed.
        """
        arcade.start_render()
        arcade.set_background_color(self.get_current_map().background_color)
        for layer in self.get_current_map().layers:
            layer.draw()
        self.npc_list.draw()
        self.player_list.draw()
        message = self.message()
        if message:
            arcade.draw_text(message, 10 + self.view_left, 10 + self.view_bottom,
                    arcade.csscolor.WHITE, 18)
        if self.current_modal:
            self.current_modal.on_draw()

    def open_modal(self, modal):
        """Shows a modal window and pauses the game until the modal resolves.
        """
        self.running = False
        self.current_modal = modal
        self.current_modal.update_position(
            self.view_left + self.screen_width / 2,
            self.view_bottom + self.screen_height / 2,
        )

    def close_modal(self):
        """Resolves a modal window and resumes the game.
        """
        self.current_modal = None
        self.running = True

    def on_key_press(self, key, modifiers):
        """Handles key presses.

        Arguments:
            key: The key that was pressed.
            modifiers: A list of currently-active modifier keys (e.g. shift).

        While a key is pressed, the sprite's x- and y- change values are set
        to the player's movement speed. Think of this as an intention to move;
        it's up to the physics engine to decide whether this actually
        results in movement. For example, the physics engine will prevent
        players from moving into walls. This method is automatically called at
        the appropriate time.
        """
        if self.current_modal:
            self.current_modal.on_key_press(key, modifiers)
        else:
            if key == arcade.key.UP or key == arcade.key.W:
                self.player.change_y = self.player.speed
            elif key == arcade.key.DOWN or key == arcade.key.S:
                self.player.change_y = -self.player.speed
            if key == arcade.key.LEFT or key == arcade.key.A:
                self.player.change_x = -self.player.speed
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.player.change_x = self.player.speed

    def on_key_release(self, key, modifiers):
        """Handles key releases.

        Arguments:
            key: The key that was released.
            modifiers: A list of currently-active modifier keys (e.g. shift).

        Whenever a key is released, the player's change_x or change_y
        is set to 0, indicating that the player no longer intends to keep
        moving. This method is automatically called at the appropriate time.
        """
        if self.current_modal:
            self.current_modal.on_key_release(key, modifiers)
        else:
            if key == arcade.key.UP or key == arcade.key.W:
                self.player.change_y = 0
            elif key == arcade.key.DOWN or key == arcade.key.S:
                self.player.change_y = 0
            elif key == arcade.key.LEFT or key == arcade.key.A:
                self.player.change_x = 0
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.player.change_x = 0

    def center_view_on_player(self):
        """Centers the viewport on the player.
        """
        self.view_left = self.player.center_x - self.screen_width / 2
        self.view_bottom = self.player.center_y - self.screen_height / 2
        self.update_viewport()
        self.scroll_viewport()

    def scroll_viewport(self):
        """Updates the viewport to keep the player within margins.

        If the player sprite is too close to any edge of the viewport
        (or has somehow gone beyond the viewport), scrolls the viewport
        to the player. The {left, right, bottom, top}_viewport_margin
        properties specify how close the player is allowed to be to the
        edge before scrolling.
        """

        changed = False

        left_boundary = self.view_left + self.left_viewport_margin
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        right_boundary = self.view_left + self.screen_width - self.right_viewport_margin
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        top_boundary = self.view_bottom + self.screen_height - self.top_viewport_margin
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        bottom_boundary = self.view_bottom + self.bottom_viewport_margin
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)
            self.update_viewport()

    def update_viewport(self):
        """Updates the viewport.

        Uses the `view_left`, `view_bottom`, and the screen size
        properties to update the viewport. Needs to be called after
        changing any of these properties.
        """
        arcade.set_viewport(
            self.view_left,
            self.screen_width + self.view_left,
            self.view_bottom,
            self.screen_height + self.view_bottom
        )

    def message(self):
        """Generates a message (or no message) to be shown on screen.

        Returns:
            A string to be shown on screen, or None if no message is needed.
        """
        return None
