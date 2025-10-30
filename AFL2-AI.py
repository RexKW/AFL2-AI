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
