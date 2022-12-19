from maze_creator.core.maze import Maze, MazeType

if __name__ == "__main__":
    maze = Maze(MazeType.SIDEWINDER, columns=150, rows=150, horizontal_bias=0.45)
    maze.analyze()
