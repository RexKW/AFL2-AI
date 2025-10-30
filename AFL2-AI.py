#!/usr/bin/env python3
"""
Singapore MRT Dijkstra Path Finder
Clean, Modern UI + Distance, Time & Fare
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import math

# ---------- Sample Graph ----------
# Each tuple = (Station A, Station B, Distance km, Time min)
SAMPLE_EDGES = [
    ("Jurong East", "Bukit Batok", 4, 6),
    ("Bukit Batok", "Bukit Gombak", 2, 3),
    ("Bukit Gombak", "Choa Chu Kang", 3, 4),
    ("Choa Chu Kang", "Yew Tee", 2, 3),
    ("Jurong East", "Boon Lay", 10, 14),
    ("Boon Lay", "Choa Chu Kang", 12, 18),
    ("City Hall", "Raffles Place", 2, 3),
    ("City Hall", "Bugis", 3, 4),
    ("Bugis", "Dhoby Ghaut", 2, 3),
    ("Dhoby Ghaut", "Orchard", 4, 6),
    ("Orchard", "Newton", 2, 3),
    ("Newton", "Novena", 2, 3),
    ("Novena", "Bishan", 4, 6),
    ("Bishan", "Ang Mo Kio", 3, 4),
    ("Ang Mo Kio", "Yishun", 10, 13),
    ("Jurong East", "Yishun", 22, 30),
]

# ---------- Fare Calculation ----------
def fare_from_distance(distance_km):
    """Compute fare (SGD) based on MRT distance rules."""
    if distance_km <= 3.2:
        return 0.99
    elif distance_km <= 8.2:
        return 0.99 + (distance_km - 3.2) * (1.47 - 0.99) / (8.2 - 3.2)
    elif distance_km <= 40:
        return 1.47 + (distance_km - 8.2) * (2.24 - 1.47) / (40 - 8.2)
    else:
        return 2.24  # capped

# ---------- Graph Utilities ----------
def build_graph(edges):
    graph = {}
    for u, v, dist, time in edges:
        price = fare_from_distance(dist)
        graph.setdefault(u, []).append((v, dist, time, price))
        graph.setdefault(v, []).append((u, dist, time, price))
    return graph

def dijkstra(graph, start, end):
    nodes = list(graph.keys())
    if start not in graph or end not in graph:
        return None, None, "Start or end station not found."

    unvisited = set(nodes)
    dist = {n: math.inf for n in nodes}
    prev = {n: None for n in nodes}
    dist[start] = 0.0

    while unvisited:
        current = min(unvisited, key=lambda x: dist[x], default=None)
        if current is None or dist[current] == math.inf:
            break
        if current == end:
            break
        unvisited.remove(current)

        for neighbor, d, t, p in graph.get(current, []):
            if neighbor not in unvisited:
                continue
            alt = dist[current] + d
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = (current, d, t, p)

    if dist[end] == math.inf:
        return None, None, "No path found."

    path = []
    total_distance = 0.0
    total_time = 0.0
    total_price = 0.0

    cur = end
    while cur != start:
        pr = prev[cur]
        if pr is None:
            break
        prev_node, d, t, p = pr
        path.append((prev_node, cur, d, t, p))
        total_distance += d
        total_time += t
        total_price += p
        cur = prev_node
    path.reverse()

    return path, {"distance": total_distance, "time": total_time, "price": total_price}, None

# ---------- GUI ----------
class MRTApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🚇 Singapore MRT Route Finder")
        self.geometry("700x420")
        self.configure(bg="#f9fafc")
        self.resizable(False, False)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8, background="#0078D7", foreground="white")
        style.map("TButton", background=[("active", "#005fa3")])
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TCombobox", font=("Segoe UI", 10), padding=5)

        self.edges = SAMPLE_EDGES.copy()
        self.graph = build_graph(self.edges)
        self.stations = sorted(self.graph.keys())

        self.create_widgets()

    def create_widgets(self):
        frm_main = ttk.Frame(self, padding=20)
        frm_main.pack(fill="both", expand=True)

        ttk.Label(frm_main, text="Singapore MRT Path Finder", font=("Segoe UI Semibold", 16)).pack(pady=(0, 15))

        frm_inputs = ttk.Frame(frm_main)
        frm_inputs.pack(pady=5)

        ttk.Label(frm_inputs, text="Start:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.start_var = tk.StringVar(value=self.stations[0])
        ttk.Combobox(frm_inputs, values=self.stations, textvariable=self.start_var, width=25).grid(row=0, column=1, padx=5)

        ttk.Label(frm_inputs, text="Destination:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.end_var = tk.StringVar(value=self.stations[-1])
        ttk.Combobox(frm_inputs, values=self.stations, textvariable=self.end_var, width=25).grid(row=0, column=3, padx=5)

        ttk.Button(frm_main, text="Find Route", command=self.find_path).pack(pady=15)

        self.result_frame = ttk.Frame(frm_main)
        self.result_frame.pack(pady=10, fill="x")

        self.result_label = ttk.Label(self.result_frame, text="", font=("Segoe UI", 11), foreground="#333", wraplength=650, justify="center")
        self.result_label.pack()

        ttk.Separator(frm_main, orient="horizontal").pack(fill="x", pady=15)

        ttk.Button(frm_main, text="Load CSV", command=self.load_csv).pack(side="left", padx=20)
        ttk.Button(frm_main, text="Reset to Default", command=self.reset_graph).pack(side="right", padx=20)

    def find_path(self):
        start = self.start_var.get().strip()
        end = self.end_var.get().strip()
        path, totals, err = dijkstra(self.graph, start, end)

        if err:
            messagebox.showerror("Error", err)
            return

        route = " → ".join([u for u, _, _, _, _ in path] + [end])
        result_text = (
            f"{route}\n"
            f"⏱️  Time: {totals['time']:.0f} min "
            f"📏  Distance: {totals['distance']:.1f} km "
            f"💵  Fare: ${totals['price']:.2f}"
        )

        self.result_label.config(text=result_text)

    def load_csv(self):
        path = filedialog.askopenfilename(title="Open CSV", filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        try:
            new_edges = []
            with open(path, newline="", encoding="utf-8") as f:
                for row in csv.reader(f):
                    if not row or row[0].startswith("#"):
                        continue
                    u, v, d, t = row[:4]
                    new_edges.append((u.strip(), v.strip(), float(d), float(t)))
            self.edges = new_edges
            self.graph = build_graph(self.edges)
            self.stations = sorted(self.graph.keys())
            messagebox.showinfo("Loaded", f"Loaded {len(new_edges)} edges from CSV.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reset_graph(self):
        self.edges = SAMPLE_EDGES.copy()
        self.graph = build_graph(self.edges)
        self.stations = sorted(self.graph.keys())
        messagebox.showinfo("Reset", "Graph reset to demo dataset.")
        self.result_label.config(text="")

if __name__ == "__main__":
    app = MRTApp()
    app.mainloop()
