
import os
import time
import glob
import csv
from src.model.tsp_model import TSPInstance
from src.constructive.nearest_neighbor import ConstructiveSolver
from src.local_search.two_opt import LocalSearchSolver
from src.grasp.grasp_solver import GRASPSolver
from src.exact.branch_and_bound import BranchAndBoundSolver

def run_benchmark_q7():
    # Target files in the ROOT directory (excluding subdirectories)
    # We look for .in files in the current folder
    files = glob.glob("*.in")
    
    if not files:
        print(f"No instances found in current directory")
        return

    # Sort files by size
    files.sort(key=lambda x: os.path.getsize(x))
    
    print(f"Found {len(files)} instances for validation (Q7).")
    
    output_file = "report/benchmark_q7_results.csv"
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
        
        try:
            temp_instance = TSPInstance(file)
            n = temp_instance.n
        except Exception as e:
            print(f"Skipping {filename}: {e}")
            continue
            
        if n > 1000:
            print(f"Skipping {filename} (Size {n}) - too large for validation")
            continue
            
        print(f"\nProcessing {filename} (Size: {n})...")
        try:
            instance = temp_instance
            
            # Exact
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
                    optimal = True
                else: 
                    cost_exact = "Timeout"

            # Constructive
            print("    Running Constructive...")
            start_pc = time.perf_counter()
            sol_const = ConstructiveSolver(instance).solve()
            time_const = time.perf_counter() - start_pc

            # Local Search
            print("    Running Local Search...")
            start_pc = time.perf_counter()
            sol_ls = LocalSearchSolver(instance, sol_const).solve()
            time_ls = time.perf_counter() - start_pc

            # GRASP (OPTIMIZED CONFIGURATION)
            # Assuming alpha=0.2 and 50 iterations were found best in Q6
            best_alpha = 0.2
            best_iter = 50
            if n > 500: best_iter = 20 # Adjustment for large instances
            
            print(f"    Running GRASP (alpha={best_alpha}, iter={best_iter})...")
            start_pc = time.perf_counter()
            sol_grasp = GRASPSolver(instance, max_iterations=best_iter, alpha=best_alpha).solve()
            time_grasp = time.perf_counter() - start_pc

            # Gaps
            gap_const = (sol_const.cost - cost_exact)/cost_exact*100 if (optimal and isinstance(cost_exact, (int, float))) else ""
            gap_ls = (sol_ls.cost - cost_exact)/cost_exact*100 if (optimal and isinstance(cost_exact, (int, float))) else ""
            # Calculate gap against BEST KNOWN if Exact not available? 
            # For now, stick to Exact comparison or just raw verification.
            gap_grasp = (sol_grasp.cost - cost_exact)/cost_exact*100 if (optimal and isinstance(cost_exact, (int, float))) else ""

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
                
            print(f"    -> GRASP Cost: {sol_grasp.cost} (Time: {time_grasp:.4f}s)")
            
        except Exception as e:
            print(f"  Error processing {file}: {e}")

    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    run_benchmark_q7()
