# optical_elements.py
class OpticalElement:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.id = None

    def snap_to_grid(self, x, y, grid_size=50):
        snapped_x = round(x / grid_size) * grid_size
        snapped_y = round(y / grid_size) * grid_size
        return snapped_x, snapped_y

class LightSource(OpticalElement):
    def draw(self):
        self.id = self.canvas.create_oval(self.x-10, self.y-10, self.x+10, self.y+10, fill="yellow", tags="element")
        return {"type": "light", "id": self.id, "x": self.x, "y": self.y, "jones": [1, 0]}  # H偏振

class ConvexLens(OpticalElement):
    def draw(self):
        self.id = self.canvas.create_polygon(self.x-10, self.y-30, self.x+10, self.y-30, self.x+15, self.y, 
                                             self.x+10, self.y+30, self.x-10, self.y+30, self.x-15, self.y, 
                                             fill="lightblue", tags="element")
        return {"type": "convex_lens", "id": self.id, "x": self.x, "y": self.y}

class ConcaveLens(OpticalElement):
    def draw(self):
        self.id = self.canvas.create_polygon(self.x-15, self.y-30, self.x+15, self.y-30, self.x+10, self.y, 
                                             self.x+15, self.y+30, self.x-15, self.y+30, self.x-10, self.y, 
                                             fill="lightblue", tags="element")
        return {"type": "concave_lens", "id": self.id, "x": self.x, "y": self.y}

class PlaneMirror(OpticalElement):
    def draw(self):
        self.id = self.canvas.create_rectangle(self.x-5, self.y-40, self.x+5, self.y+40, fill="silver", tags="element")
        return {"type": "plane_mirror", "id": self.id, "x": self.x, "y": self.y}

class ConcaveMirror(OpticalElement):
    def draw(self):
        self.id = self.canvas.create_arc(self.x-40, self.y-40, self.x+40, self.y+40, start=90, extent=180, fill="silver", tags="element")
        return {"type": "concave_mirror", "id": self.id, "x": self.x, "y": self.y}

class ConvexMirror(OpticalElement):
    def draw(self):
        self.id = self.canvas.create_arc(self.x-40, self.y-40, self.x+40, self.y+40, start=270, extent=180, fill="silver", tags="element")
        return {"type": "convex_mirror", "id": self.id, "x": self.x, "y": self.y}

class PBS(OpticalElement):
    def draw(self):
        self.id = self.canvas.create_rectangle(self.x-20, self.y-20, self.x+20, self.y+20, fill="gray", tags="element", stipple="gray50")
        return {"type": "pbs", "id": self.id, "x": self.x, "y": self.y}

class BS(OpticalElement):
    def draw(self):
        self.id = self.canvas.create_rectangle(self.x-20, self.y-20, self.x+20, self.y+20, fill="lightgray", tags="element")
        return {"type": "bs", "id": self.id, "x": self.x, "y": self.y}

class Prism(OpticalElement):
    def draw(self):
        self.id = self.canvas.create_polygon(self.x-20, self.y-20, self.x+20, self.y-20, self.x, self.y+20, fill="lightgreen", tags="element")
        return {"type": "prism", "id": self.id, "x": self.x, "y": self.y}

class Line(OpticalElement):
    def draw(self, end_x, end_y):
        self.id = self.canvas.create_line(self.x, self.y, end_x, end_y, fill="red", tags="element")
        return {"type": "line", "id": self.id, "x": self.x, "y": self.y}