from maze_creator.maze import Maze, MazeType

if __name__ == "__main__":
    maze = Maze(MazeType.HUNTANDKILL, columns=50, rows=50)

    # Add another view on top of our existing maze
    maze.draw()
