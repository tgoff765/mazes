from src.core.maze import Maze, MazeType

if __name__ == "__main__":
    maze = Maze(MazeType.BINARY,
                columns=100,
                rows=100,
                horizontal_bias=0.45)

    # Add another view on top of our existing maze
    maze.draw()



