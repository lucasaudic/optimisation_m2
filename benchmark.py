
import os
import time
import glob
import pandas as pd
from src.model.tsp_model import TSPInstance
from src.constructive.nearest_neighbor import ConstructiveSolver
from src.local_search.two_opt import LocalSearchSolver
from src.grasp.grasp_solver import GRASPSolver
from src.exact.branch_and_bound import BranchAndBoundSolver

def run_benchmark():
    # Look for instances in the new_instances folder
    instance_path = "instances/new_instances/*.in"
    files = glob.glob(instance_path)
    
    if not files:
        print(f"No instances found in {instance_path}")
        return

    files.sort(key=lambda x: os.path.getsize(x))
    
    results = []
    
    for file in files:
        filename = os.path.basename(file)
        if filename == "benchmark_results.csv": continue
        
        print(f"\nProcessing {filename}...")
        try:
            instance = TSPInstance(file)
            n = instance.n
            print(f"  Size: {n}")
            
            # 1. Constructive
            start = time.time()
            solver_const = ConstructiveSolver(instance)
            sol_const = solver_const.solve()
            time_const = time.time() - start
            print(f"    Constructive: {sol_const.cost} (Time: {time_const:.4f}s)")
            
            # 2. Local Search
            start = time.time()
            solver_ls = LocalSearchSolver(instance, sol_const)
            sol_ls = solver_ls.solve()
            time_ls = time.time() - start
            print(f"    Local Search: {sol_ls.cost} (Time: {time_ls:.4f}s)")
            
            # 3. GRASP
            start = time.time()
            solver_grasp = GRASPSolver(instance, max_iterations=20)
            sol_grasp = solver_grasp.solve()
            time_grasp = time.time() - start
            print(f"    GRASP: {sol_grasp.cost} (Time: {time_grasp:.4f}s)")
            
            # 4. Exact (Branch and Bound)
            sol_exact_cost = "N/A"
            time_exact = "N/A"
            if n <= 20: 
                start = time.time()
                solver_bb = BranchAndBoundSolver(instance, time_limit=60)
                sol_bb = solver_bb.solve()
                time_exact = time.time() - start
                if sol_bb:
                    sol_exact_cost = sol_bb.cost
                    print(f"    Exact: {sol_exact_cost} (Time: {time_exact:.4f}s)")
                else:
                    sol_exact_cost = "Timeout/NoSol"
                    print(f"    Exact: Timeout")
            else:
                 print(f"    Exact: Skipped (N={n} too large)")
            
            results.append({
                "Instance": filename,
                "Size": n,
                "Constructive_Cost": sol_const.cost,
                "Constructive_Time": time_const,
                "LocalSearch_Cost": sol_ls.cost,
                "LocalSearch_Time": time_ls,
                "GRASP_Cost": sol_grasp.cost,
                "GRASP_Time": time_grasp,
                "Exact_Cost": sol_exact_cost,
                "Exact_Time": time_exact
            })
            
        except Exception as e:
            print(f"  Error processing {file}: {e}")
            
    if results:
        df = pd.DataFrame(results)
        df.to_csv("report/benchmark_results.csv", index=False)
        print("\nResults saved to report/benchmark_results.csv")
        print(df.to_markdown())

if __name__ == "__main__":
    run_benchmark()
