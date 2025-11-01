from collections import deque

class VersatileDigraph:
    """A versatile directed graph implementation."""

    def __init__(self):
        """Initialize the graph."""
        self.nodes = {}
        self.edges = {}

    def add_node(self, node_id, data=None):
        """Add a node to the graph."""
        if node_id not in self.nodes:
            self.nodes[node_id] = data
            self.edges[node_id] = []

    def add_edge(self, src, dest):
        """Add a directed edge from src to dest."""
        if src not in self.nodes:
            self.add_node(src)
        if dest not in self.nodes:
            self.add_node(dest)
        self.edges[src].append(dest)

    def __str__(self):
        """String representation of the graph."""
        result = []
        for src in self.edges:
            for dest in self.edges[src]:
                result.append(f"{src} -> {dest}")
        return "\n".join(result)


class SortableDigraph(VersatileDigraph):
    """Directed graph that supports topological sorting."""

    def top_sort(self):
        """Return a topologically sorted list of nodes using Kahn's algorithm."""
        in_degree = {u: 0 for u in self.nodes}

        # Compute in-degrees
        for u in self.edges:
            for v in self.edges[u]:
                in_degree[v] += 1

        # Initialize queue with nodes that have zero in-degree
        queue = deque([u for u in self.nodes if in_degree[u] == 0])
        topo_order = []

        while queue:
            u = queue.popleft()
            topo_order.append(u)
            for v in self.edges.get(u, []):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        if len(topo_order) != len(self.nodes):
            raise ValueError("Graph has at least one cycle; cannot topologically sort.")

        return topo_order


class TraversableDigraph(SortableDigraph):
    """Directed graph that supports DFS and BFS traversals."""
    
    def dfs(self, start=None):
        """
        Perform depth-first search traversal of the digraph.
        Yields nodes in DFS order.
        """
        visited = set()
        
        # If no start node specified, use all nodes as potential starting points
        if start is not None:
            nodes_to_visit = [start]
        else:
            nodes_to_visit = list(self.nodes.keys())
        
        for node in nodes_to_visit:
            if node not in visited:
                stack = [node]
                visited.add(node)
                
                while stack:
                    current = stack.pop()
                    yield current
                    
                    # Push neighbors in reverse order to maintain DFS semantics
                    for neighbor in reversed(self.edges.get(current, [])):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            stack.append(neighbor)
    
    def bfs(self, start=None):
        """
        Perform breadth-first search traversal of the digraph.
        Yields nodes in BFS order.
        """
        visited = set()
        
        # If no start node specified, use all nodes as potential starting points
        if start is not None:
            nodes_to_visit = [start]
        else:
            nodes_to_visit = list(self.nodes.keys())
        
        for node in nodes_to_visit:
            if node not in visited:
                queue = deque([node])
                visited.add(node)
                
                while queue:
                    current = queue.popleft()
                    yield current
                    
                    for neighbor in self.edges.get(current, []):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)


class DAG(TraversableDigraph):
    """
    Directed Acyclic Graph that prevents cycles when adding edges.
    """
    
    def add_edge(self, src, dest):
        """
        Add a directed edge from src to dest, ensuring no cycles are created.
        Raises ValueError if adding the edge would create a cycle.
        """
        if src not in self.nodes:
            self.add_node(src)
        if dest not in self.nodes:
            self.add_node(dest)
        
        # Check if adding edge would create a cycle
        if self._would_create_cycle(src, dest):
            raise ValueError(f"Adding edge {src} -> {dest} would create a cycle")
        
        # Add the edge if safe
        self.edges[src].append(dest)
    
    def _would_create_cycle(self, src, dest):
        """
        Check if adding an edge from src to dest would create a cycle.
        Returns True if a path already exists from dest to src.
        """
        # If src and dest are the same, it's definitely a cycle
        if src == dest:
            return True
        
        # Use BFS to check if there's a path from dest to src
        visited = set()
        queue = deque([dest])
        visited.add(dest)
        
        while queue:
            current = queue.popleft()
            if current == src:
                return True
            
            for neighbor in self.edges.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return False


