
import time
from typing import List
from ..model.tsp_model import Solver, Solution, TSPInstance
from ..constructive.nearest_neighbor import ConstructiveSolver

class BranchAndBoundSolver(Solver):
    def __init__(self, instance: TSPInstance, time_limit: int = 300):
        super().__init__(instance)
        self.best_solution = None
        self.upper_bound = float('inf')
        self.time_limit = time_limit
        self.start_time = 0

    def solve(self) -> Solution:
        self.start_time = time.time()
        
        # Initial upper bound
        constructive = ConstructiveSolver(self.instance)
        initial_sol = constructive.solve()
        self.best_solution = initial_sol
        self.upper_bound = initial_sol.cost
        
        start_node = 0
        visited = {start_node}
        path = [start_node]
        
        self._dfs(start_node, visited, 0, path)
        
        return self.best_solution

    def _dfs(self, current_node: int, visited: set, current_cost: int, path: List[int]):
        if time.time() - self.start_time > self.time_limit:
            return

        # Pruning with Lower Bound
        if self._bound(current_node, visited, current_cost) >= self.upper_bound:
            return

        if len(visited) == self.instance.n:
            total_cost = current_cost + self.instance.distance(current_node, path[0])
            if total_cost < self.upper_bound:
                self.upper_bound = total_cost
                self.best_solution = Solution(path[:], total_cost)
            return

        remaining_nodes = []
        for city in range(self.instance.n):
            if city not in visited:
                dist = self.instance.distance(current_node, city)
                remaining_nodes.append((dist, city))
        
        # Sort by distance (heuristic)
        remaining_nodes.sort()
        
        for dist, next_city in remaining_nodes:
             # Basic pruning before recursive call
             if current_cost + dist < self.upper_bound:
                 visited.add(next_city)
                 path.append(next_city)
                 self._dfs(next_city, visited, current_cost + dist, path)
                 path.pop()
                 visited.remove(next_city)

    def _bound(self, current_node: int, visited: set, current_cost: int) -> float:
        """
        Calculate a lower bound for the best tour extending the current path.
        LB = current_cost + MST(unvisited) + min_edge(current -> unvisited) + min_edge(unvisited -> start)
        """
        unvisited = [i for i in range(self.instance.n) if i not in visited]
        
        if not unvisited:
            return current_cost + self.instance.distance(current_node, 0) # 0 is always start_node in this setup
            
        bound = current_cost
        
        # 1. Minimum Spanning Tree of unvisited nodes
        if len(unvisited) > 1:
            bound += self._mst_cost(unvisited)
            
        # 2. Connection from current_node to unvisited
        min_to_unvisited = min(self.instance.distance(current_node, u) for u in unvisited)
        bound += min_to_unvisited
        
        # 3. Connection from unvisited back to start (0)
        min_to_start = min(self.instance.distance(u, 0) for u in unvisited)
        bound += min_to_start
        
        return bound

    def _mst_cost(self, nodes: List[int]) -> int:
        """Calculates the cost of MST for the given set of nodes using Prim's algorithm."""
        if not nodes:
            return 0
        
        cost = 0
        # Map node values to 0..len(nodes)-1 for easier array management if needed, 
        # but here we just use the raw indices and a set for 'seen'.
        
        # Prim's algorithm
        # Start with the first node in the list
        start_v = nodes[0]
        seen = {start_v}
        # Distances from the tree to the remaining nodes
        # We want strict O(V^2) implementation for small sets, which is fine here.
        # Initialize min_dists
        min_dists = {v: self.instance.distance(start_v, v) for v in nodes if v != start_v}
        
        while len(seen) < len(nodes):
            # Find node u in nodes \ seen with smallest min_dist
            u = min(min_dists, key=min_dists.get)
            cost += min_dists[u]
            del min_dists[u]
            seen.add(u)
            
            # Update min_dists
            for v in min_dists:
                d = self.instance.distance(u, v)
                if d < min_dists[v]:
                    min_dists[v] = d
                    
        return cost
if __name__ == "__main__":
    # On importe les classes nécessaires si elles ne sont pas déjà là
    # (Adaptez selon vos imports existants en haut du fichier)
    from src.model.tsp_model import TSPInstance

    # 1. Créer une fausse instance de problème (exemple avec 4 villes)
    # Adaptez les arguments selon ce que TSPInstance attend (ex: nombre de villes, matrice)
    dist_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    instance = TSPInstance(n=4, distance_matrix=dist_matrix) # Vérifiez les arguments init de votre classe

    # 2. Initialiser le solveur
    solver = BranchAndBoundSolver(instance)

    # 3. Lancer la résolution
    solution = solver.solve() # Assurez-vous que la méthode s'appelle bien solve()

    # 4. Afficher le résultat
    print("Le résultat est :", solution)