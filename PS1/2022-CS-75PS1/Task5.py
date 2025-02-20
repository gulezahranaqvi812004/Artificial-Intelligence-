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

    def dfs(self, start_vertex):
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

    def dfs_draw_tree(self, start_vertex):
        G = nx.DiGraph()
        for vertex in self.vertices:
            G.add_node(vertex)
        for start, end in self.edges:
            G.add_edge(start, end)
            if not self.is_graph_directed():
                G.add_edge(end, start)
        
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, arrows=True)
        plt.title("DFS Tree")
        plt.show()

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

    def is_acyclic(self):
        def dfs(v, visited, rec_stack):
            visited.add(v)
            rec_stack.add(v)
            
            for neighbor in self.get_neighbors(v):
                if neighbor not in visited:
                    if dfs(neighbor, visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(v)
            return False
        
        visited = set()
        rec_stack = set()
        
        for vertex in self.vertices:
            if vertex not in visited:
                if dfs(vertex, visited, rec_stack):
                    return False  # Cycle found
        
        return True  # No cycles found

    def count_cycles(self):
        def dfs(v, visited, stack):
            visited.add(v)
            stack.add(v)
            cycles = 0
            
            for neighbor in self.get_neighbors(v):
                if neighbor not in visited:
                    result, new_cycles = dfs(neighbor, visited, stack)
                    cycles += new_cycles
                elif neighbor in stack:
                    cycles += 1  # Found a cycle
            
            stack.remove(v)
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
            raise ValueError(f"Either '{start_vertex}' or '{end_vertex}' or both are not in the graph")
        
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
            return (float('inf'), [])  # No path found
        
        total_path = []
        current = end_vertex
        while path[current] is not None:
            previous, weight = path[current]
            total_path.append((previous, current, weight))
            current = previous
        total_path.reverse()
        
        return (distances[end_vertex], total_path)

    def shortest_path_bellmanford(self, start_vertex, end_vertex):
        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[start_vertex] = 0
        path = {vertex: None for vertex in self.vertices}
        
        for _ in range(len(self.vertices) - 1):
            for u, v in self.edges:
                weight = self.adjacency_matrix[self.vertices.index(u)][self.vertices.index(v)]
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    path[v] = (u, weight)
        
        # Check for negative-weight cycles
        for u, v in self.edges:
            weight = self.adjacency_matrix[self.vertices.index(u)][self.vertices.index(v)]
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                print("Graph contains a negative weight cycle")
                return (float('inf'), [])
        
        if distances[end_vertex] == float('inf'):
            return (float('inf'), [])  # No path found
        
        total_path = []
        current = end_vertex
        while path[current] is not None:
            previous, weight = path[current]
            total_path.append((previous, current, weight))
            current = previous
        total_path.reverse()
        
        return (distances[end_vertex], total_path)

def main():
    graph = Graph()
    graph.read_graph_from_file("graph.txt")
    
    print("\n--- Graph State ---")
    print(f"Vertex count: {graph.get_vertex_count()}")
    print(f"Edge count: {graph.get_edge_count()}")
    
    for vertex in graph.vertices:
        neighbors = graph.get_neighbors(vertex)
        print(f"Neighbors of {vertex}: {neighbors}")
    
    try:
        acyclic = graph.is_acyclic()
        if acyclic:
            print("\nThe graph is acyclic.")
        else:
            print("\nThe graph is not acyclic.")
            print(f"Number of cycles: {graph.count_cycles()}")
        
        distance, path = graph.shortest_path_dijkstra('A', 'C')
        print(f"\nDijkstra: Distance = {distance}, Path = {path}")
        
        distance, path = graph.shortest_path_bellmanford('A', 'C')
        print(f"Bellman-Ford: Distance = {distance}, Path = {path}")
    
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
