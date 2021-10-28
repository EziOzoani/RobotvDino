The ``database`` module
======================

Using ``Game.create_game``
----------------------

This is the test file for database classes. First import ``Game`` from the ``database`` module:

    >>> from database import Game

Create a new game, new robot and new dinosaurs in diferent places, then save it in the database.


Dinosaurs position list must have the same dinosaurs positions as indicated in number of dinosaurs
    >>> Game.create_game(grid_cols=10, grid_rows=10, num_dinos=5, dinos_pos=[[1, 2], [3, 4], [4, 5]], robot_pos=[0, 0])
    Traceback (most recent call last):
        ...
    ValueError: Dinosaurs positions array length must be equal to num_dinos


The grid of the game can not have less than 10 grid columns
    >>> Game.create_game(grid_cols=1, grid_rows=10, num_dinos=3, dinos_pos=[[1, 2], [3, 4], [4, 5]], robot_pos=[0, 0])
    Traceback (most recent call last):
        ...
    ValueError: Grid columns must be greater than 10 and lower than 51


The grid of the game can not have less than 10 grid rows
    >>> Game.create_game(grid_cols=10, grid_rows=1, num_dinos=3, dinos_pos=[[1, 2], [3, 4], [4, 5]], robot_pos=[0, 0])
    Traceback (most recent call last):
        ...
    ValueError: Grid rows must be greater than 10 and lower than 51


Two entities can not be in the same place
    >>> Game.create_game(grid_cols=10, grid_rows=30, num_dinos=3, dinos_pos=[[1, 2], [3, 4], [4, 5]], robot_pos=[1, 2])
    Traceback (most recent call last):
        ...
    ValueError: Two entities (Robot and dinosaurs) can not be in the same place
    >>> Game.create_game(grid_cols=10, grid_rows=30, num_dinos=3, dinos_pos=[[1, 2], [1, 2], [4, 5]], robot_pos=[1, 5])
    Traceback (most recent call last):
        ...
    ValueError: Dinosaur position can not be repeated