from typing import Dict
class DependencyResolver:
    def __init__(self, metadata: Dict[str, dict]):
        self.metadata = metadata
        self.graph = self._build_graph()
    def _build_graph(self):
        graph = {}
        for name, meta in self.metadata.items():
            graph[name] = meta.get("dependencies", [])
        return graph
    def resolve_order(self):
        visited, order = set(), []
        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            for dep in self.graph.get(node, []):
                dfs(dep)
            order.append(node)
        for node in self.graph:
            dfs(node)
        return order
    def detect_cycles(self):
        stack, visited, cycles = set(), set(), set()
        def visit(node):
            if node in stack:
                cycles.add(node); return
            if node in visited: return
            stack.add(node)
            for dep in self.graph.get(node, []):
                visit(dep)
            stack.remove(node); visited.add(node)
        for node in self.graph:
            visit(node)
        return cycles
