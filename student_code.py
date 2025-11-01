from collections import deque

class SortableDigraph:
    """Basic directed graph with adjacency list representation."""
    def __init__(self):
        self.adj = {}  # {vertex: [list of neighbors]}
    
    def add_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = []
    
    def add_edge(self, start, end):
        """Add a directed edge from start → end"""
        self.add_vertex(start)
        self.add_vertex(end)
        self.adj[start].append(end)
    
    def vertices(self):
        return list(self.adj.keys())
    
    def neighbors(self, v):
        return self.adj.get(v, [])
    
    def __str__(self):
        result = []
        for v in self.adj:
            result.append(f"{v} -> {self.adj[v]}")
        return "\n".join(result)


# ---------------------------------------------------------
# TraversableDigraph: adds DFS and BFS traversals
# ---------------------------------------------------------
class TraversableDigraph(SortableDigraph):
    """Extends SortableDigraph with DFS and BFS traversal methods."""
    
    def dfs(self, start, visited=None):
        """Depth-First Search traversal."""
        if visited is None:
            visited = set()
        visited.add(start)
        yield start
        for neighbor in self.neighbors(start):
            if neighbor not in visited:
                yield from self.dfs(neighbor, visited)
    
    def bfs(self, start):
        """Breadth-First Search traversal using deque and yield."""
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


# ---------------------------------------------------------
# DAG: ensures no cycles are created when adding edges
# ---------------------------------------------------------
class DAG(TraversableDigraph):
    """Directed Acyclic Graph that prevents cycles."""
    
    def add_edge(self, start, end):
        """Add edge only if it does NOT create a cycle."""
        # First ensure both vertices exist
        self.add_vertex(start)
        self.add_vertex(end)
        
        # Check if adding start->end would create a cycle
        if self._path_exists(end, start):
            raise ValueError(f"Adding edge {start} -> {end} would create a cycle.")
        
        # Safe to add
        self.adj[start].append(end)
    
    def _path_exists(self, src, dest):
        """Helper: returns True if there is a path from src → dest."""
        visited = set()
        stack = [src]
        
        while stack:
            v = stack.pop()
            if v == dest:
                return True
            if v not in visited:
                visited.add(v)
                stack.extend(self.neighbors(v))
        return False


