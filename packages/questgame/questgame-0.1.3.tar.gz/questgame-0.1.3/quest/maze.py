from collections import defaultdict
import random

def is_even(x):
    "Returns True if x is even, otherwise False."
    return x % 2 == 0

def is_odd(x):
    "Returns True if x is odd, otherwise False."
    return not is_even(x)

class Maze:
    """Generates a maze stored in a 2-dimensional array.

    This class generates a maze. The mathematical definition of a maze is a set 
    of paths that are connected so that there is exactly one way to go between 
    any two points. Here's an example::

        >>> from quest.maze import Maze
        >>> m = Maze(55, 15)
        >>> m.generate()
        >>> print(m)

        ╔═══════════════╦═════╦═════════╦═════════╦═══════╦═══╗
        ║               ║     ║         ║         ║       ║   ║
        ║ ╔═════════╦══ ║ ══╗ ║ ║ ══╦══ ╚═══╦══ ║ ║ ╔═══╗ ╠══ ║
        ║ ║         ║   ║   ║   ║   ║       ║   ║   ║   ║ ║   ║
        ║ ║ ╔═════╗ ║ ║ ╚═╗ ╚═╦═╩═╗ ╚═╦═══╗ ║ ╔═╩═══╝ ║ ║ ║ ══╣
        ║ ║ ║     ║ ║ ║   ║   ║   ║   ║   ║   ║       ║ ║ ║   ║
        ║ ║ ║ ╔═╗ ║ ║ ╠═══╝ ╔═╝ ║ ║ ║ ║ ║ ╚═══╣ ══╗ ╔═╩═╝ ╠══ ║
        ║ ║ ║ ║ ║ ║ ║ ║     ║   ║ ║ ║ ║ ║     ║   ║ ║     ║   ║
        ║ ║ ║ ║ ║ ║ ║ ║ ══╦═╝ ╔═╝ ╠═╝ ║ ╚═══╗ ╠══ ║ ║ ╔═══╣ ║ ║
        ║ ║     ║ ║ ║     ║   ║   ║   ║     ║ ║   ║   ║   ║ ║ ║
        ╠═╩═════╝ ║ ╠═══╦═╝ ╔═╣ ╔═╝ ╔═╩═╦══ ║ ║ ╔═╩═══╝ ║ ║ ╚═╣
        ║         ║ ║   ║   ║ ║ ║   ║   ║   ║   ║       ║ ║   ║
        ║ ╔═══════╝ ║ ║ ║ ╔═╝ ║ ╚══ ║ ══╝ ══╩═══╩════ ╔═╝ ╚══ ║
        ║ ║           ║   ║         ║                 ║       ║
        ╚═╩═══════════╩═══╩═════════╩═════════════════╩═══════╝

    There are many different algorithms for generating mazes, and they tend to 
    produce mazes with different characteristics. This class implements a 
    `depth-first search <http://algostructure.com/specials/maze.php>`_ maze 
    generation algorithm, which tends to produce long corridors without much
    branching. See :py:meth:`generate` for a description of how this works.

    Args:
        columns: the number of columns in the maze (including edge walls).
        rows: the number of rows in the maze (including edge walls).

    .. _depth-first search: http://algostructure.com/specials/maze.php
    """

    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows

    def generate(self, seed=None):
        """Generates (or re-generates) a random maze.

        We are always going to keep track of a current point and we're going
        to keep a list of points that have been visited. Every time a point 
        becomes the current point, we will add it to `visited`. Also, every
        time we move to a new current point, we add the old current point to a 
        stack. This becomes a history of where we have been. 

        Now we see if the current point has any neighbors that have not yet been 
        visited. If so, choose one randomly, make it the current point, and 
        repeat. Now the maze is growing like a worm, one point at a time. At 
        some point, though, the growing worm will get stuck in a dead end, where
        the current point has no unvisited neighbors. It can't grow anymore.

        This is where the history stack comes in. Since the maze can't grow from
        the current point, let's pop the most recent point off the history stack
        and make that the current point instead. If that point has unvisited
        neighbors, great: we can continue. Otherwise, keep popping points off
        the history stack until we find one that has unvisited neighbors. 

        When does this end? Once the history stack is empty. That means we have
        worked our way all the way back to the starting point, and no points 
        have any unvisited neighbors remaining. This means the maze has filled
        up its whole world so it's finished!

        If you want to see this in action, 
        `here <http://algostructure.com/specials/maze.php>`_ is a website with 
        several different maze-generation algorithms. Choose 
        "Flood fill/Depth-first."

        Args:
            seed: If provided, sets the random seed. (Random numbers on 
                computers are not really random, they're just hard to predict. If
                you set the random seed to the same value, you'll get the same set
                of random numbers every time. This is helpful when you want to get
                the same random maze.)
        """
        if seed:
            random.seed(seed)
        self.links = defaultdict(set)
        visited = set()
        stack = [(1, 1)]
        current_point = (1, 1)
        while len(stack) > 0:
            visited.add(current_point)
            unvisited_neighbors = [n for n in self.neighbors(current_point) if n not in visited]
            if len(unvisited_neighbors) > 0:
                next_point = random.choice(unvisited_neighbors)
                self.connect(current_point, next_point)
                stack.append(current_point)
                current_point = next_point
            else:
                current_point = stack.pop()

    def generate_fully_connected_maze(self):
        """Generates a maze where every node is connected to all its neighbors.
        """
        self.links = defaultdict(set)
        x = 1
        while x < self.columns:
            y = 1
            while y < self.rows:
                for n in self.neighbors((x, y)):
                    self.links[(x, y)].add(n)
                y += 2
            x += 2

    def connect(self, p0, p1):
        """Connects two points by storing each in the other's list of links.

        Args:
            p0: A point, which is represented as a tuple of (x, y) coordinates.
            p1: Another point, also a tuple.
        """
        self.links[p0].add(p1)
        self.links[p1].add(p0)
                
    def connected(self, p0, p1):
        """Checks whether two points are connected as neighbors.

        Args:
            p0: A point, which is represented as a tuple of (x, y) coordinates.
            p1: Another point, also a tuple.

        Returns:
            True if the points are connected, otherwise False.
        """
        return p1 in self.links[p0]

    def neighbors(self, point):
        """Gets a list of the point's neighbors.

        The points we care about are those with odd coordinates,
        like (1, 1) and (5, 7). Let's call these points nodes. They 
        are represented with stars in the diagrams below. 

        The reason nodes are on the odd coordinates is because we need
        to leave room for walls between points in the maze, and surrounding
        the maze. 
        ::

            ╔═══════╗   ╔═══════╗   ╔═══════╗
            ║* * * *║   ║* * * *║   ║       ║
            ║ ┼ ┼ ┼ ║   ╠═════╗ ║   ╠═════╗ ║
            ║* * * *║   ║* * *║*║   ║     ║ ║
            ║ ┼ ┼ ┼ ║   ║ ╔══ ║ ║   ║ ╔══ ║ ║
            ║* * * *║   ║*║* *║*║   ║ ║   ║ ║
            ║ ┼ ┼ ┼ ║   ║ ║ ══╝ ║   ║ ║ ══╝ ║
            ║* * * *║   ║*║* * *║   ║ ║     ║
            ╚═══════╝   ╚═╩═════╝   ╚═╩═════╝

        Args:
            point: A tuple of (x, y) coordinates.

        Returns:
            A list of nodes two spaces to the left, right, down, and up from 
            the given point, as long as they are in bounds.
        """
        x, y = point
        possible_neighbors = [(x+2, y), (x-2, y), (x, y+2), (x, y-2)]
        return [n for n in possible_neighbors if self.is_in_bounds(n)]

    def is_in_bounds(self, point):
        """Checks whether a point is in bounds.

        Returns:
            True if the point is in bounds, otherwise False.
        """
        x, y = point
        return x >= 0 and x < self.columns - 1 and y >= 0 and y < self.rows - 1

    def get_walls(self):
        """Returns a list of points containing walls in the current maze.
        
        To find all the walls, we just loop through every (x, y) point in the 
        maze and check if it's a wall. First off, all the points around the 
        edges must be walls. Then, If both a point's x and y coordinates are 
        odd, the point is definitely not a wall (See :py:meth:`neighbors`).
        If both a point's coordinates are even, it is definitely a wall.
        For points with one even and one odd coordinate, we need to check the
        links to see whether the point has been chosen as a link. Otherwise, 
        it's a wall.

        Returns:
            A list of (x, y) tuples for wall spaces in the maze.
        """
        walls = []
        for i in range(self.columns):
            for j in range(self.rows):
                if i == 0 or i == self.columns - 1 or j == 0 or j == self.rows - 1:
                    walls.append((i, j))
                elif is_even(i) and is_even(j):
                    walls.append((i, j))
                elif is_even(i) and (i+1, j) not in self.links[(i-1, j)]:
                    walls.append((i, j))
                elif is_even(j) and (i, j+1) not in self.links[(i, j-1)]:
                    walls.append((i, j))
        return walls

    def __str__(self, nodes=False):
        """Produces a string representation of the maze (example above).

        Since the maze is stored in an array of arrays, we can just turn each 
        array (row of the maze) into a string and then join the rows together 
        with newline characters.

        Args:
            nodes: If True, points that are nodes (see :py:meth:`neighbors`)
                will be shown as stars.

        Returns:
            A multiline string representation of the maze.
        """
        walls = set(self.get_walls())
        rows = []
        for j in reversed(range(self.rows)):
            row = [self.str_char((i, j), walls, nodes) for i in range(self.columns)]
            rows.append(''.join(row))
        return "\n".join(rows)

    def str_char(self, point, walls, nodes=False):
        """Determines which character should represent a point in the maze.

        Args:
            point: A (x, y) tuple.
            walls: A list of (x, y) tuples.
            nodes: If True, points that are nodes (see :py:meth:`neighbors`)
                will be shown as stars.
        """
        x, y = point
        symbols = " ═║╚══╝╩║╔║╠╗╦╣╬"
        code = 0
        if nodes and is_odd(x) and is_odd(y):
            return '*'
        if (x, y) in walls:
            if (x+1, y) in walls:
                code += 1
            if (x, y+1) in walls:
                code += 2
            if (x-1, y) in walls:
                code += 4
            if (x, y-1) in walls:
                code += 8
        return symbols[code]

if __name__ == '__main__':
    m = Maze(99, 99)
    m.generate()
    print(m)
