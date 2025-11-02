"""Graph classes implementing traversable digraph and DAG with cycle detection."""

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
    """Extends SortableDigraph with traversal methods"""
    def dfs(self, start):
        """Depth-First Search traversal starting from a node"""
        visited = set()
        order = []

        def visit(node):
            if node in visited:
                return
            visited.add(node)
            order.append(node)
            for neighbor in self.adj.get(node, []):
                visit(neighbor)

        visit(start)
        return order

    def bfs(self, start):
        """Breadth-First Search traversal starting from a node"""
        visited = set()
        queue = deque([start])
        order = []

        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                order.append(node)
                for neighbor in self.adj.get(node, []):
                    queue.append(neighbor)

        return order


class DAG(TraversableDigraph):
    """Directed Acyclic Graph with cycle detection"""
    def add_edge(self, u, v, edge_weight=None):
        """Add an edge only if it does not create a cycle"""
        super().add_edge(u, v, edge_weight)
        if self._has_cycle():
            # Remove the edge if cycle is detected
            self.adj[u].remove(v)
            del self.edge_weights[(u, v)]
            raise ValueError(f"Adding edge {u}->{v} creates a cycle")

    def _has_cycle(self):
        """Detect if a cycle exists in the graph"""
        visited = set()
        stack = set()

        def visit(node):
            if node in stack:
                return True
            if node in visited:
                return False
            visited.add(node)
            stack.add(node)
            for neighbor in self.adj.get(node, []):
                if visit(neighbor):
                    return True
            stack.remove(node)
            return False

        return any(visit(node) for node in self.adj)

