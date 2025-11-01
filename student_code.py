from collections import deque

class SortableDigraph:
    """A basic directed graph represented with adjacency lists."""
    def __init__(self):
        self.graph = {}

    def add_vertex(self, v):
        """Add a vertex if it doesn't already exist."""
        if v not in self.graph:
            self.graph[v] = []

    def add_edge(self, start, end):
        """Add an edge from start to end (no cycle check here)."""
        self.add_vertex(start)
        self.add_vertex(end)
        self.graph[start].append(end)

    def vertices(self):
        """Return a list of all vertices."""
        return list(self.graph.keys())

    def neighbors(self, v):
        """Return the list of adjacent vertices for a vertex."""
        return self.graph.get(v, [])

    def __repr__(self):
        """Return a string representation of the graph."""
        return f"{self.graph}"


# ------------------------------------------------------------------
# TraversableDigraph adds DFS and BFS traversal methods
# ------------------------------------------------------------------
class TraversableDigraph(SortableDigraph):
    """A directed graph that supports DFS and BFS traversals."""

    def dfs(self, start):
        """Depth-first traversal generator."""
        visited = set()

        def _dfs(v):
            visited.add(v)
            yield v
            for neighbor in self.neighbors(v):
                if neighbor not in visited:
                    yield from _dfs(neighbor)

        if start in self.graph:
            yield from _dfs(start)

    def bfs(self, start):
        """Breadth-first traversal generator using deque."""
        visited = set()
        queue = deque([start])
        visited.add(start)

        while queue:
            v = queue.popleft()
            yield v
            for neighbor in self.neighbors(v):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)


# ------------------------------------------------------------------
# DAG ensures acyclic graph structure by overriding add_edge
# ------------------------------------------------------------------
class DAG(TraversableDigraph):
    """Directed Acyclic Graph (DAG) that prevents cycles."""

    def add_edge(self, start, end):
        """Add an edge only if it won't create a cycle."""
        self.add_vertex(start)
        self.add_vertex(end)

        # Check for potential cycle (path from end → start)
        if self._has_path(end, start):
            raise ValueError(f"Adding edge {start} -> {end} would create a cycle.")

        self.graph[start].append(end)

    def _has_path(self, start, target):
        """Return True if a path exists from start to target."""
        visited = set()
        stack = [start]
        while stack:
            v = stack.pop()
            if v == target:
                return True
            if v not in visited:
                visited.add(v)
                stack.extend(self.neighbors(v))
        return False




