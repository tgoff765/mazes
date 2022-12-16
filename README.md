## Intro 
Work in progress python implementation of the maze generating algorithms explained in Jamis Buck's [Mazes For Programmers](https://pragprog.com/titles/jbmaze/mazes-for-programmers/)

## Requirements 
Checkout the code to your machine and using virtual environment pip install the Pillow Library (used for image rendering)

## Quick Start
Using the `maze` class (from `src.core.maze`) to create a maze using one of the maze-generating algorithms 
- e.g. `maze = Maze(MazeType.ALDOUSBRODER, columns=100,rows=100)` creates a maze of size 100x100 using the aldous-broder algorithm

Once a maze has been created the following methods can be used:
- `draw`: Render the maze as a PNG image 
- `solve`: Calculate the shortest distance path between two points in the graph. Calling draw again will render the graph with the path traced. 
- `analyze`: Render the maze, shading in every cell according to its distance from a starting cell (see images for examples). 

## Update Log 
- 2022-12-16: Initial release