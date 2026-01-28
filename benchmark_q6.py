
import os
import time
import glob
import csv
from src.model.tsp_model import TSPInstance
from src.constructive.nearest_neighbor import ConstructiveSolver
from src.local_search.two_opt import LocalSearchSolver
from src.grasp.grasp_solver import GRASPSolver
from src.exact.branch_and_bound import BranchAndBoundSolver

def run_benchmark_q6():
    # Instances to process
    instance_path = "instances/new_instances/*.in"
    files = glob.glob(instance_path)
    
    if not files:
        print(f"No instances found in {instance_path}")
        return

    # Sort files by size
    files.sort(key=lambda x: os.path.getsize(x))
    
    output_file = "report/benchmark_q6_results.csv"
    os.makedirs("report", exist_ok=True)
    
    fieldnames = ["Instance", "Size", "Exact_Cost", "Exact_Time", 
                  "Constructive_Cost", "Constructive_Time", "Constructive_Gap",
                  "LocalSearch_Cost", "LocalSearch_Time", "LocalSearch_Gap",
                  "GRASP_Cost", "GRASP_Time", "GRASP_Gap"]

    # Write header
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    
    for file in files:
        filename = os.path.basename(file)
        if "benchmark_results" in filename: continue
        
        # Skip very large instances to save time during this interactive session if needed
        # But we try to do as much as possible. 1379 might be too slow for Python 2-opt.
        # Let's peek at size first
        try:
            temp_instance = TSPInstance(file)
            n = temp_instance.n
        except:
            continue
            
        if n > 1000:
            print(f"Skipping {filename} (Size {n}) - too large for quick benchmark")
            continue
            
        print(f"\nProcessing {filename} (Size: {n})...")
        try:
            instance = temp_instance
            
            # 1. Exact (Branch and Bound)
            cost_exact = "N/A"
            time_exact = "N/A"
            optimal = False
            
            if n <= 20:
                print("    Running Exact...")
                start = time.time()
                solver_bb = BranchAndBoundSolver(instance, time_limit=60)
                sol_bb = solver_bb.solve()
                time_exact = time.time() - start
                if sol_bb:
                    cost_exact = sol_bb.cost
                    print(f"      Cost: {cost_exact} (Time: {time_exact:.4f}s)")
                    optimal = True
                else:
                    cost_exact = "Timeout"
                    print("      Timeout")
            else:
                 print(f"    Skipping Exact (N={n})")

            # 2. Constructive (Nearest Neighbor)
            print("    Running Constructive...")
            start_pc = time.perf_counter()
            solver_const = ConstructiveSolver(instance)
            sol_const = solver_const.solve()
            time_const = time.perf_counter() - start_pc
            print(f"      Cost: {sol_const.cost} (Time: {time_const:.6f}s)")
            
            # 3. Local Search (2-Opt)
            print("    Running Local Search...")
            start_pc = time.perf_counter()
            solver_ls = LocalSearchSolver(instance, sol_const)
            sol_ls = solver_ls.solve()
            time_ls = time.perf_counter() - start_pc
            print(f"      Cost: {sol_ls.cost} (Time: {time_ls:.6f}s)")
            
            # 4. GRASP
            print("    Running GRASP...")
            # For large instances, reduce iterations to keep runtime reasonable for demo
            iters = 50
            if n > 500: iters = 20
            
            start_pc = time.perf_counter()
            solver_grasp = GRASPSolver(instance, max_iterations=iters, alpha=0.2)
            sol_grasp = solver_grasp.solve()
            time_grasp = time.perf_counter() - start_pc
            print(f"      Cost: {sol_grasp.cost} (Time: {time_grasp:.6f}s)")
            
            # Calculate gaps
            gap_const = ""
            gap_ls = ""
            gap_grasp = ""
            
            if optimal and isinstance(cost_exact, (int, float)):
                gap_const = (sol_const.cost - cost_exact) / cost_exact * 100
                gap_ls = (sol_ls.cost - cost_exact) / cost_exact * 100
                gap_grasp = (sol_grasp.cost - cost_exact) / cost_exact * 100

            row = {
                "Instance": filename,
                "Size": n,
                "Exact_Cost": cost_exact,
                "Exact_Time": time_exact,
                "Constructive_Cost": sol_const.cost,
                "Constructive_Time": time_const,
                "Constructive_Gap": gap_const,
                "LocalSearch_Cost": sol_ls.cost,
                "LocalSearch_Time": time_ls,
                "LocalSearch_Gap": gap_ls,
                "GRASP_Cost": sol_grasp.cost,
                "GRASP_Time": time_grasp,
                "GRASP_Gap": gap_grasp
            }
            
            with open(output_file, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(row)
            
        except Exception as e:
            print(f"  Error processing {file}: {e}")

    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    run_benchmark_q6()
