
import sys
import os
import argparse
from src.model.tsp_model import TSPInstance
from src.exact.branch_and_bound import BranchAndBoundSolver
# from src.metaheuristics.grasp import GraspSolver # TODO: Add other solvers as needed
# from src.constructive.nearest_neighbor import ConstructiveSolver
from src.grasp.grasp_solver import GRASPSolver
from src.constructive.nearest_neighbor import ConstructiveSolver
from src.local_search.two_opt import LocalSearchSolver

def main():
    if len(sys.argv) < 3:
        print("Usage: python solve.py <instance_file> <method>")
        sys.exit(1)

    instance_file = sys.argv[1]
    method = sys.argv[2]

    if not os.path.exists(instance_file):
        print(f"Error: File '{instance_file}' not found.")
        sys.exit(1)

    try:
        instance = TSPInstance(instance_file)
    except Exception as e:
        print(f"Error loading instance: {e}")
        sys.exit(1)

    solver = None
    if method == "exact":
        solver = BranchAndBoundSolver(instance)
    elif method == "constructive":
        solver = ConstructiveSolver(instance)
    elif method == "local_search":
        solver = LocalSearchSolver(instance)
<<<<<<< HEAD
    # elif method == "grasp":
    #     solver = GraspSolver(instance)
=======
    elif method == "grasp":
        solver = GRASPSolver(instance)
>>>>>>> 51d6dab (Ajout du projet et fichiers principaux)
    else:
        print(f"Unknown method: {method}")
        sys.exit(1)

    print(f"Solving {instance.filename} with {method}...")
    solution = solver.solve()
    print("Done.")

    # Output file generation
    base_name = os.path.splitext(os.path.basename(instance_file))[0]
    output_filename = f"{base_name}_{method}.out"
    
    with open(output_filename, 'w') as f:
        # Line 1: Vertex numbers separated by space (1-based index usually for TSP provided solutions, 
        # but the request says "numbers of vertices... representing order". 
        # The input file uses index implicitly 0..N-1. But often output expects 0..N-1 or 1..N.
        # Let's check the example in the prompt description carefully.
        # The prompt says: "La première ligne contient les numéros des sommets séparés par un espace".
        # It doesn't specify 0-based or 1-based. 
        # Looking at valid TSP formats (TSPLIB), usually 1-based.
        # However, looking at the input file `17.in`, the first line is N=17. 
        # Let's stick to 0-based for now as it matches Python indices, or 1-based if standard. 
        # "2. 0 633..." -> typical distance matrix. 
        # I will assume 0-indexed as per `tsp_model.py` implementation.
        f.write(" ".join(map(str, solution.tour)) + "\n")
        f.write(str(solution.cost) + "\n")

    print(f"Solution written to {output_filename}")
    print(f"Tour: {solution.tour}")
    print(f"Cost: {solution.cost}")

if __name__ == "__main__":
    main()
