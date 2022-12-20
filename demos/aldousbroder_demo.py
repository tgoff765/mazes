from maze_creator.maze import Maze, MazeType

if __name__ == "__main__":
    # Can create a maze and print ASCII representation
    maze = Maze(MazeType.ALDOUSBRODER, columns=100, rows=100)
    maze.draw()
