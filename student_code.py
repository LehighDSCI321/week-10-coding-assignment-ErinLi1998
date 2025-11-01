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
        """Return a readable string representation of the graph."""
        output = []
        for src in sorted(self.edges.keys()):
            if not self.edges[src]:
                output.append(f"{src} -> []")
            else:
                output.append(f"{src} -> {sorted(self.edges[src])}")
        return "\n".join(output)

    def __repr__(self):
        """Return the internal dictionary representation."""
        return str(self.edges)


# ----------------------------------------------------------------
# SortableDigraph: adds topological sorting
# ----------------------------------------------------------------
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
        queue = deque(sorted([u for u in self.nodes if in_degree[u] == 0]))
        topo_order = []

        while queue:
            u = queue.popleft()
            topo_order.append(u)
            for v in sorted(self.edges.get(u, [])):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        if len(topo_order) != len(self.nodes):
            raise ValueError("Graph has at least one cycle; cannot topologically sort.")

        return topo_order


# ----------------------------------------------------------------
# TraversableDigraph: adds DFS and BFS traversals
# ----------------------------------------------------------------
class TraversableDigraph(SortableDigraph):
    """Directed graph with DFS and BFS traversal methods."""

    def dfs(self, start):
        """Perform a depth-first search traversal and return a list of visited nodes."""
        visited = set()
        order = []

        def _dfs(node):
            visited.add(node)
            order.append(node)
            for neighbor in sorted(self.edges.get(node, [])):
                if neighbor not in visited:
                    _dfs(neighbor)

        if start in self.nodes:
            _dfs(start)
        return order

    def bfs(self, start):
        """Perform a breadth-first search traversal and return a list of visited nodes."""
        if start not in self.nodes:
            return []

        visited = set([start])
        order = []
        queue = deque([start])

        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in sorted(self.edges.get(node, [])):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order


# ----------------------------------------------------------------
# DAG: prevents cycles when adding edges
# ----------------------------------------------------------------
class DAG(TraversableDigraph):
    """Directed Acyclic Graph that prevents cycles."""

    def add_edge(self, src, dest):
        """Add edge only if it won't create a cycle."""
        if src not in self.nodes:
            self.add_node(src)
        if dest not in self.nodes:
            self.add_node(dest)

        self.edges[src].append(dest)

        # Check for cycle using topological sort
        try:
            self.top_sort()
        except ValueError:
            self.edges[src].remove(dest)
            raise ValueError(f"Adding edge {src} -> {dest} would create a cycle.")


