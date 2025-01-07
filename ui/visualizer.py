import tkinter as tk

def plot_progress(canvas, best_route):
    canvas.delete("all")
    scale = 0.4
    for i in range(len(best_route.cities)):
        city_a = best_route.cities[i]
        city_b = best_route.cities[(i + 1) % len(best_route.cities)]
        x1, y1 = city_a.x * scale, city_a.y * scale
        x2, y2 = city_b.x * scale, city_b.y * scale
        canvas.create_line(x1, y1, x2, y2, fill="blue", arrow=tk.LAST)
        canvas.create_text(x1 + 10, y1 + 6, text=str(city_a.ID), fill="black")

    canvas.update()
