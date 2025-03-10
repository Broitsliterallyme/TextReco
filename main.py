import tkinter as tk
import math
import numpy as np

class BrushEffectApp:
    def __init__(self, master, rows=30, cols=30, cell_size=20, brush_radius=3.5):
        """
        brush_radius is in cell units.
        For example, brush_radius=1.5 covers roughly 1.5 cells in every direction.
        """
        self.master = master
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.brush_radius = brush_radius

        self.canvas = tk.Canvas(master, width=cols * cell_size, height=rows * cell_size)
        self.canvas.pack()

        # Initialize pixel_map as a list of lists (float intensities: 0.0=white, 1.0=black)
        self.pixel_map = [[0.0 for _ in range(cols)] for _ in range(rows)]
        # Also maintain a continuously updated NumPy array version
        self.numpy_map = np.array(self.pixel_map)

        self.rectangles = {}
        # Create grid of rectangles
        for i in range(rows):
            for j in range(cols):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")
                self.rectangles[(i, j)] = rect

        # Bind mouse events for drawing with the brush
        self.canvas.bind("<Button-1>", self.on_mouse_drag)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)

        # Add a Clear button to reset the canvas
        self.clear_button = tk.Button(master, text="Clear", command=self.clear_pixel_map)
        self.clear_button.pack(pady=5)

    def on_mouse_drag(self, event):
        self.apply_brush(event.x, event.y)
        # Continuously update the numpy_map after each drawing event
        self.numpy_map = np.array(self.pixel_map)

    def apply_brush(self, x, y):
        """
        For each cell within the brush area, compute the distance from the mouse pointer.
        Closer cells get a higher target intensity (up to 1), but a cell is only updated if the new intensity is higher.
        """
        # Brush radius in pixels
        brush_radius_pixels = self.brush_radius * self.cell_size
        
        # Convert mouse position to floating point cell coordinates
        center_col = x / self.cell_size
        center_row = y / self.cell_size

        # Only iterate over cells in the bounding box around the brush area
        min_row = max(int(center_row - self.brush_radius - 1), 0)
        max_row = min(int(center_row + self.brush_radius + 1), self.rows - 1)
        min_col = max(int(center_col - self.brush_radius - 1), 0)
        max_col = min(int(center_col + self.brush_radius + 1), self.cols - 1)
        
        for i in range(min_row, max_row + 1):
            for j in range(min_col, max_col + 1):
                # Center of the current cell
                cell_center_x = j * self.cell_size + self.cell_size / 2
                cell_center_y = i * self.cell_size + self.cell_size / 2
                distance = math.sqrt((cell_center_x - x) ** 2 + (cell_center_y - y) ** 2)
                if distance <= brush_radius_pixels:
                    # New intensity: closer cells are darker
                    new_intensity = 1 - (distance / brush_radius_pixels)
                    # Only update if the new intensity is higher than the current one
                    if new_intensity > self.pixel_map[i][j]:
                        self.pixel_map[i][j] = new_intensity
                        # Convert intensity to grayscale: 0 -> white, 1 -> black
                        grey_value = int((1 - self.pixel_map[i][j]) * 255)
                        color = f"#{grey_value:02x}{grey_value:02x}{grey_value:02x}"
                        rect_id = self.rectangles[(i, j)]
                        self.canvas.itemconfig(rect_id, fill=color)

    def clear_pixel_map(self):
        """Reset the pixel map and update the canvas and numpy_map accordingly."""
        for i in range(self.rows):
            for j in range(self.cols):
                self.pixel_map[i][j] = 0.0
                rect_id = self.rectangles[(i, j)]
                self.canvas.itemconfig(rect_id, fill="white")
        self.numpy_map = np.array(self.pixel_map)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Continuous Brush Drawing with Clear")
    app = BrushEffectApp(root)
    root.mainloop()
