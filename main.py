import tkinter as tk
import math
import numpy as np

class BrushEffectApp:
    def __init__(self, master, rows=30, cols=30, cell_size=15, brush_radius=1.5):
        """
        brush_radius is in cell units. For example, a brush_radius of 3 means the brush covers roughly
        3 cells in every direction from the mouse pointer.
        """
        self.master = master
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.brush_radius = brush_radius

        self.canvas = tk.Canvas(master, width=cols * cell_size, height=rows * cell_size)
        self.canvas.pack()

        # Initialize pixel_map to store intensity values (0.0 = white, 1.0 = black)
        self.pixel_map = [[0.0 for _ in range(cols)] for _ in range(rows)]
        # Maintain a continuously updated NumPy array version of the pixel map
        self.pixel_map_np = np.array(self.pixel_map)
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

        # Bind mouse events for clicking and dragging
        self.canvas.bind("<Button-1>", self.on_mouse_drag)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)

        # Provide a Clear button to reset the canvas
        self.clear_button = tk.Button(master, text="Clear", command=self.clear_pixel_map)
        self.clear_button.pack(pady=5)

    def on_mouse_drag(self, event):
        self.apply_brush(event.x, event.y)
        # Update the NumPy array after each brush stroke
        self.pixel_map_np = np.array(self.pixel_map)

    def apply_brush(self, x, y):
        """
        Applies the brush effect with a strong dark center and a small outer gradient.
        Pixels within the inner region (brush_radius_pixels - cell_size) become full dark (intensity 1).
        Only the narrow ring (last cell width) shows a gradual falloff.
        """
        brush_radius_pixels = self.brush_radius * self.cell_size
        inner_radius = max(brush_radius_pixels - self.cell_size, 0)  # inner region threshold

        center_col = x / self.cell_size
        center_row = y / self.cell_size

        # Iterate over cells in the bounding box of the brush area
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
                    # Determine intensity:
                    if distance <= inner_radius:
                        new_intensity = 1.0
                    else:
                        # Only a small gradient in the outer ring (width=cell_size)
                        new_intensity = 1 - ((distance - inner_radius) / (brush_radius_pixels - inner_radius))
                    # Update only if the new intensity is higher than current intensity
                    if new_intensity > self.pixel_map[i][j]:
                        self.pixel_map[i][j] = new_intensity
                        # Convert intensity to a grayscale color (0: white, 1: black)
                        grey_value = int((1 - self.pixel_map[i][j]) * 255)
                        color = f"#{grey_value:02x}{grey_value:02x}{grey_value:02x}"
                        rect_id = self.rectangles[(i, j)]
                        self.canvas.itemconfig(rect_id, fill=color)

    def clear_pixel_map(self):
        # Reset the pixel_map and update the canvas to all white
        for i in range(self.rows):
            for j in range(self.cols):
                self.pixel_map[i][j] = 0.0
                rect_id = self.rectangles[(i, j)]
                self.canvas.itemconfig(rect_id, fill="white")
        # Update the NumPy array after clearing
        self.pixel_map_np = np.array(self.pixel_map)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Brush Effect Drawing")
    app = BrushEffectApp(root)
    root.mainloop()
