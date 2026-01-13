
from ..model.tsp_model import Solver, Solution, TSPInstance

class ConstructiveSolver(Solver):
    def solve(self, start_node: int = 0) -> Solution:
        # Nearest Neighbor Heuristic
        unvisited = set(range(self.instance.n))
        current = start_node
        tour = [current]
        unvisited.remove(current)
        
        while unvisited:
            next_city = min(unvisited, key=lambda city: self.instance.distance(current, city))
            tour.append(next_city)
            unvisited.remove(next_city)
            current = next_city
            
        cost = self.calculate_cost(tour)
        return Solution(tour, cost)
