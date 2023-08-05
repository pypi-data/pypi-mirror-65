from random import random
from math import tau, sin, cos

class Strategy:
    """A Strategy represents how a sprite responds to the environment. 

    It is useful to extract :py:class:`Strategy` as a separate class (rather than
    making it part of the NPC class) because there might be many sprites in a game
    which need to use the same strategy. In the default implementation of 
    :py:meth:`quest.sprite.NPC.on_update`, the NPC will set its course using its 
    :py:class:`Strategy` if it has one. 
    """

    def choose_course(self, sprite, game):
        """Returns a (x, y) vector representing the chosen course.

        In the default implementation, returns (0, 0) which will cause the sprite to
        stop. To create new strategies, override this method and define helper methods
        as necessary.

        Arguments:
            sprite: The sprite who is about to act.
            game: The game object (to access attributes useful in choosing the course).
        """
        return (0, 0)

class RandomWalk(Strategy):
    """ A strategy which causes the sprite to walk randomly, with some chance 
    of changing direction at each step.

    Arguments:
        change_prob (float): The probability (between 0 and 1) that the sprite will choose
        a new direction on a step.
    """
    def __init__(self, change_prob=0.1):
        self.change_prob = change_prob
        self.set_random_direction()

    def choose_course(self, sprite, game):
        """Possibly chooses a new random direction, then returns the current direction.

        Arguments:
            sprite: The sprite who is about to act.
            game: The game object (to access attributes useful in choosing the course).
        """
        if random() < self.change_prob:
            self.set_random_direction()
        return (self.x, self.y)

    def set_random_direction(self):
        """Sets attributes `x` and `y` to a random (x, y) direction. 

        Think of this as choosing a random point on a circle. Tau is another 
        word for 2 * pi, which represents the angle measure of the full circle, so 
        if we multiply it by `random()` (which returns a random number evenly distributed 
        between 0 and 1), we get a randomly-chosen angle measure between 0 and the full circle. 
        Then we can use cosine and sine to get the x and y components of this point.
        """
        r = random() * tau
        self.x = cos(r)
        self.y = sin(r)

class DividedStrategy(Strategy):
    """Builds a complex strategy based on two existing strategies and transition probabilities.

    One way to get more complex behavior is to define two simpler behaviors, and then to have a 
    certain probability of switching between them. For example, some games have enemy NPCs which 
    sometimes chase the player and other times wander around randomly. The transition probabilities
    (the chance of switching) are not symmetric. For example, you might want to define a game where 
    sprites have a low chance of going from normal to desperate, and then zero chance of going from
    desperate back to normal. The idea of composing strategies from other strategies is an example of 
    functional programming.

    This pattern could be extended to `n` strategies, with a matrix of `n * n` transition probabilities.
    This more general case is called a Markov chain, and gets used quite a lot in computer science. 

    Arguments:
        strategy_a (:py:class:`Strategy`): The initial strategy.
        strategy_b (:py:class:`Strategy`): A second strategy.
        ab_prob (float): The probability of switching from strategy a to strategy b.
        ba_prob (float): The probability of switching from strategy b to strategy a.
    """

    def __init__(self, strategy_a, strategy_b, ab_prob, ba_prob):
        self.strategy_a = self.current_strategy = strategy_a
        self.strategy_b = strategy_b
        self.ab_prob = ab_prob
        self.ba_prob = ba_prob

    def choose_course(self, sprite, game):
        """Possibly switch strategies, and then have the current strategy handle choosing the course.

        Arguments:
            sprite: The sprite who is about to act.
            game: The game object (to access attributes useful in choosing the course).
        """
        self.consider_switching_strategy()
        return self.current_strategy.choose_course(sprite, game)

    def consider_switching_strategy(self):
        """Possibly switch strategy (using transition probabilities).
        """
        if self.current_strategy is self.strategy_a:
             if random() < self.ab_prob:
                self.current_strategy = self.strategy_b
        else:
            if random() < self.ba_prob:
                self.current_strategy = self.strategy_a
