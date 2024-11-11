import matplotlib.pyplot as plt
import networkx as nx
from collections import deque, defaultdict

class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.is_directed = False
        self.adjacency_matrix = []
        self.graph_dict = defaultdict(list)  # For cycle detection

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
                    self.graph_dict[start].append(end)
                    if not self.is_directed:
                        self.graph_dict[end].append(start)

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

    def is_acyclic(self):
        visited = set()
        rec_stack = set()  # To track nodes in the current path

        def has_cycle(v):
            visited.add(v)
            rec_stack.add(v)
            
            for neighbor in self.graph_dict[v]:
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(v)
            return False

        for vertex in self.vertices:
            if vertex not in visited:
                if has_cycle(vertex):
                    print(f"Cycle detected starting from vertex: {vertex}")
                    return False
        
        return True

    def find_cycles(self):
        cycles = []
        visited = set()
        rec_stack = set()  # To track nodes in the current path

        def find_cycle(v, path):
            visited.add(v)
            rec_stack.add(v)
            path.append(v)
            
            for neighbor in self.graph_dict[v]:
                if neighbor not in visited:
                    if find_cycle(neighbor, path):
                        return True
                elif neighbor in rec_stack:
                    cycle_start_index = path.index(neighbor)
                    cycles.append(path[cycle_start_index:] + [neighbor])
                    return True

            rec_stack.remove(v)
            path.pop()
            return False

        for vertex in self.vertices:
            if vertex not in visited:
                find_cycle(vertex, [])

        return cycles

    def output_cycles(self):
        cycles = self.find_cycles()
        if not cycles:
            print("No cycles found.")
        else:
            print(f"Number of cycles: {len(cycles)}")
            for i, cycle in enumerate(cycles):
                print(f"Cycle {i + 1}: {' -> '.join(cycle)}")

def main():
    graph = Graph()
    graph.read_graph_from_file()

    if graph.is_acyclic():
        print("The graph is acyclic.")
    else:
        print("The graph is not acyclic.")
        graph.output_cycles()

if __name__ == "__main__":
    main()
