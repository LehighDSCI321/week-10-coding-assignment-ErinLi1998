from collections import deque

class SortableDigraph:
    """A directed graph that supports topological sorting."""

    def __init__(self):
        self.nodes = set()
        self.edges = {}

    def add_node(self, node):
        """Add a node to the graph."""
        self.nodes.add(node)
        if node not in self.edges:
            self.edges[node] = set()

    def add_edge(self, start, end):
        """Add a directed edge from start → end."""
        if start not in self.nodes:
            self.add_node(start)
        if end not in self.nodes:
            self.add_node(end)
        self.edges[start].add(end)

    def top_sort(self):
        """Return a topologically sorted list of nodes."""
        visited = set()
        stack = []
        temp_mark = set()

        def visit(node):
            if node in temp_mark:
                raise ValueError("Graph is not a DAG (cycle detected).")
            if node not in visited:
                temp_mark.add(node)
                for neighbor in self.edges.get(node, []):
                    visit(neighbor)
                temp_mark.remove(node)
                visited.add(node)
                stack.append(node)

        for node in self.nodes:
            if node not in visited:
                visit(node)

        stack.reverse()
        return stack


class TraversableDigraph(SortableDigraph):
    """A digraph that supports DFS and BFS traversals."""

    def dfs(self, start, visited=None):
        """Depth-First Search traversal (recursive, yields nodes)."""
        if visited is None:
            visited = set()
        visited.add(start)
        yield start
        for neighbor in self.edges.get(start, []):
            if neighbor not in visited:
                yield from self.dfs(neighbor, visited)

    def bfs(self, start):
        """Breadth-First Search traversal (using deque, yields nodes)."""
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
        """Add an edge if it doesn't create a cycle."""
        # Check if adding start→end would create a cycle
        if self._path_exists(end, start):
            raise ValueError(f"Adding edge {start} → {end} would create a cycle.")
        super().add_edge(start, end)

    def _path_exists(self, start, target, visited=None):
        """Helper method to detect if a path exists from start to target."""
        if visited is None:
            visited = set()
        if start == target:
            return True
        visited.add(start)
        for neighbor in self.edges.get(start, []):
            if neighbor not in visited and self._path_exists(neighbor, target, visited):
                return True
        return False



