from src.core.maze import Maze, MazeType

if __name__ == "__main__":
    maze = Maze(MazeType.WILSON,
                columns=40,
                rows=40)
    maze.solve()
    maze.draw()





