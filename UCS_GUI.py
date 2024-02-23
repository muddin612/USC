import tkinter as tk
from tkinter import messagebox, Scrollbar
import networkx as nx
from UCS import UCS

class UCS_GUI:
    def __init__(self, root, graph):
        self.root = root
        self.root.title("UCS Algorithm GUI")
        self.graph = graph
        self.G = nx.Graph(self.graph)
        self.path = None

        self.create_widgets()

    def create_widgets(self):
        # Entry for start node
        self.label_start = tk.Label(self.root, text="Start Node:")
        self.label_start.grid(row=0, column=0)
        self.entry_start = tk.Entry(self.root)
        self.entry_start.grid(row=0, column=1)

        # Entry for goal node
        self.label_goal = tk.Label(self.root, text="Goal Node:")
        self.label_goal.grid(row=1, column=0)
        self.entry_goal = tk.Entry(self.root)
        self.entry_goal.grid(row=1, column=1)

        # Button to find shortest path
        self.button_find_path = tk.Button(self.root, text="Find Shortest Path", command=self.find_shortest_path)
        self.button_find_path.grid(row=2, columnspan=2)

        # Button to visualize graph
        self.button_visualize_graph = tk.Button(self.root, text="Visualize Graph", command=self.visualize_graph)
        self.button_visualize_graph.grid(row=3, columnspan=2)

        # Create a frame to hold the canvas and scrollbar
        self.frame_canvas = tk.Frame(self.root)
        self.frame_canvas.grid(row=0, column=2, rowspan=5, sticky='nsew')

        # Canvas for graph visualization
        self.canvas = tk.Canvas(self.frame_canvas, bg="white")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Scrollbar for canvas
        self.scrollbar = Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame_graph = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0,0), window=self.frame_graph, anchor='nw')
        self.frame_graph.bind("<Configure>", self.on_frame_configure)

    def find_shortest_path(self):
        start = self.entry_start.get()
        goal = self.entry_goal.get()

        if start not in self.graph or goal not in self.graph:
            messagebox.showerror("Error", "Invalid start or goal node")
            return

        path, total_cost = UCS(self.graph, start, goal)
        if path:
            messagebox.showinfo("Shortest Path", f"Shortest path from {start} to {goal}: {path}\nTotal Cost: {total_cost}")
            self.path = path
            self.visualize_graph()
        else:
            messagebox.showerror("Error", f"No path found from {start} to {goal}")

    def visualize_graph(self):
        self.canvas.delete("graph")
        pos = nx.spring_layout(self.G)

        # Calculate canvas size based on graph layout
        max_x = max(pos[node][0] for node in pos)
        max_y = max(pos[node][1] for node in pos)
        canvas_width = int((max_x + 1) * 100)
        canvas_height = int((max_y + 1) * 100)
        self.canvas.config(width=canvas_width, height=canvas_height)

        # Draw nodes and edges
        for node in self.G.nodes:
            x, y = pos[node]
            x = x * 100
            y = y * 100
            self.canvas.create_oval(x, y, x + 50, y + 50, fill="skyblue", tags="graph")
            self.canvas.create_text(x + 25, y + 25, text=node, font=("Helvetica", 12), tags="graph")

        for edge in self.G.edges:
            x1, y1 = pos[edge[0]]
            x2, y2 = pos[edge[1]]
            x1 = x1 * 100
            y1 = y1 * 100
            x2 = x2 * 100
            y2 = y2 * 100
            self.canvas.create_line(x1 + 25, y1 + 25, x2 + 25, y2 + 25, fill="black", tags="graph")

        # Highlight shortest path
        if self.path:
            for i in range(len(self.path) - 1):
                start_node = self.path[i]
                end_node = self.path[i + 1]
                x1, y1 = pos[start_node]
                x2, y2 = pos[end_node]
                x1 = x1 * 100
                y1 = y1 * 100
                x2 = x2 * 100
                y2 = y2 * 100
                self.canvas.create_line(x1 + 25, y1 + 25, x2 + 25, y2 + 25, fill="red", width=2, tags="graph")

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    app = UCS_GUI(root, {
        'Entrance': {'Lobby': 2},
        'Lobby': {'Hallway1': 3, 'Hallway2': 4},
        'Hallway1': {'Room1': 2, 'Stairs1': 3},
        'Hallway2': {'Room2': 2, 'Stairs2': 2},
        'Room1': {'Hallway1': 2, 'Exit1': 5},
        'Room2': {'Hallway2': 2, 'Exit2': 4},
        'Stairs1': {'Lobby': 2, 'Floor2_Lobby': 3},
        'Stairs2': {'Lobby': 2, 'Floor2_Lobby': 4},
        'Floor2_Lobby': {'Floor2_Hallway1': 3, 'Floor2_Hallway2': 4},
        'Floor2_Hallway1': {'Floor2_Room1': 2, 'Stairs3': 3},
        'Floor2_Hallway2': {'Floor2_Room2': 2, 'Stairs3': 4},
        'Floor2_Room1': {'Floor2_Hallway1': 2, 'Exit3': 6},
        'Floor2_Room2': {'Floor2_Hallway2': 2},
        'Stairs3': {'Floor2_Lobby': 3, 'Ground_Lobby': 4},
        'Ground_Lobby': {'Exit4': 6},
        'Exit1': {},
        'Exit2': {},
        'Exit3': {},
        'Exit4': {}
    })
    root.mainloop()
