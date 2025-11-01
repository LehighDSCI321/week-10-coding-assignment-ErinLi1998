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


# ----------------------------------------------------------------
# SortableDigraph (already provided by you)
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


# ----------------------------------------------------------------
# TraversableDigraph: adds DFS and BFS traversals
# ----------------------------------------------------------------
class TraversableDigraph(SortableDigraph):
    """Directed graph with DFS and BFS traversal methods."""

    def dfs(self, start, visited=None):
        """Perform a depth-first traversal starting from 'start'."""
        if visited is None:
            visited = set()
        visited.add(start)
        yield start
        for neighbor in self.edges.get(start, []):
            if neighbor not in visited:
                yield from self.dfs(neighbor, visited)

    def bfs(self, start):
        """Perform a breadth-first traversal starting from 'start'."""
        visited = set()
        queue = deque([start])
        visited.add(start)

        while queue:
            v = queue.popleft()
            yield v
            for neighbor in self.edges.get(v, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)


# ----------------------------------------------------------------
# DAG: prevents cycles when adding edges
# ----------------------------------------------------------------
class DAG(TraversableDigraph):
    """Directed Acyclic Graph (DAG) that prevents cycles."""

    def add_edge(self, src, dest):
        """Add edge only if it won't create a cycle."""
        # Ensure both nodes exist
        if src not in self.nodes:
            self.add_node(src)
        if dest not in self.nodes:
            self.add_node(dest)

        # Temporarily add the edge
        self.edges[src].append(dest)

        # Check for cycle by attempting topological sort
        try:
            self.top_sort()
        except ValueError:
            # Revert addition and raise exception
            self.edges[src].remove(dest)
            raise ValueError(f"Adding edge {src} -> {dest} would create a cycle.")



