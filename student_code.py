"""graph implementation module.
Implements VersatileDigraph, TraversableDigraph, and DAG classes.
Each class supports directed graph operations, traversal, and topological sorting.
"""

from collections import deque


class VersatileDigraph:
    """A versatile directed graph with nodes and weighted edges."""

    def __init__(self):
        """Initialize the graph with empty node and edge sets."""
        self.nodes = {}   # {node_id: value}
        self.edges = {}   # {src: {dest: weight}}

    def add_node(self, node_id, value=None):
        """Add a node to the graph if not already present."""
        if node_id not in self.nodes:
            self.nodes[node_id] = value
            self.edges[node_id] = {}

    def add_edge(self, src, dest, edge_weight=1):
        """Add a directed edge from src to dest with an optional weight."""
        if src not in self.nodes:
            self.add_node(src)
        if dest not in self.nodes:
            self.add_node(dest)
        self.edges[src][dest] = edge_weight

    def get_nodes(self):
        """Return a list of all node IDs."""
        return list(self.nodes.keys())

    def get_node_value(self, node_id):
        """Return the stored value for a node."""
        return self.nodes.get(node_id, None)

    def get_edge_weight(self, src, dest):
        """Return the weight of the edge from src to dest."""
        return self.edges.get(src, {}).get(dest, None)

    def successors(self, node_id):
        """Return a list of successors (outgoing neighbors) for a node."""
        return list(self.edges.get(node_id, {}).keys())

    def predecessors(self, node_id):
        """Return a list of predecessors (incoming neighbors) for a node."""
        preds = []
        for src in self.edges:
            if node_id in self.edges[src]:
                preds.append(src)
        return preds

    def __str__(self):
        """Return a human-readable string representation of the graph."""
        result = []
        for src in self.edges:
            for dest in self.edges[src]:
                weight = self.edges[src][dest]
                result.append(f"{src} -> {dest} (weight: {weight})")
        return "\n".join(result)


class TraversableDigraph(VersatileDigraph):
    """A graph that supports DFS and BFS traversals."""
    
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
                    for neighbor in reversed(self.successors(current)):
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
                    
                    for neighbor in self.successors(current):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)


class DAG(TraversableDigraph):
    """Directed Acyclic Graph (DAG) with topological sorting and cycle detection."""

    def __init__(self):
        """Initialize an empty DAG."""
        super().__init__()

    def _detect_cycle(self):
        """Detect if the graph contains a cycle using DFS recursion."""
        visited = set()
        rec_stack = set()

        def dfs(node):
            """Recursive DFS to detect cycles."""
            visited.add(node)
            rec_stack.add(node)
            for neighbor in self.successors(node):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        for node in self.nodes:
            if node not in visited:
                if dfs(node):
                    return True
        return False

    def add_edge(self, src, dest, edge_weight=1):
        """Add an edge and prevent cycles."""
        super().add_edge(src, dest, edge_weight)
        if self._detect_cycle():
            # Remove the edge that caused a cycle
            del self.edges[src][dest]
            raise ValueError("Cycle detected — edge addition aborted.")

    def top_sort(self):
        """Perform topological sorting using Kahn's algorithm."""
        in_degree = {u: 0 for u in self.nodes}

        # Compute in-degree for each node
        for u in self.edges:
            for v in self.edges[u]:
                in_degree[v] += 1

        queue = deque([u for u in self.nodes if in_degree[u] == 0])
        topo_order = []

        while queue:
            u = queue.popleft()
            topo_order.append(u)
            for v in self.edges[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        if len(topo_order) != len(self.nodes):
            raise ValueError("Graph has at least one cycle; cannot topologically sort.")
        
        return topo_order
