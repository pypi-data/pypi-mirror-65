import arcade
from arcade.sprite_list import SpriteList, _check_for_collision
from arcade import check_for_collision_with_list
from itertools import chain, combinations
from collections import defaultdict
from easing_functions import LinearInOut
from quest.helpers import Direction, SpriteListList, scale
from time import time
from math import sqrt

class QuestPhysicsEngine:
    """Base class for Quest Physics Engines

    The engine is initialized with a :py:class:`QuestGame` instance, which
    the engine uses to access sprites. Quest's physics engines make some assumptions
    about the structure of a game in order to simplify logic. It is assumed that the
    game has attributes `player_list`, `wall_list`, and `npc_list`. Players and NPCs will
    be moved according to their `change_x` and `change_y` attributes; walls will not move.
    When players or NPCs collide with walls, they are pushed back until they are no longer
    colliding. When players or NPCs collide with each other, their `on_collision` methods
    are called, but they are not automatically repelled. If you want players or NPCs to be
    repelled from each other, see :py:class:`quest.examples.grandmas_soup.Grandma`. Time-based
    updates are optionally implemented using the argument `time` which defaults to False.

    Args:
        game (QuestGame): The game to which the engine will be attached.
    """
    max_darkness = 100

    def __init__(self, game, time=False, time_cycle_secs=30):
        self.game = game
        self.player_list=game.player_list
        self.wall_list=game.wall_list
        self.npc_list=game.npc_list
        all_sprite_lists = [self.player_list, self.wall_list, self.npc_list]
        curr_map = self.game.get_current_map()
        for layer in curr_map.layers:
            all_sprite_lists.append(layer.sprite_list)
        self.all_sprites = SpriteListList(all_sprite_lists)
        self.time = time
        self.time_cycle_secs = time_cycle_secs

    def update(self, game):
        """Updates game based on time the game has run if the time option is set. Otherwise,
        waits for implementation from a more complex physics engine like py:class:`ContinuousPhysicsEngine`
        """
        if self.time:
            self.time_updates()

    def time_updates(self):
        self.update_sprites_for_time()

    def update_sprites_for_time(self):
        """Calculates shade by converting the time passed since the start of the game to a percentage
        of the current day/night cycle.
        """
        time_since_start = time()-self.game.start_time
        curr_mod = time_since_start%self.time_cycle_secs
        grade = abs(curr_mod - self.time_cycle_secs/2) / (self.time_cycle_secs/2)
        color_value = grade*(255-self.max_darkness) + self.max_darkness
        for sprite in self.all_sprites:
            sprite.color = (color_value, color_value, color_value)

    def player(self):
        return self.player_list.sprite_list[0]

class ContinuousPhysicsEngine(QuestPhysicsEngine):
    """A continuous physics engine allows sprites to be at any point.

    This implementation is simple but inefficient. It may be problematic with
    more complex games. If we run into trouble, first try using spatial hashes
    to resolve collisions.
    """
    def __init__(self, game, **kwargs):
        super().__init__(game, **kwargs)
        self.non_wall_list = SpriteListList([self.player_list, self.npc_list])

    def update(self):
        """Updates sprite positions and handles collisions.
        """
        super().update(self.game)
        self.update_sprite_positions()
        self.resolve_collisions_with_walls()
        self.resolve_collisions_between_nonwalls()

    def update_sprite_positions(self):
        """Updates sprite positions using their `change_x` and `change_y` attributes.
        """
        for moving_sprite in self.non_wall_list:
            moving_sprite.center_x += moving_sprite.change_x
            moving_sprite.center_y += moving_sprite.change_y

    def resolve_collisions_with_walls(self):
        """Resolves collisions between every sprite and every wall.
        """
        for moving_sprite in self.non_wall_list:
            if moving_sprite.change_x == 0 and moving_sprite.change_y == 0:
                continue
            wall_collisions = check_for_collision_with_list(moving_sprite, self.wall_list)
            for wall in wall_collisions:
                moving_sprite.on_collision(wall, self.game)
                wall.on_collision(moving_sprite, self.game)
                self.resolve_sprite_wall_collision(moving_sprite, wall)

    def resolve_sprite_wall_collision(self, sprite, wall):
        """Stops the sprite and backs it away from the wall until they are no longer colliding.

        The distance by which the sprite backs up doubles until they are no longer colliding.
        Note that this does not handle the case in which backing away from one wall means
        it hits another wall (e.g. in a narrow passageway). This will be handled on the subsequent
        update. We can write more complex code if it becomes necessary.
        """
        sprite.stop()
        repel_distance = 1
        away = (wall.center_x - sprite.center_x, wall.center_y - sprite.center_y)
        while _check_for_collision(sprite, wall):
            away_x, away_y = scale(away, repel_distance)
            sprite.center_x = sprite.center_x - away_x
            sprite.center_y = sprite.center_y - away_y
            repel_distance *= 2

    def resolve_collisions_between_nonwalls(self):
        """For every pair of nonwall sprites, resolves collisions.
        """
        for sprite0, sprite1 in combinations(self.non_wall_list, 2):
            if _check_for_collision(sprite0, sprite1):
                sprite0.on_collision(sprite1, self.game)
                sprite1.on_collision(sprite0, self.game)

