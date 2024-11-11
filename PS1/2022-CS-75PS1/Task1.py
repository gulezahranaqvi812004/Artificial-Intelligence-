class Graph:
    def __init__(self):
        self.vertices = []  # List to store vertex names
        self.edges = []  # List to store edges as tuples (start, end)
        self.is_directed = False  # To store whether the graph is directed
        self.adjacency_matrix = []  # 2D list to store adjacency matrix

    def read_graph_from_file(self, filename="D:\Semester5\AIThoery\PS1\\2022-CS-75\graph.txt"):
        """
        Reads the graph from a file with the specified format and represents it with an adjacency matrix.
        Input: filename - name of the file containing the graph.
        """
        try:
            with open(filename, 'r') as file:
                # First line: number of vertices and directed/undirected status
                first_line = file.readline().strip().split('_')
                num_vertices = int(first_line[0])
                self.is_directed = (first_line[1] == '1')
                
                # Second line: vertices names
                self.vertices = file.readline().strip().split()
                
                # Check if the number of vertices matches the list length
                if num_vertices != len(self.vertices):
                    raise ValueError("Number of vertices does not match the number of vertex names provided.")
                
                # Initialize adjacency matrix
                self.adjacency_matrix = [[0] * num_vertices for _ in range(num_vertices)]
                
                # Mapping vertex names to indices
                vertex_index = {vertex: idx for idx, vertex in enumerate(self.vertices)}
                
                # Third line: number of edges
                num_edges = int(file.readline().strip())
                
                # Next lines: edges between vertices
                self.edges = []
                for _ in range(num_edges):
                    start, end = file.readline().strip().split()
                    self.edges.append((start, end))
                    start_idx = vertex_index[start]
                    end_idx = vertex_index[end]
                    self.adjacency_matrix[start_idx][end_idx] = 1
                    if not self.is_directed:
                        self.adjacency_matrix[end_idx][start_idx] = 1

                # Print the graph's internal state
                self.print_graph_state()
        
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except ValueError as ve:
            print(ve)
        except Exception as e:
            print(f"An error occurred: {e}")

    def print_graph_state(self):
        """
        Print the internal state of the graph including vertices, edges, and adjacency matrix.
        """
        print("\n--- Graph State ---")
        print(f"Vertices: {self.vertices}")
        print(f"Edges: {self.edges}")
        print(f"Is the graph directed? {'Yes' if self.is_directed else 'No'}")
        print("Adjacency matrix:")
        for row in self.adjacency_matrix:
            print(" ".join(map(str, row)))

    def get_vertex_count(self):
        """
        Returns the total number of vertices in the graph.
        Output: int - number of vertices.
        """
        return len(self.vertices)

    def get_edge_count(self):
        """
        Returns the total number of edges in the graph.
        Output: int - number of edges.
        """
        return len(self.edges)  # For both directed and undirected graphs

    def is_graph_directed(self):
        """
        Returns whether the graph is directed or not.
        Output: bool - True if the graph is directed, False otherwise.
        """
        return self.is_directed

    def get_neighbors(self, vertex):
        """
        Returns the neighbors of the given vertex using the adjacency matrix.
        Input: vertex - the vertex whose neighbors are to be returned.
        Output: list - list of neighboring vertices.
        """
        if vertex not in self.vertices:
            return []
        
        vertex_index = self.vertices.index(vertex)
        neighbors = []
        for idx, is_edge in enumerate(self.adjacency_matrix[vertex_index]):
            if is_edge:
                neighbors.append(self.vertices[idx])
        return neighbors


# Automatically print information about the graph
def print_graph_info():
    graph = Graph()
    graph.read_graph_from_file()  # Read the graph from 'graph.txt'
    
    # Print the graph information
    print("\n--- Graph Information ---")
    print(f"Number of vertices: {graph.get_vertex_count()}")
    print(f"Number of edges: {graph.get_edge_count()}")
    print(f"Is the graph directed? {'Yes' if graph.is_graph_directed() else 'No'}")
    
    # Print neighbors for each vertex
    for vertex in graph.vertices:
        neighbors = graph.get_neighbors(vertex)
        print(f"Neighbors of {vertex}: {', '.join(neighbors) if neighbors else 'None'}")


if __name__ == "__main__":
    print_graph_info()
