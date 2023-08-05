# Quest

Quest provides a simpler interface to python's Arcade library. 

## Installation

Quest runs on Python3. Quest will be distributed on PyPI, so that you can install it with pip. But for now, you have to install it manually. 
As usual, a virtual env is recommended but not required.

    $ python3 -m venv env
    $ source env/bin/activate
    $ git clone https://github.com/cproctor/quest.git
    $ cd quest
    $ pip install -r requirements.txt
    $ pip install -e .
    $ cd quest/examples
    $ python maze_demo.py
    
The point is to subclass the classes provided in the framework to make your own game. There will be documentation explaining how all the code works, but it doesn't exist yet. So you'll just have to read the source!

## Creating sprites and maps
- [Tiled](https://www.mapeditor.org/)
- [Tileset resources](https://opengameart.org/content/best-orthogonal-rectangular-tilesets-for-tilemaps)
- [Piskel](https://www.piskelapp.com) for drawing sprites

## TODO 
- Test case: Create beast game.
    - TilePhysicsEngine
    - NPC Strategy
        - Wrap sprites in simpler class (including animated textures, sounds, callbacks)
        - Doesn't currently work.
- Write documentation

## Pedagogy

### Goals

#### Skills
- Object-oriented programming
  - classes
  - inheritance
- Tick-based time system
- Introductory algorithms
  - terrain/maze generation
  - NPC behavior
- Using logging for evaluation

#### Practices

- Collaboration (students will work in groups to create a game)
- Planning (especially considering alternative possible implementations)
- Reading documentation
- Reading source code; navigating multiple-file projects
- Subclassing to change behavior of exisiting system

### Possible Activities

- Have students trace inheritance chain of classes, list method instances.
- Have students trace call execution through class methods
- Have students implement subclasses using method hooks
- Observe default behavior of existing framework and tracing the codebase to find where 
- Make trivial changes via subclassing. Each can be achieved by adding a single property:
	- change the player sprite filename
	- scale the player sprite to be larger or smaller. 
	- change the player speed
- Make small changes by overriding methods (with low task complexity)
	- change the input keys 
	- add a "run" mode: the character goes faster while spacebar is pressed
  - load a different map (eg load a Maze map but change the number of stars)
- Plan possible implementation strategies
	- Give students a list of possible game mechanics (eg an enemy chases you; add an inventory; moving between maps; a way to win the game; a key unlocks a door) and have them write a plan of what could be overridden/extended to make it happen. 
- As groups start developing games, brainstorm needed features as a class, and collaborate on implementing them. (This will reward good design, as we want an inventory system or an enemy behavior system that can work for everyone.)


