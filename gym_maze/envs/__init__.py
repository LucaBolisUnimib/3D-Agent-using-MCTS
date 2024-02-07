from maze_env import *
from maze_view_2d import MazeView2D

if __name__ == "__main__":

    #mazeEnv = MazeEnv("maze2d_10x10.npy")
    maze = MazeView2D(screen_size= (500, 500), maze_file_path= "maze2d_10x10.npy", maze_size=(10,10))
    #view = MazeView2D("maze_file_path = maze_saples/maze2d_10x10.npy")
    while True: 
        maze.update()
        #maze.move_robot()
    #input("Enter any key to quit.")