
from typing import List, Optional
from ..model.tsp_model import Solver, Solution, TSPInstance
from ..constructive.nearest_neighbor import ConstructiveSolver

class LocalSearchSolver(Solver):
    def __init__(self, instance: TSPInstance, initial_solution: Optional[Solution] = None):
        super().__init__(instance)
        self.initial_solution = initial_solution

    def solve(self) -> Solution:
        if self.initial_solution:
            current_tour = self.initial_solution.tour[:]
            current_cost = self.initial_solution.cost
        else:
            # Generate a random or simple constructive solution first if none provided
            constructive = ConstructiveSolver(self.instance)
            sol = constructive.solve()
            current_tour = sol.tour
            current_cost = sol.cost
            
        return self.two_opt(current_tour, current_cost)

    def two_opt(self, tour: List[int], cost: int) -> Solution:
        improved = True
        best_tour = tour[:]
        best_cost = cost
        n = len(tour)
        
        while improved:
            improved = False
            for i in range(1, n - 1):
                for j in range(i + 1, n):
                    if j - i == 1: continue # No change for adjacent edges
                    
                    u1, v1 = best_tour[i-1], best_tour[i]
                    u2, v2 = best_tour[j], best_tour[(j+1)%n]
                    
                    current_delta = self.instance.distance(u1, v1) + self.instance.distance(u2, v2)
                    new_delta = self.instance.distance(u1, u2) + self.instance.distance(v1, v2)
                    
                    if new_delta < current_delta:
                        # Perform swap
                        best_tour[i:j+1] = reversed(best_tour[i:j+1])
                        best_cost -= (current_delta - new_delta)
                        improved = True
        
        return Solution(best_tour, best_cost)
