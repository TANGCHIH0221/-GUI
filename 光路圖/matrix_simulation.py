# matrix_simulation.py
import numpy as np

class MatrixSimulation:
    def __init__(self, canvas, result_text, canvas_width):
        self.canvas = canvas
        self.result_text = result_text
        self.canvas_width = canvas_width

    def simulate_light(self, elements):
        self.canvas.delete("light_path")
        self.result_text.delete(1.0, "end")
        for light in [e for e in elements if e["type"] == "light"]:
            self.draw_light_path(light, elements)

    def draw_light_path(self, light, elements):
        x, y = light["x"], light["y"]
        current_x, current_y = x, y
        direction = "right"
        jones_vector = np.array(light["jones"])
        path_count = 0

        elements_sorted = sorted([e for e in elements if e["type"] != "light" and e["type"] != "line" and e["x"] > x], key=lambda e: e["x"])

        for element in elements_sorted:
            next_x = element["x"]
            next_y = element["y"]

            if direction == "right":
                self.canvas.create_line(current_x, current_y, next_x, current_y, fill="red", tags="light_path")
            elif direction == "up":
                self.canvas.create_line(current_x, current_y, next_x, current_y - 100, fill="red", tags="light_path")
            elif direction == "down":
                self.canvas.create_line(current_x, current_y, next_x, current_y + 100, fill="red", tags="light_path")

            current_x = next_x
            current_y = next_y

            if element["type"] in ["plane_mirror", "concave_mirror"]:
                direction = "up" if direction == "right" else "right"
                jones_matrix = np.array([[1, 0], [0, 1]])
                jones_vector = np.dot(jones_matrix, jones_vector)
            elif element["type"] == "convex_mirror":
                direction = "down" if direction == "right" else "right"
                jones_matrix = np.array([[1, 0], [0, 1]])
                jones_vector = np.dot(jones_matrix, jones_vector)
            elif element["type"] == "pbs":
                pbs_trans = np.array([[1, 0], [0, 0]])
                pbs_refl = np.array([[0, 0], [0, 1]])
                trans_vector = np.dot(pbs_trans, jones_vector)
                refl_vector = np.dot(pbs_refl, jones_vector)
                self.canvas.create_line(next_x, next_y, next_x + 100, next_y, fill="red", tags="light_path")
                self.canvas.create_line(next_x, next_y, next_x, next_y + 100, fill="blue", tags="light_path")
                path_count += 1
                self.result_text.insert("end", f"光路 {path_count} (透射): {trans_vector}\n")
                path_count += 1
                self.result_text.insert("end", f"光路 {path_count} (反射): {refl_vector}\n")
                jones_vector = trans_vector
                direction = "right"
            elif element["type"] == "bs":
                bs_matrix = np.array([[0.5, 0], [0, 0.5]])
                trans_vector = np.dot(bs_matrix, jones_vector)
                refl_vector = np.dot(bs_matrix, jones_vector)
                self.canvas.create_line(next_x, next_y, next_x + 100, next_y, fill="red", tags="light_path", dash=(4, 4))
                self.canvas.create_line(next_x, next_y, next_x, next_y + 100, fill="red", tags="light_path", dash=(4, 4))
                path_count += 1
                self.result_text.insert("end", f"光路 {path_count} (透射): {trans_vector}\n")
                path_count += 1
                self.result_text.insert("end", f"光路 {path_count} (反射): {refl_vector}\n")
                jones_vector = trans_vector
                direction = "right"
            elif element["type"] == "prism":
                direction = "down"
                jones_matrix = np.array([[1, 0], [0, 1]])
                jones_vector = np.dot(jones_matrix, jones_vector)
            elif element["type"] in ["convex_lens", "concave_lens"]:
                direction = "right"
                jones_matrix = np.array([[1, 0], [0, 1]])
                jones_vector = np.dot(jones_matrix, jones_vector)

        if not elements_sorted and direction == "right":
            self.canvas.create_line(current_x, current_y, self.canvas_width, current_y, fill="red", tags="light_path")
            path_count += 1
            self.result_text.insert("end", f"光路 {path_count} (末端): {jones_vector}\n")