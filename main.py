import tkinter as tk
from tkinter import messagebox

class PixelDrawer:
    def __init__(self, master, rows=30, cols=30, cell_size=20):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size

        # Create a canvas with a grid of rectangles.
        self.canvas = tk.Canvas(master, width=cols * cell_size, height=rows * cell_size, borderwidth=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=2)

        # Initialize a 2D pixel map (0 = white, 1 = black)
        self.pixel_map = [[0 for _ in range(cols)] for _ in range(rows)]
        # Store rectangle ids for each grid cell
        self.rectangles = {}

        # Draw the grid on the canvas
        for i in range(rows):
            for j in range(cols):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")
                self.rectangles[(i, j)] = rect

        # Bind mouse events to the canvas
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)

        # Add Save and Clear buttons
        self.save_button = tk.Button(master, text="Save", command=self.save_pixel_map)
        self.save_button.grid(row=1, column=0, sticky="ew")
        self.clear_button = tk.Button(master, text="Clear", command=self.clear_pixel_map)
        self.clear_button.grid(row=1, column=1, sticky="ew")

    def on_mouse_down(self, event):
        self.toggle_pixel(event)

    def on_mouse_drag(self, event):
        self.toggle_pixel(event)

    def toggle_pixel(self, event):
        # Calculate grid coordinates from mouse position
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            # Set pixel state to 1 (black)
            self.pixel_map[row][col] = 1
            color = "black"
            rect_id = self.rectangles[(row, col)]
            self.canvas.itemconfig(rect_id, fill=color)

    def clear_pixel_map(self):
        # Reset the pixel map and update the grid to all white
        for i in range(self.rows):
            for j in range(self.cols):
                self.pixel_map[i][j] = 0
                rect_id = self.rectangles[(i, j)]
                self.canvas.itemconfig(rect_id, fill="white")

    def save_pixel_map(self):
        # Save the grid state to a text file, one row per line
        filename = "pixel_map.txt"
        try:
            with open(filename, "w") as f:
                for row in self.pixel_map:
                    line = " ".join(str(val) for val in row)
                    f.write(line + "\n")
            messagebox.showinfo("Save", f"Pixel map saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving pixel map: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("30x30 Pixel Map Drawer")
    app = PixelDrawer(root)
    root.mainloop()
