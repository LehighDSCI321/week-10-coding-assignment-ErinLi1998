"""Graph implementation module.

Implements SortableDigraph, TraversableDigraph, and DAG classes.
Each class supports directed graph operations, traversal, and topological sorting.
"""

from collections import deque


class SortableDigraph:
    """A versatile directed graph with nodes and weighted edges."""

    def __init__(self):
        """Initialize the graph with empty node and edge sets."""
        self.nodes = {}  # {node_id: value}
        self.edges = {}  # {src: {dest: weight}}

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
        return self.nodes.get(node_id)

    def get_edge_weight(self, src, dest):
        """Return the weight of the edge from src to dest."""
        return self.edges.get(src, {}).get(dest)

    def successors(self, node_id):
        """Return a list of successors (outgoing neighbors) for a node."""
        return list(self.edges.get(node_id, {}).keys())

    def predecessors(self, node_id):
        """Return a list of predecessors (incoming neighbors) for a node."""
        return [src for src in self.edges if node_id in self.edges[src]]

    def __str__(self):
        """Return a human-readable string representation of the graph."""
        result = []
        for src, dests in self.edges.items():
            for dest, weight in dests.items():
                result.append(f"{src} -> {dest} ({weight})")
        return "\n".join(result)

    def top_sort(self):
        """Return a topologically sorted list of nodes using Kahn's algorithm."""
        in_degree = {u: 0 for u in self.nodes}

        # Compute in-degrees
        for u in self.edges:
            for v in self.edges[u]:
                in_degree[v] += 1

        # Initialize queue with zero in-degree nodes
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
            raise ValueError(
                "Graph has at least one cycle; cannot topologically sort."
            )

        return topo_order


class TraversableDigraph(SortableDigraph):
    """A directed graph with traversal methods (BFS and DFS)."""

    def bfs(self, start):
        """Perform breadth-first search (excluding the start node)."""
        visited = set()
        queue = deque([start])
        result = []

        while queue:
            node = queue.popleft()
            for neighbor in self.successors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    result.append(neighbor)
                    queue.append(neighbor)
        return result

    def dfs(self, start):
        """Perform depth-first search (excluding the start node)."""
        visited = set()
        result = []

        def dfs_visit(node):
            """Recursive helper function for DFS traversal."""
            for neighbor in self.successors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    result.append(neighbor)
                    dfs_visit(neighbor)

        dfs_visit(start)
        return result


class DAG(TraversableDigraph):
    """Directed Acyclic Graph (DAG) with topological sorting and cycle detection."""

    def __init__(self):
        """Initialize an empty DAG."""
        super().__init__()

    def _detect_cycle(self):
        """Detect if the graph contains a cycle using DFS recursion."""
        visited = set()
        rec_stack = set()

        def dfs_cycle(node):
            """Recursive DFS to detect cycles."""
            visited.add(node)
            rec_stack.add(node)
            for neighbor in self.successors(node):
                if neighbor not in visited and dfs_cycle(neighbor):
                    return True
                if neighbor in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        for node in self.nodes:
            if node not in visited and dfs_cycle(node):
                return True
        return False

    def add_edge(self, src, dest, edge_weight=1):
        """Add an edge and prevent cycles."""
        super().add_edge(src, dest, edge_weight)
        if self._detect_cycle():
            del self.edges[src][dest]
            raise ValueError("Cycle detected — edge addition aborted.")

    def top_sort(self):
        """Perform topological sorting using Kahn's algorithm."""
        in_degree = {u: 0 for u in self.nodes}

        # Compute in-degree for each node
        for src, dests in self.edges.items():
            for dest in dests:
                in_degree[dest] += 1

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
            raise ValueError(
                "Graph has at least one cycle; cannot topologically sort."
            )

        return topo_order

