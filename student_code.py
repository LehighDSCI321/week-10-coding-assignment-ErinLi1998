"""Graph implementation module.

Implements SortableDigraph, TraversableDigraph, and DAG classes.
Each class supports directed graph operations, traversal, and topological sorting.
"""
from collections import deque

class SortableDigraph:
    """Base class providing basic graph structure and topological sort"""
    def __init__(self):
        self.adj = {}  # adjacency list
        self.node_data = {}  # store node data
        self.edge_weights = {}  # store edge weights

    def add_node(self, node, data=None):
        """Add a node to the graph"""
        if node not in self.adj:
            self.adj[node] = []
            self.node_data[node] = data

    def add_edge(self, u, v, edge_weight=None):
        """Add an edge from u to v"""
        self.add_node(u)
        self.add_node(v)
        self.adj[u].append(v)
        self.edge_weights[(u, v)] = edge_weight

    def get_node_value(self, node):
        """Get the data associated with a node"""
        return self.node_data.get(node)

    def get_edge_weight(self, u, v):
        """Get the weight of an edge"""
        return self.edge_weights.get((u, v))

    def topsort(self):
        """Topological sort"""
        visited = set()
        result = []

        def visit(node):
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
        """Alias for topsort to match test requirements"""
        return self.topsort()

    def successors(self, node):
        """Get all successors of a node"""
        return self.adj.get(node, []).copy()

    def predecessors(self, node):
        """Get all predecessors of a node"""
        preds = []
        for u, neighbors in self.adj.items():
            if node in neighbors:
                preds.append(u)
        return preds

    def get_nodes(self):
        """Get all nodes in the graph"""
        return list(self.adj.keys())
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

        for node in self.adj:  # Iterate over keys of self.adj
            if node not in visited and dfs_cycle(node):
                return True
        return False

    def add_edge(self, src, dest, edge_weight=1):
        """Add an edge and prevent cycles."""
        super().add_edge(src, dest, edge_weight)
        if self._detect_cycle():
            del self.edge_weights[(src, dest)]  # Correctly delete from edge_weights
            self.adj[src].remove(dest) # Also remove the edge from the adjacency list
            raise ValueError("Cycle detected — edge addition aborted.")

    def top_sort(self):
        """Perform topological sorting using Kahn's algorithm."""
        in_degree = {u: 0 for u in self.adj} # Use self.adj keys for nodes

        # Compute in-degree for each node
        for src, dests in self.adj.items(): # Iterate over self.adj
            for dest in dests:
                in_degree[dest] += 1

        queue = deque([u for u in self.adj if in_degree.get(u, 0) == 0]) # Use self.adj keys for nodes, handle nodes with no incoming edges
        topo_order = []

        while queue:
            u = queue.popleft()
            topo_order.append(u)
            for v in self.adj.get(u, []): # Iterate over neighbors from self.adj
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        if len(topo_order) != len(self.adj): # Compare with number of nodes in self.adj
            raise ValueError(
                "Graph has at least one cycle; cannot topologically sort."
            )

        return topo_order
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

