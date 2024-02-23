from queue import PriorityQueue

def UCS(graph, start, goal):
    explore = PriorityQueue()
    explore.put((0, start))
    visited = set()
    parent = {}
    cost = {node: float('inf') for node in graph}
    cost[start] = 0


    while not explore.empty():
        current_cost , current = explore.get()

        if current == goal:
            path = [current]
            while current in parent:
                current = parent[current]
                path.append(current)
            path.reverse()
            return path, cost[goal]
        
        visited.add(current)

        for next_node, next_cost in graph[current].items():
            new_cost = cost[current] + next_cost
            if next_node not in visited and new_cost < cost[next_node]:
                cost[next_node] = new_cost
                explore.put((new_cost, next_node))
                parent[next_node] = current
    return None

graph = {
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
}

path, total_cost = UCS(graph, 'Entrance','Exit4')
print("Path: ", path)
print("Total Cost: ", total_cost)