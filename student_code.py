from collections import deque

class SortableDigraph:
    """A directed graph that supports topological sorting."""

    def __init__(self):
        """Initialize the graph with empty nodes and edges."""
        self.nodes = {}
        self.edges = {}

    def add_node(self, node):
        """Add a node to the graph if it does not already exist."""
        if node not in self.nodes:
            self.nodes[node] = None
        if node not in self.edges:
            self.edges[node] = set()

    def add_edge(self, start, end):
        """Add a directed edge from start → end."""
        if start not in self.nodes:
            self.add_node(start)
        if end not in self.nodes:
            self.add_node(end)
        if start not in self.edges:
            self.edges[start] = set()
        self.edges[start].add(end)

    def top_sort(self):
        """Return a topologically sorted list of nodes."""
        visited = set()
        stack = []
        temp = set()

        def visit(node):
            if node in temp:
                raise ValueError("Graph contains a cycle.")
            if node not in visited:
                temp.add(node)
                for neighbor in self.edges.get(node, []):
                    visit(neighbor)
                temp.remove(node)
                visited.add(node)
                stack.append(node)

        for node in self.nodes:
            if node not in visited:
                visit(node)
        stack.reverse()
        return stack


class TraversableDigraph(SortableDigraph):
    """A digraph that supports DFS and BFS traversals."""

    def dfs(self, start):
        """Depth-First Search traversal that yields nodes in order."""
        visited = set()

        def visit(node):
            if node not in visited:
                visited.add(node)
                yield node
                for neighbor in self.edges.get(node, []):
                    yield from visit(neighbor)

        if start in self.nodes:
            yield from visit(start)

    def bfs(self, start):
        """Breadth-First Search traversal that yields nodes in order."""
        if start not in self.nodes:
            return
        visited = set([start])
        queue = deque([start])
        while queue:
            node = queue.popleft()
            yield node
            for neighbor in self.edges.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)


class DAG(TraversableDigraph):
    """A Directed Acyclic Graph that prevents cycles."""

    def add_edge(self, start, end):
        """Add an edge if it does not create a cycle."""
        # Ensure nodes exist first
        if start not in self.nodes:
            self.add_node(start)
        if end not in self.nodes:
            self.add_node(end)
        # Check if a path exists from end to start
        if self._path_exists(end, start):
            raise ValueError(f"Adding edge {start} → {end} would create a cycle.")
        # Add edge if safe
        super().add_edge(start, end)

    def _path_exists(self, start, target):
        """Return True if there is a path from start → target."""
        if start == target:
            return True
        visited = set()
        stack = [start]
        while stack:
            node = stack.pop()
            if node == target:
                return True
            if node not in visited:
                visited.add(node)
                stack.extend(self.edges.get(node, []))
        return False



