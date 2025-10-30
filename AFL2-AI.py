"""
Singapore MRT Shortest Path Finder (by Distance + Time Prediction)
- Dijkstra Algorithm (undirected / dua arah otomatis)
- Optimasi berdasarkan jarak terdekat (km)
- Juga menghitung total waktu (menit)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import math


# ---------- Sample Graph Data (jarak km, waktu menit) ----------
SAMPLE_EDGES =[
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


# ---------- Graph Utilities ----------
def build_graph(edges):
    """Build graph dua arah (undirected)."""
    graph = {}
    nodes = set()
    for u, v, d, t in edges:
        nodes.update([u, v])
        graph.setdefault(u, []).append((v, d, t))
        graph.setdefault(v, []).append((u, d, t))
    for n in nodes:
        graph.setdefault(n, [])
    return graph


def dijkstra(graph, start, end, mode="distance", weight=0.5):
    """Dijkstra dengan mode distance / time / combined."""
    if start not in graph:
        return None, None, None, f"Start station '{start}' not found."
    if end not in graph:
        return None, None, None, f"End station '{end}' not found."
    if start == end:
        return [], 0, 0, None

    dist = {n: math.inf for n in graph}
    prev = {n: None for n in graph}
    time_taken = {n: 0 for n in graph}
    dist[start] = 0
    unvisited = set(graph.keys())

    while unvisited:
        current = min(unvisited, key=lambda n: dist[n])
        if dist[current] == math.inf:
            break
        unvisited.remove(current)

        if current == end:
            break

        for (neighbor, d, t) in graph[current]:
            # Tentukan cost
            if mode == "distance":
                cost = d
            elif mode == "time":
                cost = t
            else:  # combined mode
                cost = (1 - weight) * d + weight * t

            alt = dist[current] + cost
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = (current, d, t)
                time_taken[neighbor] = time_taken[current] + t

    if dist[end] == math.inf:
        return None, None, None, "No path found."

    # Rekonstruksi path
    path = []
    total_dist = 0
    total_time = 0
    cur = end
    while cur in prev and prev[cur] is not None:
        prev_node, d, t = prev[cur]
        path.append((prev_node, cur, d, t))
        total_dist += d
        total_time += t
        cur = prev_node
    path.reverse()

    return path, total_dist, total_time, None


# ---------- GUI ----------
class MRTApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Singapore MRT - Shortest Path Finder (Distance / Time / Combined)")
        self.geometry("880x640")
        self.resizable(False, False)

        self.edges = SAMPLE_EDGES.copy()
        self.graph = build_graph(self.edges)
        self.stations = sorted(self.graph.keys())

        self.create_widgets()

    def create_widgets(self):
        frm_left = ttk.Frame(self, padding=12)
        frm_left.place(x=10, y=10, width=380, height=600)

        ttk.Label(frm_left, text="Start Station:").pack(anchor="w")
        self.start_var = tk.StringVar(value=self.stations[0])
        self.start_combo = ttk.Combobox(frm_left, values=self.stations, textvariable=self.start_var, width=40)
        self.start_combo.pack(fill="x", pady=4)

        ttk.Label(frm_left, text="End Station:").pack(anchor="w", pady=(8, 0))
        self.end_var = tk.StringVar(value=self.stations[-1])
        self.end_combo = ttk.Combobox(frm_left, values=self.stations, textvariable=self.end_var, width=40)
        self.end_combo.pack(fill="x", pady=4)

        ttk.Label(frm_left, text="Mode Optimasi:").pack(anchor="w", pady=(8, 0))
        self.mode_var = tk.StringVar(value="distance")
        mode_combo = ttk.Combobox(frm_left, values=["distance", "time", "combined"], textvariable=self.mode_var, width=20)
        mode_combo.pack(fill="x", pady=4)

        ttk.Label(frm_left, text="Bobot Kombinasi (0 = Jarak, 1 = Waktu):").pack(anchor="w", pady=(8, 0))
        self.weight_var = tk.DoubleVar(value=0.5)
        self.weight_slider = ttk.Scale(frm_left, from_=0, to=1, orient="horizontal", variable=self.weight_var)
        self.weight_slider.pack(fill="x", pady=4)

        ttk.Button(frm_left, text="Cari Jalur", command=self.find_path).pack(fill="x", pady=(12, 4))
        ttk.Button(frm_left, text="Load dari CSV", command=self.load_csv).pack(fill="x", pady=4)
        ttk.Button(frm_left, text="Reset ke Data Demo", command=self.reset_graph).pack(fill="x", pady=4)

        frm_right = ttk.Frame(self, padding=12)
        frm_right.place(x=400, y=10, width=470, height=600)

        ttk.Label(frm_right, text="Hasil Jalur Terpendek / Tercepat / Gabungan:").pack(anchor="w")
        self.result_txt = tk.Text(frm_right, height=18, width=60, state="disabled", wrap="word")
        self.result_txt.pack(pady=4)

        ttk.Label(frm_right, text="Edges (dua arah, A ↔ B : km, menit):").pack(anchor="w", pady=(8, 0))
        self.edges_list = tk.Text(frm_right, height=14, width=60, state="disabled", wrap="none")
        self.edges_list.pack(pady=4)
        self.refresh_edges_display()

    def refresh_edges_display(self):
        self.edges_list.config(state="normal")
        self.edges_list.delete("1.0", tk.END)
        for u, v, d, t in self.edges:
            self.edges_list.insert(tk.END, f"{u} ↔ {v} : {d:.2f} km, {t:.0f} menit\n")
        self.edges_list.config(state="disabled")

        self.graph = build_graph(self.edges)
        self.stations = sorted(self.graph.keys())
        self.start_combo.config(values=self.stations)
        self.end_combo.config(values=self.stations)

    def find_path(self):
        start = self.start_var.get().strip()
        end = self.end_var.get().strip()
        mode = self.mode_var.get().strip().lower()
        weight = float(self.weight_var.get())

        path, total_dist, total_time, err = dijkstra(self.graph, start, end, mode, weight)
        self.result_txt.config(state="normal")
        self.result_txt.delete("1.0", tk.END)

        if err:
            self.result_txt.insert(tk.END, f"⚠️ {err}\n")
        else:
            label_mode = {
                "distance": "TERDEKAT (berdasarkan jarak)",
                "time": "TERCEPAT (berdasarkan waktu)",
                "combined": f"GABUNGAN (w={weight:.2f})"
            }[mode]
            self.result_txt.insert(tk.END, f"Jalur {label_mode} dari {start} ke {end}\n\n")
            for u, v, d, t in path:
                self.result_txt.insert(tk.END, f"{u} → {v} : {d:.2f} km, {t:.0f} menit\n")
            self.result_txt.insert(tk.END, f"\nTotal jarak: {total_dist:.2f} km\n")
            self.result_txt.insert(tk.END, f"Total waktu: {total_time:.0f} menit\n")
        self.result_txt.config(state="disabled")

    def load_csv(self):
        path = filedialog.askopenfilename(title="Open CSV", filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        try:
            new_edges = []
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) < 4:
                        continue
                    u, v = row[0].strip(), row[1].strip()
                    d, t = float(row[2]), float(row[3])
                    new_edges.append((u, v, d, t))
            if not new_edges:
                messagebox.showwarning("No edges", "CSV harus berisi station1,station2,jarak_km,waktu_menit.")
                return
            self.edges = new_edges
            self.refresh_edges_display()
            messagebox.showinfo("Loaded", f"Loaded {len(new_edges)} edges dari CSV.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal load CSV: {e}")

    def reset_graph(self):
        self.edges = SAMPLE_EDGES.copy()
        self.refresh_edges_display()
        messagebox.showinfo("Reset", "Graph direset ke data demo.")


if __name__ == "__main__":
    app = MRTApp()
    app.mainloop()
