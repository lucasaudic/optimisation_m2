
import random
from typing import List
from ..model.tsp_model import Solver, Solution, TSPInstance
from ..local_search.two_opt import LocalSearchSolver

class GRASPSolver(Solver):
    def __init__(self, instance: TSPInstance, max_iterations: int = 50, alpha: float = 0.2):
        super().__init__(instance)
        self.max_iterations = max_iterations
        self.alpha = alpha 

    def solve(self) -> Solution:
        best_solution = None
        
        for _ in range(self.max_iterations):
            # Phase 1: Construction (Randomized Greedy)
            tour = self.construct_randomized_greedy()
            cost = self.calculate_cost(tour)
            
            # Phase 2: Local Search
            ls_solver = LocalSearchSolver(self.instance, Solution(tour, cost))
            local_optimum = ls_solver.solve()
            
            if best_solution is None or local_optimum.cost < best_solution.cost:
                best_solution = local_optimum
                
        return best_solution

    def construct_randomized_greedy(self) -> List[int]:
        unvisited = set(range(self.instance.n))
        start_node = random.randint(0, self.instance.n - 1)
        current = start_node
        tour = [current]
        unvisited.remove(current)
        
        while unvisited:
            candidates = list(unvisited)
            costs = [self.instance.distance(current, city) for city in candidates]
            min_cost = min(costs)
            max_cost = max(costs)
            
            threshold = min_cost + self.alpha * (max_cost - min_cost)
            
            rcl = [city for city, cost in zip(candidates, costs) if cost <= threshold]
            
            if not rcl:
                 next_city = min(unvisited, key=lambda city: self.instance.distance(current, city))
            else:
                next_city = random.choice(rcl)
            
            tour.append(next_city)
            unvisited.remove(next_city)
            current = next_city
            
        return tour
