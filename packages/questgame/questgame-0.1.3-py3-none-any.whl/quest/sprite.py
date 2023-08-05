from arcade.sprite import Sprite
from arcade import calculate_points
from quest.helpers import scale

class QuestSprite(Sprite):
    """The base class for sprites in Quest.

    A :py:class:`QuestSprite` is a subclass of :py:class:`arcade.Sprite` with a 
    few additional methods to help integrate into the Quest framework. 

    Attributes:
        description: A string description of the sprite.
        strategy: If set, should be a :py:class:`quest.strategy.Strategy`, or another class 
            instance with a :py:meth:`choose_course` method. 
        speed: The sprite's speed.

    Arguments:
        filename: The only required argument is the name of the sprite's image file. 
        kwargs: There are many optional keyword arguments inherited from :py:class:`arcade.Sprite`.
    """
    description = "quest sprite"
    strategy = None
    speed = 1

    def set_course(self, vector):
        """Update the `change_x` and `change_y` properties using a vector.

        Normally, sprites' intended movement is set using the `change_x` and `change_y` 
        properties. This method updates `change_x` and `change_y` based on an (x, y) vector
        whose magnitude is scaled to the sprite's speed. This is helpful when you have an 
        (x, y) vector, for example a :py:class:`quest.helpers.Direction` or a vector to another
        sprite, and want to have this sprite head that direction at its speed. For example, if you wanted
        a sprite to always try to move down at its speed::
        
                def on_update(self):
                    self.set_course(Direction.DOWN.to_vector())

        """
        vx, vy = scale(vector, self.speed)
        self.change_x = vx
        self.change_y = vy

    def stop(self):
        """Set the sprite's `change_x` and `change_y` to zero.
        """
        self.change_x = 0
        self.change_y = 0

    def on_collision(self, other_sprite, game):
        """Called when the sprite collides with another sprite. 
        
        Override this method to change the sprite's collision behavior. 
        For example, an NPC sprite which represents an item that can be collected
        by the player would probably call a method on `game` to update the inventory
        and then call :py:meth:`self.kill()`.  
        """
        pass

    def on_update(self, game):
        """Called on every tick, performs any needed updates.

        By default, if the sprite has a strategy, it uses the strategy 
        to set its course.
        """
        if self.strategy:
            self.set_course(self.strategy.choose_course(self, game))

    def __str__(self):
        return "<{}>".format(self.description)


class Wall(QuestSprite):
    """Wall.
    """
    description = "wall"

class Player(QuestSprite):
    """Player
    """
    description = "player"

class NPC(QuestSprite):
    """Non-playable character
    """
    description = "npc"

class Background(QuestSprite):
    """A sprite that does nothing.
    """
    description = "background"
