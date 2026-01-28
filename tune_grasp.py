
import os
import time
import statistics
from src.model.tsp_model import TSPInstance
from src.grasp.grasp_solver import GRASPSolver

def run_experiment():
    instance_path = "instances/new_instances/51.in"
    if not os.path.exists(instance_path):
        print(f"Instance {instance_path} not found.")
        return

    try:
        instance = TSPInstance(instance_path)
    except Exception as e:
        print(f"Error loading {instance_path}: {e}")
        return

    alphas = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    iterations = 50
    num_runs = 5

    results = {}

    print(f"Running tuning on {instance_path} with {iterations} iterations, {num_runs} runs per alpha.")
    print("Alpha | Avg Cost | Best Cost | Avg Time")
    print("-" * 40)

    for alpha in alphas:
        costs = []
        times = []
        for _ in range(num_runs):
            solver = GRASPSolver(instance, max_iterations=iterations, alpha=alpha)
            start_time = time.time()
            solution = solver.solve()
            end_time = time.time()
            
            costs.append(solution.cost)
            times.append(end_time - start_time)
        
        avg_cost = statistics.mean(costs)
        best_cost = min(costs)
        avg_time = statistics.mean(times)
        
        results[alpha] = avg_cost
        print(f"{alpha:5.1f} | {avg_cost:8.2f} | {best_cost:9.2f} | {avg_time:8.4f}s")

    best_alpha = min(results, key=results.get)
    print("\nBest Alpha based on Avg Cost:", best_alpha)

if __name__ == "__main__":
    run_experiment()
