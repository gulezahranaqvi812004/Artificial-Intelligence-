import matplotlib.pyplot as plt
import networkx as nx
from collections import deque

class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.is_directed = False
        self.adjacency_matrix = []

    def read_graph_from_file(self, filename="D:\Semester5\AIThoery\PS1\\2022-CS-75\graph.txt"):
        try:
            with open(filename, 'r') as file:
                first_line = file.readline().strip().split('_')
                num_vertices = int(first_line[0])
                self.is_directed = (first_line[1] == '1')
                
                self.vertices = file.readline().strip().split()
                
                if num_vertices != len(self.vertices):
                    raise ValueError("Number of vertices does not match the number of vertex names provided.")
                
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

                self.print_graph_state()
        
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except ValueError as ve:
            print(ve)
        except Exception as e:
            print(f"An error occurred: {e}")

    def print_graph_state(self):
        print("\n--- Graph State ---")
        print(f"Vertices: {self.vertices}")
        print(f"Edges: {self.edges}")
        print(f"Is the graph directed? {'Yes' if self.is_directed else 'No'}")
        print("Adjacency matrix:")
        for row in self.adjacency_matrix:
            print(" ".join(map(str, row)))

    def get_vertex_count(self):
        return len(self.vertices)

    def get_edge_count(self):
        return len(self.edges)

    def is_graph_directed(self):
        return self.is_directed

    def get_neighbors(self, vertex):
        if vertex not in self.vertices:
            return []
        
        vertex_index = self.vertices.index(vertex)
        neighbors = []
        for idx, is_edge in enumerate(self.adjacency_matrix[vertex_index]):
            if is_edge:
                neighbors.append(self.vertices[idx])
        return neighbors

    

    def bfs(self, start_vertex):
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
        
        max_distance = max(distances.values())
        return max_distance + 1

    def bfs_draw_tree(self, start_vertex):
        G = nx.DiGraph()
        for vertex in self.vertices:
            G.add_node(vertex)
        for start, end in self.edges:
            G.add_edge(start, end)
            if not self.is_graph_directed():
                G.add_edge(end, start)
        
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, arrows=True)
        plt.title("BFS Tree")
        plt.show()

def print_graph_info():
    graph = Graph()
    graph.read_graph_from_file()
    
    print("\n--- Graph Information ---")
    print(f"Number of vertices: {graph.get_vertex_count()}")
    print(f"Number of edges: {graph.get_edge_count()}")
    print(f"Is the graph directed? {'Yes' if graph.is_graph_directed() else 'No'}")
    
    for vertex in graph.vertices:
        neighbors = graph.get_neighbors(vertex)
        print(f"Neighbors of {vertex}: {', '.join(neighbors) if neighbors else 'None'}")
    
   
    
    print("\n--- BFS ---")
    bfs_order = graph.bfs(graph.vertices[0])  # Assuming start_vertex is the first in list
    print(f"Order of nodes visited in BFS: {bfs_order}")
    for vertex in graph.vertices:
        print(f"Distance from {graph.vertices[0]} to {vertex}: {graph.bfs_distance(graph.vertices[0], vertex)}")
    print(f"Number of levels in the BFS tree: {graph.bfs_number_of_levels(graph.vertices[0], graph.vertices[-1])}")
    graph.bfs_draw_tree(graph.vertices[0])

if __name__ == "__main__":
    print_graph_info()
