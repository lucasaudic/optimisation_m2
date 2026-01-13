
from typing import List, Tuple

class TSPInstance:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = filepath.split("/")[-1]
        self.n, self.matrix = self._load_instance(filepath)

    def _load_instance(self, filepath: str) -> Tuple[int, List[List[int]]]:
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        try:
            n = int(lines[0])
            matrix = []
            current_row = []
            
            # Combine all remaining lines into a single stream of numbers
            all_numbers = []
            for line in lines[1:]:
                all_numbers.extend(map(int, line.split()))
                
            # validation
            if len(all_numbers) != n * n:
                pass

            # Chunk into rows
            for i in range(n):
                matrix.append(all_numbers[i*n : (i+1)*n])
                
            return n, matrix
        except ValueError:
            print(f"Error parsing {filepath}")
            return 0, []

    def distance(self, i: int, j: int) -> int:
        return self.matrix[i][j]

class Solution:
    def __init__(self, tour: List[int], cost: int):
        self.tour = tour
        self.cost = cost

    def __str__(self):
        return f"Cost: {self.cost}, Tour: {self.tour}"

class Solver:
    def __init__(self, instance: TSPInstance):
        self.instance = instance

    def solve(self) -> Solution:
        raise NotImplementedError

    def calculate_cost(self, tour: List[int]) -> int:
        cost = 0
        for i in range(len(tour)):
            cost += self.instance.distance(tour[i], tour[(i + 1) % len(tour)])
        return cost