class DiscretePhysicsEngine(QuestPhysicsEngine):
    """A physics engine which snaps sprite movement to specific gridpoints.

    Some games work better when sprites occupy specific tiles, rather than
    having continuous positions. This can make it easier to think about
    relationships between sprites (for example, to calculate which are
    adjacent, or to plan a route). :py:class:`DiscretePhysicsEngine` handles
    sprite movement in a discrete way, while animating sprites' transitions
    from tile to tile.

    Args:
        player_sprite (arcade.Sprite):
        dynamic_sprite_lists (bool): Whether new sprites might be added
            to sprite lists during the game. Performance is better when
            False. Default True.

    Attributes:
        tile_transition_cutoff (float): Parametric t value at which a sprite's
            current tile should shift to the

    """

    tile_transition_cutoff = 0.5
    easing_class = LinearInOut

    def __init__(self, game, grid_map_layer, diagonal=True, check_for_new_sprites=True, **kwargs):
        super().__init__(game, **kwargs)
        self.grid = grid_map_layer
        self.diagonal = diagonal
        self.easing = self.easing_class()
        self.check_for_new_sprites = check_for_new_sprites
        sprite_lists = [self.player_list, self.wall_list, self.npc_list]
        self.all_nonbackground_sprites = SpriteListList(sprite_lists)
        self.dynamic_sprites = SpriteListList([l for l in sprite_lists if not l.is_static])
        self.ensure_sprite_metadata(all_sprites=True)
        self.tile_positions = defaultdict(list)
        for sprite in self.all_nonbackground_sprites:
            self.tile_positions[sprite.current_tile].append(sprite)

    def update(self):
        super().update(self.game)
        if self.check_for_new_sprites:
            self.ensure_sprite_metadata()
        for sprite in self.dynamic_sprites:
            if (sprite.change_x or sprite.change_y) and not sprite.moving:
                self.begin_move(sprite)
            elif sprite.moving:
                self.continue_move(sprite)

    def begin_move(self, sprite):
        direction = Direction.from_vector((sprite.change_x, sprite.change_y), self.diagonal)
        ox, oy = sprite.origin_tile
        vx, vy = direction.to_vector()
        destination = (ox + vx, oy + vy)
        if self.grid.position_in_grid(destination):
            wall = self.get_wall(self.tile_positions[destination])
            if wall:
                self.player().on_collision(wall, self.game)
                wall.on_collision(self.player(), self.game)
            else:
                sprite.moving = True
                sprite.move_start = time()
                sprite.t = 0
                sprite.move_direction = direction
                sprite.destination_tile = destination

    def continue_move(self, sprite):
        duration = 1 / sprite.speed
        if sprite.move_direction.is_diagonal():
            duration *= sqrt(2)
        sprite.t = self.ease((time() - sprite.move_start) / duration)
        if sprite.t >= self.tile_transition_cutoff:
            self.tile_positions[sprite.current_tile].remove(sprite)
            sprite.current_tile = sprite.destination_tile
            for other_sprite in self.tile_positions[sprite.current_tile]:
                sprite.on_collision(other_sprite, self.game)
                other_sprite.on_collision(sprite, self.game)
            self.tile_positions[sprite.current_tile].append(sprite)
        if sprite.t >= 1.0:
            self.end_move(sprite)
        else:
            p0 = self.grid.get_pixel_position(sprite.origin_tile)
            p1 = self.grid.get_pixel_position(sprite.destination_tile)
            sprite.center_x, sprite.center_y = self.interpolate(p0, p1, sprite.t)

    def end_move(self, sprite):
        sprite.moving = False
        sprite.center_x, sprite.center_y = self.grid.get_pixel_position(sprite.destination_tile)
        sprite.origin_tile = sprite.current_tile = sprite.destination_tile

    def get_wall(self, sprite_list):
        for sprite in sprite_list:
            if sprite in self.wall_list:
                return sprite

    def interpolate(self, p0, p1, t):
        (x0, y0), (x1, y1) = p0, p1
        return x0 + (x1 - x0) * t, y0 + (y1 - y0) * t

    def ease(self, x):
        return self.easing.ease(x)

    def ensure_sprite_metadata(self, all_sprites=False):
        sprites = self.all_nonbackground_sprites if all_sprites else self.dynamic_sprites
        for sprite in sprites:
            if not hasattr(sprite, 'current_tile'):
                sprite.origin_tile = self.grid.get_grid_position((sprite.center_x, sprite.center_y))
                sprite.current_tile = sprite.origin_tile
                sprite.destination_tile = None
                sprite.move_start = None
                sprite.moving = False
                sprite.t = None
