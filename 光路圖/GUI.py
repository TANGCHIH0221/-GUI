# gui.py
import tkinter as tk
from optical_elements import LightSource, ConvexLens, ConcaveLens, PlaneMirror, ConcaveMirror, ConvexMirror, PBS, BS, Prism, Line
from matrix_simulation import MatrixSimulation

class OpticalDesignApp:
    def __init__(self, root):
        self.root = root
        self.root.title("光路圖設計工具 ")
        self.root.geometry("1000x600")

        # 固定尺寸參數
        self.canvas_width = 750
        self.canvas_height = 600
        self.toolbar_width = 150
        self.grid_size = 50

        # 工具列框架
        self.toolbar = tk.Frame(self.root, width=self.toolbar_width, height=self.canvas_height, bg="lightgray")
        self.toolbar.pack(side=tk.LEFT, fill=tk.Y)
        self.toolbar.pack_propagate(False)

        # 畫布
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=None, expand=False)

        # 結果顯示框
        self.result_frame = tk.Frame(self.root, bg="lightyellow")
        self.result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.result_label = tk.Label(self.result_frame, text="矩陣運算結果", bg="lightyellow")
        self.result_label.pack(pady=10)
        self.result_text = tk.Text(self.result_frame, width=20, height=30)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # 畫格子
        self.draw_grid()

        # 元件按鈕
        self.add_button("光源", self.add_light_source)
        self.add_button("凸透鏡", self.add_convex_lens)
        self.add_button("凹透鏡", self.add_concave_lens)
        self.add_button("平面鏡", self.add_plane_mirror)
        self.add_button("凹面鏡", self.add_concave_mirror)
        self.add_button("凸面鏡", self.add_convex_mirror)
        self.add_button("分光鏡 (PBS)", self.add_pbs)
        self.add_button("分束器 (BS)", self.add_bs)
        self.add_button("稜鏡", self.add_prism)
        self.add_button("On", self.simulate_light)

        # 儲存元件的列表
        self.elements = []
        self.selected = None
        self.draw_mode = False
        self.start_point = None

        # 初始化矩陣模擬
        self.matrix_sim = MatrixSimulation(self.canvas, self.result_text, self.canvas_width)

        # 綁定滑鼠事件
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-3>", self.on_right_click)

    def draw_grid(self):
        for x in range(0, self.canvas_width, self.grid_size):
            self.canvas.create_line(x, 0, x, self.canvas_height, fill="gray", dash=(2, 2), tags="grid")
        for y in range(0, self.canvas_height, self.grid_size):
            self.canvas.create_line(0, y, self.canvas_width, y, fill="gray", dash=(2, 2), tags="grid")

    def snap_to_grid(self, x, y):
        snapped_x = round(x / self.grid_size) * self.grid_size
        snapped_y = round(y / self.grid_size) * self.grid_size
        return snapped_x, snapped_y

    def add_button(self, text, command):
        btn = tk.Button(self.toolbar, text=text, command=command)
        btn.pack(fill=tk.X, pady=5)

    def add_light_source(self):
        x, y = self.snap_to_grid(100, 300)
        element = LightSource(self.canvas, x, y)
        self.elements.append(element.draw())

    def add_convex_lens(self):
        x, y = self.snap_to_grid(300, 300)
        element = ConvexLens(self.canvas, x, y)
        self.elements.append(element.draw())

    def add_concave_lens(self):
        x, y = self.snap_to_grid(300, 300)
        element = ConcaveLens(self.canvas, x, y)
        self.elements.append(element.draw())

    def add_plane_mirror(self):
        x, y = self.snap_to_grid(500, 300)
        element = PlaneMirror(self.canvas, x, y)
        self.elements.append(element.draw())

    def add_concave_mirror(self):
        x, y = self.snap_to_grid(500, 300)
        element = ConcaveMirror(self.canvas, x, y)
        self.elements.append(element.draw())

    def add_convex_mirror(self):
        x, y = self.snap_to_grid(500, 300)
        element = ConvexMirror(self.canvas, x, y)
        self.elements.append(element.draw())

    def add_pbs(self):
        x, y = self.snap_to_grid(400, 300)
        element = PBS(self.canvas, x, y)
        self.elements.append(element.draw())

    def add_bs(self):
        x, y = self.snap_to_grid(400, 300)
        element = BS(self.canvas, x, y)
        self.elements.append(element.draw())

    def add_prism(self):
        x, y = self.snap_to_grid(400, 300)
        element = Prism(self.canvas, x, y)
        self.elements.append(element.draw())

    def start_draw_line(self):
        self.draw_mode = True
        self.start_point = None

    def on_click(self, event):
        if self.draw_mode:
            if self.start_point is None:
                self.start_point = self.snap_to_grid(event.x, event.y)
            else:
                end_point = self.snap_to_grid(event.x, event.y)
                element = Line(self.canvas, self.start_point[0], self.start_point[1])
                self.elements.append(element.draw(end_point[0], end_point[1]))
                self.draw_mode = False
                self.start_point = None
        else:
            self.selected = None
            for element in self.elements:
                coords = self.canvas.coords(element["id"])
                if min(coords[0::2]) <= event.x <= max(coords[0::2]) and min(coords[1::2]) <= event.y <= max(coords[1::2]):
                    self.selected = element
                    break

    def on_drag(self, event):
        if self.selected and not self.draw_mode:
            new_x, new_y = self.snap_to_grid(event.x, event.y)
            dx = new_x - self.selected["x"]
            dy = new_y - self.selected["y"]
            self.canvas.move(self.selected["id"], dx, dy)
            self.selected["x"] = new_x
            self.selected["y"] = new_y

    def on_release(self, event):
        if not self.draw_mode:
            self.selected = None

    def on_right_click(self, event):
        for element in self.elements[:]:
            coords = self.canvas.coords(element["id"])
            if min(coords[0::2]) <= event.x <= max(coords[0::2]) and min(coords[1::2]) <= event.y <= max(coords[1::2]):
                self.canvas.delete(element["id"])
                self.elements.remove(element)
                break

    def simulate_light(self):
        self.matrix_sim.simulate_light(self.elements)

if __name__ == "__main__":
    root = tk.Tk()
    app = OpticalDesignApp(root)
    root.mainloop()