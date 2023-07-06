import tkinter as tk

class UnicornHDSimulator:
    def __init__(self, grid):
        self.grid = grid

        # Create the main window
        self.window = tk.Tk()
        self.window.title("Unicorn HD HAT Simulator")

        # Create a canvas to display the grid
        self.canvas = tk.Canvas(self.window, width=320, height=320, bg="black")
        self.canvas.pack()

        # Define the size of each pixel in the grid
        self.pixel_size = 20

        # Start the GUI event loop
        self.window.after(0, self.update_display)
        self.window.mainloop()

    # Function to update the display
    def update_display(self):
        print("Updating display")
        self.canvas.delete("all")  # Clear the canvas

        for row in range(16):
            for col in range(16):
                x1 = col * self.pixel_size
                y1 = row * self.pixel_size
                x2 = x1 + self.pixel_size
                y2 = y1 + self.pixel_size
                pixel_color = "white" if self.grid[row][col] else "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=pixel_color, outline="")

        self.window.after(100, self.update_display)

    # Function to update the grid
    def set_grid(self, grid):
        self.grid = grid
        self.update_display()

# Create a 16x16 array representing the initial grid
initial_grid = [[0 for _ in range(16)] for _ in range(16)]

# Set a few pixels to ON (white)
initial_grid[3][7] = 1
initial_grid[8][4] = 1
initial_grid[10][12] = 1

# Create an instance of the UnicornHDSimulator class
simulator = UnicornHDSimulator(initial_grid)

# Update the grid by setting a new array
new_grid = [[1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]]

simulator.set_grid(new_grid)