
"""
Singapore MRT Dijkstra Path Finder
Clean, Modern UI + Distance, Time & Fare
Now supports route type: Shortest Distance, Shortest Time, or Balanced
"""

from collections import deque
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import csv
import math

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- Sample Graph ----------
# Each tuple = (Station A, Station B, Distance km, Time min)
SAMPLE_EDGES = [
    ("Jurong East", "Bukit Batok", 2.1, 7),
    ("Bukit Batok", "Bukit Gombak", 1.2, 5),
    ("Bukit Gombak", "Choa Chu Kang", 3.3, 7),
    ("Choa Chu Kang", "Yew Tee", 1.4, 6),
    ("Yew Tee", "Kranji", 4.1, 11),
    ("Kranji", "Marsiling", 1.7, 6),
    ("Marsiling", "Woodlands", 1.5, 6),
    ("Woodlands", "Admiralty", 1.7, 6),
    ("Admiralty", "Sembawang", 2.4, 6),
    ("Sembawang", "Yishun", 3.2, 7),
    ("Yishun", "Khatib", 1.4, 5),
    ("Khatib", "Yio Chu Kang", 4.9, 8),
    ("Yio Chu Kang", "Ang Mo Kio", 1.5, 6),
    ("Ang Mo Kio", "Bishan", 2.4, 6),
    ("Bishan", "Braddell", 1.2, 5),
    ("Braddell", "Toa Payoh", 0.9, 5),
    ("Toa Payoh", "Novena", 1.5, 5),
    ("Novena", "Newton", 1.2, 5),
    ("Newton", "Orchard", 1.2, 5),
    ("Orchard", "Somerset", 1.0, 5),
    ("Somerset", "Dhoby Ghaut", 0.8, 5),
    ("Dhoby Ghaut", "City Hall", 1.0, 5),
    ("City Hall", "Raffles Place", 1.0, 5),
    ("Raffles Place", "Marina Bay", 1.0, 5),
    ("Marina Bay", "Marina South Pier", 1.4, 6),
    ("Tuas Link", "Tuas West Road", 1.3, 5),
    ("Tuas West Road", "Tuas Crescent", 1.4, 5),
    ("Tuas Crescent", "Gul Circle", 1.7, 6),
    ("Gul Circle", "Joo Koon", 2.3, 6),
    ("Joo Koon", "Pioneer", 2.6, 6),
    ("Pioneer", "Boon Lay", 0.9, 5),
    ("Boon Lay", "Lakeside", 1.8, 7),
    ("Lakeside", "Chinese Garden", 1.4, 6),
    ("Chinese Garden", "Jurong East", 1.5, 6),
    ("Jurong East", "Clementi", 3.5, 7),
    ("Clementi", "Dover", 1.7, 6),
    ("Dover", "Buona Vista", 1.4, 6),
    ("Buona Vista", "Commonwealth", 1.1, 5),
    ("Commonwealth", "Queenstown", 1.2, 5),
    ("Queenstown", "Redhill", 1.4, 6),
    ("Redhill", "Tiong Bahru", 1.2, 5),
    ("Tiong Bahru", "Outram Park", 1.5, 6),
    ("Outram Park", "Tanjong Pagar", 1.0, 5),
    ("Tanjong Pagar", "Raffles Place", 1.2, 5),
    ("Raffles Place", "City Hall", 1.0, 5),
    ("City Hall", "Bugis", 1.0, 6),
    ("Bugis", "Lavender", 1.1, 5),
    ("Lavender", "Kallang", 1.1, 5),
    ("Kallang", "Aljunied", 1.4, 6),
    ("Aljunied", "Paya Lebar", 1.2, 5),
    ("Paya Lebar", "Eunos", 1.1, 5),
    ("Eunos", "Kembangan", 1.1, 5),
    ("Kembangan", "Bedok", 2.0, 6),
    ("Bedok", "Tanah Merah", 1.9, 6),
    ("Tanah Merah", "Simei", 2.5, 8),
    ("Simei", "Tampines", 1.4, 6),
    ("Tampines", "Pasir Ris", 2.4, 6),
    ("Tanah Merah", "Expo", 1.9, 13),
    ("Expo", "Changi Airport", 4.5, 14),
    ("HarbourFront", "Outram Park", 2.6, 7),
    ("Outram Park", "Chinatown", 0.7, 5),
    ("Chinatown", "Clarke Quay", 0.6, 5),
    ("Clarke Quay", "Dhoby Ghaut", 1.4, 6),
    ("Dhoby Ghaut", "Little India", 1.0, 5),
    ("Little India", "Farrer Park", 0.8, 5),
    ("Farrer Park", "Boon Keng", 1.2, 6),
    ("Boon Keng", "Potong Pasir", 1.6, 6),
    ("Potong Pasir", "Woodleigh", 0.9, 5),
    ("Woodleigh", "Serangoon", 1.2, 6),
    ("Serangoon", "Kovan", 1.7, 6),
    ("Kovan", "Hougang", 1.5, 6),
    ("Hougang", "Buangkok", 1.3, 6),
    ("Buangkok", "Sengkang", 1.1, 5),
    ("Sengkang", "Punggol", 1.7, 6),
    ("Dhoby Ghaut", "Bras Basah", 0.6, 7),
    ("Bras Basah", "Esplanade", 0.7, 7),
    ("Esplanade", "Promenade", 0.8, 7),
    ("Promenade", "Nicoll Highway", 0.8, 7),
    ("Nicoll Highway", "Stadium", 1.5, 7),
    ("Stadium", "Mountbatten", 0.9, 7),
    ("Mountbatten", "Dakota", 0.7, 7),
    ("Dakota", "Paya Lebar", 1.2, 7),
    ("Paya Lebar", "MacPherson", 1.1, 7),
    ("MacPherson", "Tai Seng", 1.0, 7),
    ("Tai Seng", "Bartley", 1.3, 8),
    ("Bartley", "Serangoon", 1.3, 8),
    ("Serangoon", "Lorong Chuan", 0.9, 7),
    ("Lorong Chuan", "Bishan", 1.7, 8),
    ("Bishan", "Marymount", 1.6, 8),
    ("Marymount", "Caldecott", 1.2, 7),
    ("Caldecott", "Botanic Gardens", 3.9, 10),
    ("Botanic Gardens", "Farrer Road", 1.0, 7),
    ("Farrer Road", "Holland Village", 1.4, 8),
    ("Holland Village", "Buona Vista", 0.9, 7),
    ("Buona Vista", "one-north", 0.8, 7),
    ("one-north", "Kent Ridge", 0.8, 7),
    ("Kent Ridge", "Haw Par Villa", 1.4, 8),
    ("Haw Par Villa", "Pasir Panjang", 1.3, 7),
    ("Pasir Panjang", "Labrador Park", 1.4, 7),
    ("Labrador Park", "Telok Blangah", 0.8, 7),
    ("Telok Blangah", "HarbourFront", 1.5, 7),
    ("Promenade", "Bayfront", 1.3, 6),
    ("Bayfront", "Marina Bay", 0.8, 8),
    ("Bukit Panjang", "Cashew", 1.2, 6),
    ("Cashew", "Hillview", 0.9, 5),
    ("Hillview", "Beauty World", 2.6, 9),
    ("Beauty World", "King Albert Park", 1.2, 6),
    ("King Albert Park", "Sixth Avenue", 1.6, 6),
    ("Sixth Avenue", "Tan Kah Kee", 1.3, 5),
    ("Tan Kah Kee", "Botanic Gardens", 1.1, 5),
    ("Botanic Gardens", "Stevens", 1.1, 5),
    ("Stevens", "Newton", 1.6, 6),
    ("Newton", "Little India", 1.4, 6),
    ("Little India", "Rochor", 0.5, 5),
    ("Rochor", "Bugis", 0.8, 5),
    ("Bugis", "Promenade", 0.9, 5),
    ("Promenade", "Bayfront", 1.3, 6),
    ("Bayfront", "Downtown", 0.9, 5),
    ("Downtown", "Telok Ayer", 0.6, 5),
    ("Telok Ayer", "Chinatown", 0.6, 5),
    ("Chinatown", "Fort Canning", 1.0, 6),
    ("Fort Canning", "Bencoolen", 1.0, 5),
    ("Bencoolen", "Jalan Besar", 0.9, 5),
    ("Jalan Besar", "Bendemeer", 1.3, 6),
    ("Bendemeer", "Geylang Bahru", 1.4, 5),
    ("Geylang Bahru", "Mattar", 1.5, 5),
    ("Mattar", "MacPherson", 0.8, 5),
    ("MacPherson", "Ubi", 1.1, 5),
    ("Ubi", "Kaki Bukit", 1.2, 5),
    ("Kaki Bukit", "Bedok North", 1.1, 5),
    ("Bedok North", "Bedok Reservoir", 1.8, 5),
    ("Bedok Reservoir", "Tampines West", 1.7, 6),
    ("Tampines West", "Tampines", 1.3, 6),
    ("Tampines", "Tampines East", 1.4, 5),
    ("Tampines East", "Upper Changi", 2.6, 7),
    ("Upper Changi", "Expo", 0.9, 5),
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


def dijkstra(graph, start, end, mode="distance"):
    """
    Compute shortest path based on selected mode:
    - 'distance' → prioritize distance
    - 'time' → prioritize time
    - 'balanced' → mix distance & time equally
    """
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

            # Determine edge weight based on mode
            if mode == "distance":
                weight = d
            elif mode == "time":
                weight = t
            else:  # balanced
                weight = 0.5 * d + 0.5 * t  # normalize both

            alt = dist[current] + weight
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

def bfs(graph, start, end):
    """Find path with the fewest stations (unweighted)."""
    if start not in graph or end not in graph:
        return None, None, "Start or end station not found."

    queue = deque([[start]])
    visited = set()

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == end:
            # Compute totals (distance, time, fare)
            total_distance = 0.0
            total_time = 0.0
            total_price = 0.0
            for i in range(len(path) - 1):
                cur = path[i]
                nxt = path[i + 1]
                for neighbor, d, t, p in graph[cur]:
                    if neighbor == nxt:
                        total_distance += d
                        total_time += t
                        total_price += p
                        break
            return [(path[i], path[i + 1], 0, 0, 0) for i in range(len(path) - 1)], {
                "distance": total_distance,
                "time": total_time,
                "price": total_price,
            }, None

        if node not in visited:
            visited.add(node)
            for neighbor, _, _, _ in graph.get(node, []):
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

    return None, None, "No path found."


# ---------- GUI ----------
class MRTApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🚇 Singapore MRT Route Finder")
        self.geometry("800x850")
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

        # Route mode
        ttk.Label(frm_inputs, text="Route Type:").grid(row=1, column=0, padx=5, pady=10, sticky="e")
        self.mode_var = tk.StringVar(value="distance")
        ttk.Combobox(
            frm_inputs,
            values=["distance", "time", "balanced", "bfs"],
            textvariable=self.mode_var,
            width=25,
        ).grid(row=1, column=1, padx=5)
        frm_buttons = ttk.Frame(frm_main)
        frm_buttons.pack(pady=15)

        ttk.Button(frm_buttons, text="Load CSV", command=self.load_csv).pack(side="left", padx=10)
        ttk.Button(frm_buttons, text="Find Route", command=self.find_path).pack(side="left", padx=10)
        ttk.Button(frm_buttons, text="Reset to Default", command=self.reset_graph).pack(side="left", padx=10)

        self.result_frame = ttk.Frame(frm_main)
        self.result_frame.pack(pady=10, fill="x")

        self.result_label = ttk.Label(self.result_frame, text="", font=("Segoe UI", 11), foreground="#333", wraplength=650, justify="center")
        self.result_label.pack()

        ttk.Separator(frm_main, orient="horizontal").pack(fill="x", pady=5)

        try:
            img = Image.open(os.path.join(BASE_DIR, "mrtMapLimit.png"))
            img = img.resize((720, 420))
            self.mrt_img = ImageTk.PhotoImage(img)
            ttk.Label(frm_main, image=self.mrt_img).pack(pady=10)
        except Exception as e:
            ttk.Label(frm_main, text=f"⚠️ Could not load mrtMapLimit.png: {e}", foreground="red").pack()
            
    def load_csv(self):
        path = filedialog.askopenfilename(
            title="Open CSV",
            filetypes=[("CSV files", "*.csv")]
        )
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


    def find_path(self):
        start = self.start_var.get().strip()
        end = self.end_var.get().strip()
        mode = self.mode_var.get().strip().lower()

        if mode == "bfs":
            path, totals, err = bfs(self.graph, start, end)
        else:
            path, totals, err = dijkstra(self.graph, start, end, mode)
        if err:
            messagebox.showerror("Error", err)
            return

        route = " → ".join([u for u, _, _, _, _ in path] + [end])
        result_text = (
            f"{route}\n"
            f"⏱️  Time: {totals['time']:.0f} min "
            f"📏  Distance: {totals['distance']:.1f} km "
            f"💵  Fare: ${totals['price']:.2f}\n\n"
            f"🧭 Mode: {mode.capitalize()}"
        )

        self.result_label.config(text=result_text)

if __name__ == "__main__":
    app = MRTApp()
    app.mainloop()