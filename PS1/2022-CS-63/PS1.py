import heapq
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque


import heapq
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque

class Graph:
    
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.is_directed = False
        self.adjacency_matrix = []

    def load_from_file(self, filename="graph.txt"):
        try:
            with open(filename, 'r') as file:
                first_line = file.readline().strip().split('_')
                num_vertices = int(first_line[0])
                self.is_directed = (first_line[1] == '1')
                
                self.vertices = file.readline().strip().split()
                
                if num_vertices != len(self.vertices):
                    raise ValueError("The number of vertices provided does not match the number of vertex names in the file.")
                
                self.adjacency_matrix = [[0] * num_vertices for _ in range(num_vertices)]
                
                vertex_index = {vertex: idx for idx, vertex in enumerate(self.vertices)}
                
                num_edges = int(file.readline().strip())
                
                self.edges = []
                for _ in range(num_edges):
                    start, end = file.readline().strip().split()
                    self.edges.append((start, end))
                    start_idx = vertex_index[start]
                    end_idx = vertex_index[end]
                    self.adjacency_matrix[start_idx][end_idx] = 1
                    if not self.is_directed:
                        self.adjacency_matrix[end_idx][start_idx] = 1

                self.display_graph_info()
        
        except FileNotFoundError:
            print(f"Oops! The file '{filename}' couldn't be found.")
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"Something went wrong: {e}")

    def display_graph_info(self):
        print("Graph Information:")
        print(f"Vertices: {self.vertices}")
        print(f"Edges: {self.edges}")
        print(f"Directed: {'Yes' if self.is_directed else 'No'}")
        print("Adjacency Matrix:")
        for row in self.adjacency_matrix:
            formatted_row = ""
            for value in row:
                formatted_row += str(value) + " "
            print(formatted_row.strip())

    def get_vertex_count(self):
        return len(self.vertices)

    def get_edge_count(self):
        return len(self.edges)

    def is_directed_graph(self):
        return self.is_directed

    def get_neighbors(self, vertex):
        if vertex not in self.vertices:
            return []
        vertex_index = self.vertices.index(vertex)
        neighbors = []
        for i in range(len(self.adjacency_matrix[vertex_index])):
            if self.adjacency_matrix[vertex_index][i] == 1:
                neighbors.append(self.vertices[i])
        return neighbors

    def depth_first_search(self, start_vertex):
        visited = set()
        order = []
        def dfs_recursive(vertex):
            if vertex not in visited:
                visited.add(vertex)
                order.append(vertex)
                for neighbor in self.get_neighbors(vertex):
                    dfs_recursive(neighbor)
        dfs_recursive(start_vertex)
        return tuple(order)

    def draw_dfs_tree(self, start_vertex):
        G = nx.DiGraph()
        G.add_nodes_from(self.vertices)
        for start, end in self.edges:
            G.add_edge(start, end)
            if not self.is_directed_graph():
                G.add_edge(end, start)
        nx.draw(G, with_labels=True, arrows=True)
        plt.title("DFS Tree")
        plt.show()

    def breadth_first_search(self, start_vertex):
        visited = set()
        order = []
        queue = deque([start_vertex])
        visited.add(start_vertex)
        while queue:
            vertex = queue.popleft()
            order.append(vertex)
            for neighbor in self.get_neighbors(vertex):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return tuple(order)

    def bfs_distance(self, start_vertex, end_vertex):
        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[start_vertex] = 0
        queue = deque([start_vertex])
        while queue:
            vertex = queue.popleft()
            for neighbor in self.get_neighbors(vertex):
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = distances[vertex] + 1
                    queue.append(neighbor)
        return distances.get(end_vertex, -1)

    def bfs_number_of_levels(self, start_vertex, end_vertex):
        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[start_vertex] = 0
        queue = deque([start_vertex])
        while queue:
            vertex = queue.popleft()
            for neighbor in self.get_neighbors(vertex):
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = distances[vertex] + 1
                    queue.append(neighbor)
        return max(distances.values()) + 1

    def draw_bfs_tree(self, start_vertex):
        G = nx.DiGraph()
        for vertex in self.vertices:
            G.add_node(vertex)
        for start, end in self.edges:
            G.add_edge(start, end)
            if not self.is_directed_graph():
                G.add_edge(end, start)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, arrows=True)
        plt.title("BFS Tree")
        plt.show()

    def is_acyclic(self):
        def dfs(vertex, visited, rec_stack):
            visited.add(vertex)
            rec_stack.add(vertex)
            for neighbor in self.get_neighbors(vertex):
                if neighbor not in visited:
                    if dfs(neighbor, visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(vertex)
            return False
        visited = set()
        rec_stack = set()
        for vertex in self.vertices:
            if vertex not in visited:
                if dfs(vertex, visited, rec_stack):
                    return False
        return True

    def count_cycles(self):
        def dfs(vertex, visited, stack):
            visited.add(vertex)
            stack.add(vertex)
            cycles = 0
            for neighbor in self.get_neighbors(vertex):
                if neighbor not in visited:
                    result, new_cycles = dfs(neighbor, visited, stack)
                    cycles += new_cycles
                elif neighbor in stack:
                    cycles += 1
            stack.remove(vertex)
            return True, cycles
        visited = set()
        stack = set()
        total_cycles = 0
        for vertex in self.vertices:
            if vertex not in visited:
                _, cycles = dfs(vertex, visited, stack)
                total_cycles += cycles
        return total_cycles

    def shortest_path_dijkstra(self, start_vertex, end_vertex):
        if start_vertex not in self.vertices or end_vertex not in self.vertices:
            raise ValueError(f"One or both vertices '{start_vertex}' or '{end_vertex}' are not in the graph.")
        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[start_vertex] = 0
        path = {vertex: None for vertex in self.vertices}
        priority_queue = [(0, start_vertex)]
        while priority_queue:
            current_distance, u = heapq.heappop(priority_queue)
            if u == end_vertex:
                break
            if current_distance > distances[u]:
                continue
            for neighbor in self.get_neighbors(u):
                weight = self.adjacency_matrix[self.vertices.index(u)][self.vertices.index(neighbor)]
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    path[neighbor] = (u, weight)
                    heapq.heappush(priority_queue, (distance, neighbor))
        if distances[end_vertex] == float('inf'):
            return (float('inf'), [])
        total_path = []
        current = end_vertex
        while path[current] is not None:
            previous, weight = path[current]
            total_path.append((previous, current, weight))
            current = previous
        total_path.reverse()
        return (distances[end_vertex], total_path)

    def shortest_path_bellmanford(self, start_vertex, end_vertex):
        if start_vertex not in self.vertices or end_vertex not in self.vertices:
            raise ValueError(f"One or both vertices '{start_vertex}' or '{end_vertex}' are not in the graph.")
        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[start_vertex] = 0
        path = {vertex: None for vertex in self.vertices}
        for _ in range(len(self.vertices) - 1):
            for u, v in self.edges:
                weight = self.adjacency_matrix[self.vertices.index(u)][self.vertices.index(v)]
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    path[v] = u
        for u, v in self.edges:
            weight = self.adjacency_matrix[self.vertices.index(u)][self.vertices.index(v)]
            if distances[u] + weight < distances[v]:
                raise ValueError("Graph contains a negative weight cycle.")
        if distances[end_vertex] == float('inf'):
            return (float('inf'), [])
        total_path = []
        current = end_vertex
        while path[current] is not None:
            previous = path[current]
            total_path.append((previous, current))
            current = previous
        total_path.reverse()
        return (distances[end_vertex], total_path)

def main():
    # Create an instance of the Graph class
    graph = Graph()

    # Load graph data from the file
    graph.load_from_file()

    # Task1
    graph.display_graph_info()

    # Task2
    start_vertex = graph.vertices[0]  # Assuming vertices are not empty
    print(f"DFS Order starting from '{start_vertex}': {graph.depth_first_search(start_vertex)}")

    # Task3 a
    print(f"BFS Order starting from '{start_vertex}': {graph.breadth_first_search(start_vertex)}")

    # Task3 b
    end_vertex = graph.vertices[-1]  # Assuming vertices are not empty
    print(f"Distance from '{start_vertex}' to '{end_vertex}': {graph.bfs_distance(start_vertex, end_vertex)}")

    # Task3 c
    print(f"Number of levels from '{start_vertex}' to '{end_vertex}': {graph.bfs_number_of_levels(start_vertex, end_vertex)}")

    # Task3 d
    graph.draw_bfs_tree(start_vertex)
    graph.draw_dfs_tree(start_vertex)

    # Task4 q
    print(f"Is the graph acyclic? {'Yes' if graph.is_acyclic() else 'No'}")

    # Task4 b
    print(f"Number of cycles in the graph: {graph.count_cycles()}")

    # Task5 a
    if len(graph.vertices) > 1:
        print(f"Shortest path from '{start_vertex}' to '{end_vertex}' using Dijkstra: {graph.shortest_path_dijkstra(start_vertex, end_vertex)}")

    # Task5 b
    if len(graph.vertices) > 1:
        print(f"Shortest path from '{start_vertex}' to '{end_vertex}' using Bellman-Ford: {graph.shortest_path_bellmanford(start_vertex, end_vertex)}")

if __name__ == "__main__":
    main()
