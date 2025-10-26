#!/usr/bin/env python3
"""
MRT Dijkstra GUI (Singapore) - demo script
- Implements Dijkstra's algorithm on a small sample Singapore MRT subgraph.
- GUI (Tkinter) allows selecting start/end stations and choosing optimization:
    * Time
    * Price
    * Combined (weighted sum of normalized time and price)
- You can also load a CSV of edges with columns: station1,station2,time_minutes,price_sgd
- Save this file and run: python mrt_dijkstra_gui.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import math

# ---------- Sample graph data (small demo subset) ----------
# Edges defined as (u, v, time_minutes, price_sgd)
SAMPLE_EDGES = [
    ("Jurong East", "Boon Lay", 8, 1.20),
    ("Jurong East", "Yishun", 25, 2.50),  # unrealistic but for demo
    ("Jurong East", "Bukit Batok", 4, 0.90),
    ("Bukit Batok", "Bukit Gombak", 3, 0.70),
    ("Bukit Gombak", "Choa Chu Kang", 4, 0.80),
    ("Choa Chu Kang", "Yew Tee", 5, 0.85),
    ("Raffles Place", "City Hall", 2, 0.60),
    ("City Hall", "Bugis", 3, 0.70),
    ("Bugis", "Dhoby Ghaut", 2, 0.60),
    ("Dhoby Ghaut", "Orchard", 5, 1.00),
    ("Orchard", "Newton", 3, 0.70),
    ("Newton", "Novena", 3, 0.70),
    ("Novena", "Bishan", 4, 0.90),
    ("Bishan", "Ang Mo Kio", 3, 0.80),
    ("Ang Mo Kio", "Yishun", 10, 1.50),
    ("City Hall", "Bras Basah", 1, 0.50),
    ("Bras Basah", "Bencoolen", 2, 0.60),
]

# ---------- Graph utilities ----------

def build_graph(edges):
    graph = {}
    for u, v, t, p in edges:
        graph.setdefault(u, []).append((v, float(t), float(p)))
        graph.setdefault(v, []).append((u, float(t), float(p)))
    return graph

def dijkstra(graph, start, end, mode="time", weight_time=0.5):
    # We will compute distance based on chosen mode:
    # - "time": use time as weight
    # - "price": use price as weight
    # - "combined": normalize time and price across graph and use weighted sum
    nodes = list(graph.keys())
    if start not in graph or end not in graph:
        return None, None, "Start or end station not in graph."

    # For combined mode, precompute normalization factors (min-max scaling)
    times = []
    prices = []
    for u in graph:
        for v, t, p in graph[u]:
            times.append(t)
            prices.append(p)
    # avoid zero-range
    t_min, t_max = (min(times), max(times)) if times else (0,1)
    p_min, p_max = (min(prices), max(prices)) if prices else (0,1)

    def edge_weight(t, p):
        if mode == "time":
            return t
        elif mode == "price":
            return p
        else:
            # normalized (0..1)
            tn = (t - t_min) / (t_max - t_min) if t_max > t_min else 0.0
            pn = (p - p_min) / (p_max - p_min) if p_max > p_min else 0.0
            return weight_time * tn + (1 - weight_time) * pn

    # Classic Dijkstra
    unvisited = set(nodes)
    dist = {n: math.inf for n in nodes}
    prev = {n: None for n in nodes}
    dist[start] = 0.0

    while unvisited:
        # pick node with smallest dist
        current = min((n for n in unvisited), key=lambda x: dist[x], default=None)
        if current is None or dist[current] == math.inf:
            break
        if current == end:
            break
        unvisited.remove(current)
        for neighbor, t, p in graph.get(current, []):
            if neighbor not in unvisited:
                # skip already-finalized neighbor
                continue
            w = edge_weight(t, p)
            alt = dist[current] + w
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = (current, t, p)
    # reconstruct path
    if dist[end] == math.inf:
        return None, None, "No path found."
    path = []
    total_time = 0.0
    total_price = 0.0
    cur = end
    while cur != start:
        pr = prev[cur]
        if pr is None:
            break
        prev_node, t, p = pr
        path.append((prev_node, cur, t, p))
        total_time += t
        total_price += p
        cur = prev_node
    path.reverse()
    return path, {"time": total_time, "price": total_price}, None

# ---------- GUI ----------
class MRTApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Singapore MRT - Dijkstra Path Finder (Demo)")
        self.geometry("820x520")
        self.resizable(False, False)

        self.edges = SAMPLE_EDGES.copy()
        self.graph = build_graph(self.edges)
        self.stations = sorted(self.graph.keys())

        self.create_widgets()

    def create_widgets(self):
        frm_left = ttk.Frame(self, padding=12)
        frm_left.place(x=10, y=10, width=380, height=500)

        ttk.Label(frm_left, text="Start Station:").pack(anchor="w")
        self.start_var = tk.StringVar(value=self.stations[0] if self.stations else "")
        self.start_combo = ttk.Combobox(frm_left, values=self.stations, textvariable=self.start_var, width=40)
        self.start_combo.pack(fill="x", pady=4)

        ttk.Label(frm_left, text="End Station:").pack(anchor="w", pady=(8,0))
        self.end_var = tk.StringVar(value=self.stations[-1] if self.stations else "")
        self.end_combo = ttk.Combobox(frm_left, values=self.stations, textvariable=self.end_var, width=40)
        self.end_combo.pack(fill="x", pady=4)

        ttk.Label(frm_left, text="Optimize by:").pack(anchor="w", pady=(8,0))
        self.mode_var = tk.StringVar(value="time")
        modes = [("Time", "time"), ("Price", "price"), ("Combined (time vs price)", "combined")]
        for text, val in modes:
            ttk.Radiobutton(frm_left, text=text, variable=self.mode_var, value=val, command=self.on_mode_change).pack(anchor="w")

        self.weight_frame = ttk.Frame(frm_left)
        self.weight_label = ttk.Label(self.weight_frame, text="Weight for Time (0 = price-only, 1 = time-only):")
        self.weight_label.pack(anchor="w")
        self.weight_var = tk.DoubleVar(value=0.6)
        self.weight_scale = ttk.Scale(self.weight_frame, from_=0.0, to=1.0, variable=self.weight_var, orient="horizontal")
        self.weight_scale.pack(fill="x", pady=6)
        self.weight_frame.pack(fill="x", pady=8)

        ttk.Button(frm_left, text="Find Path", command=self.find_path).pack(fill="x", pady=(10,4))
        ttk.Button(frm_left, text="Load edges from CSV", command=self.load_csv).pack(fill="x", pady=4)
        ttk.Button(frm_left, text="Reset to demo graph", command=self.reset_graph).pack(fill="x", pady=4)

        # Right panel: results and edges table
        frm_right = ttk.Frame(self, padding=12)
        frm_right.place(x=400, y=10, width=410, height=500)

        ttk.Label(frm_right, text="Result:").pack(anchor="w")
        self.result_txt = tk.Text(frm_right, height=12, width=48, state="disabled", wrap="word")
        self.result_txt.pack(pady=4)

        ttk.Label(frm_right, text="Current edges (u - v : time min, price SGD):").pack(anchor="w", pady=(8,0))
        self.edges_list = tk.Text(frm_right, height=14, width=48, state="disabled", wrap="none")
        self.edges_list.pack(pady=4)
        self.refresh_edges_display()

        ttk.Label(frm_right, text="Notes:").pack(anchor="w", pady=(8,0))
        notes = ("This is a demo with a small sample subgraph. For production use,\n"
                 "replace edges with real MRT network data (CSV or API), where each\n"
                 "edge has travel time and fare. Use the 'Combined' mode to mix\n"
                 "time vs price with the slider. Results show the sequence of hops\n"
                 "plus totals.")
        ttk.Label(frm_right, text=notes, wraplength=380, justify="left").pack(anchor="w", pady=4)

    def on_mode_change(self):
        if self.mode_var.get() == "combined":
            self.weight_frame.pack(fill="x", pady=8)
        else:
            self.weight_frame.forget()

    def refresh_edges_display(self):
        self.edges_list.config(state="normal")
        self.edges_list.delete("1.0", tk.END)
        for u, v, t, p in self.edges:
            self.edges_list.insert(tk.END, f"{u} - {v} : {t} min, ${p:.2f}\n")
        self.edges_list.config(state="disabled")

        # update stations list in combos
        self.graph = build_graph(self.edges)
        self.stations = sorted(self.graph.keys())
        self.start_combo.config(values=self.stations)
        self.end_combo.config(values=self.stations)

    def find_path(self):
        start = self.start_var.get().strip()
        end = self.end_var.get().strip()
        mode = self.mode_var.get()
        w = float(self.weight_var.get()) if mode == "combined" else 0.5
        path, totals, err = dijkstra(self.graph, start, end, mode=("combined" if mode=="combined" else mode), weight_time=w)
        self.result_txt.config(state="normal")
        self.result_txt.delete("1.0", tk.END)
        if err:
            self.result_txt.insert(tk.END, f"Error: {err}\n")
        else:
            self.result_txt.insert(tk.END, f"Path from {start} to {end} optimizing by {mode} (weight_time={w:.2f})\n\n")
            for u, v, t, p in path:
                self.result_txt.insert(tk.END, f"{u} -> {v} : {t} min, ${p:.2f}\n")
            self.result_txt.insert(tk.END, "\nTotals:\n")
            self.result_txt.insert(tk.END, f"Total travel time: {totals['time']:.1f} minutes\n")
            self.result_txt.insert(tk.END, f"Total fare (sum of edges): ${totals['price']:.2f}\n\n")
            self.result_txt.insert(tk.END, "Note: fares are edge-summed for demo purposes; real fare calculation may be different (distance-based or zonal).\n")
        self.result_txt.config(state="disabled")

    def load_csv(self):
        path = filedialog.askopenfilename(title="Open CSV", filetypes=[("CSV files","*.csv"),("All files","*.*")])
        if not path:
            return
        try:
            new_edges = []
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row or row[0].strip().startswith("#"):
                        continue
                    if len(row) < 4:
                        continue
                    u = row[0].strip()
                    v = row[1].strip()
                    t = float(row[2])
                    p = float(row[3])
                    new_edges.append((u, v, t, p))
            if not new_edges:
                messagebox.showwarning("No edges", "The CSV did not contain valid edges (expected station1,station2,time,price).")
                return
            self.edges = new_edges
            self.refresh_edges_display()
            messagebox.showinfo("Loaded", f"Loaded {len(new_edges)} edges from CSV.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV: {e}")

    def reset_graph(self):
        self.edges = SAMPLE_EDGES.copy()
        self.refresh_edges_display()
        messagebox.showinfo("Reset", "Graph reset to demo dataset.")

if __name__ == "__main__":
    app = MRTApp()
    app.mainloop()
