"""Graph implementation module.

Implements SortableDigraph, TraversableDigraph, and DAG classes.
Each class supports directed graph operations, traversal, and topological sorting.
"""

from collections import deque


class SortableDigraph:
    """Base class providing basic graph structure and topological sort"""
    def __init__(self):
        """Initialize the graph with empty adjacency list, node data, and edge weights."""
        self.adj = {}  # adjacency list: {node: [neighbors]}
        self.node_data = {}  # store node data: {node: data}
        self.edge_weights = {}  # store edge weights: {(u, v): weight}

    def add_node(self, node, data=None):
        """Add a node to the graph if it doesn't already exist."""
        if node not in self.adj:
            self.adj[node] = []
            self.node_data[node] = data

    def add_edge(self, u, v, edge_weight=None):
        """Add an edge from node u to node v with an optional weight."""
        self.add_node(u)
        self.add_node(v)
        self.adj[u].append(v)
        if edge_weight is not None:
            self.edge_weights[(u, v)] = edge_weight

    def get_node_value(self, node):
        """Get the data associated with a node."""
        return self.node_data.get(node)

    def get_edge_weight(self, u, v):
        """Get the weight of an edge from u to v."""
        return self.edge_weights.get((u, v))

    def topsort(self):
        """Perform topological sort using Depth First Search."""
        visited = set()
        result = []

        def visit(node):
            """Recursive helper function for topological sort."""
            if node in visited:
                return
            visited.add(node)
            for neighbor in self.adj.get(node, []):
                visit(neighbor)
            result.append(node)

        for node in list(self.adj.keys()):
            visit(node)

        return result[::-1]

    def top_sort(self):
        """Alias for topsort to match test requirements."""
        return self.topsort()

    def successors(self, node):
        """Get all successors (outgoing neighbors) of a node."""
        return self.adj.get(node, []).copy()

    def predecessors(self, node):
        """Get all predecessors (incoming neighbors) of a node."""
        preds = []
        for u, neighbors in self.adj.items():
            if node in neighbors:
                preds.append(u)
        return preds

    def get_nodes(self):
        """Get all nodes in the graph."""
        return list(self.adj.keys())


class TraversableDigraph(SortableDigraph):
    """A directed graph with traversal methods (BFS and DFS)."""

    def bfs(self, start):
        """Perform breadth-first search traversal starting from 'start'."""
        visited = set()
        queue = deque([start])
        result = []

        # The test case expects the start node to be excluded from the result,
        # so we add it to visited but don't append to result initially.
        visited.add(start)

        while queue:
            node = queue.popleft()
            for neighbor in self.successors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    result.append(neighbor)
                    queue.append(neighbor)
        return result

    def dfs(self, start):
        """Perform depth-first search traversal starting from 'start'."""
        visited = set()
        result = []

        def dfs_visit(node):
            """Recursive helper function for DFS traversal."""
            # The test case expects the start node to be excluded from the result,
            # so we add it to visited in the initial call but don't append.
            # Subsequent visited nodes are appended.
            for neighbor in self.successors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    result.append(neighbor)
                    dfs_visit(neighbor)

        # Add the start node to visited before the initial recursive call
        visited.add(start)
        dfs_visit(start)
        return result


class DAG(TraversableDigraph):
    """Directed Acyclic Graph (DAG) with topological sorting and cycle detection."""

    def add_edge(self, u, v, edge_weight=None):
        """Add an edge from u to v, raising ValueError if it creates a cycle."""
        # Check if adding edge would create a cycle before adding
        if self._has_path(v, u):
            raise ValueError(f"Adding edge ({u} -> {v}) would create a cycle")

        # Add the edge if safe
        super().add_edge(u, v, edge_weight)

    def _has_path(self, start, end, visited=None):
        """Check if a path exists from 'start' to 'end' using DFS."""
        if visited is None:
            visited = set()

        if start == end:
            return True

        visited.add(start)

        for neighbor in self.adj.get(start, []):
            if neighbor not in visited:
                if self._has_path(neighbor, end, visited):
                    return True

        return False


# Test code
if __name__ == "__main__":
    print("=== Testing TraversableDigraph ===")
    g = TraversableDigraph()
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "D")

    print("DFS:", list(g.dfs("A")))
    print("BFS:", list(g.bfs("A")))

    print("\n=== Testing DAG ===")
    dag = DAG()
    dag.add_edge("shirt", "tie")
    dag.add_edge("shirt", "belt")
    dag.add_edge("tie", "jacket")
    dag.add_edge("belt", "jacket")
    dag.add_edge("pants", "shoes")
    dag.add_edge("pants", "belt")
    dag.add_edge("socks", "shoes")

    print("Topological sort:", dag.topsort())

    try:
        dag.add_edge("jacket", "shirt")
        print("Error: Should have detected cycle!")
    except ValueError as e:
        print("Correctly detected cycle:", e)
