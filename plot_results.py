
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def plot_benchmark_results():
    results_file = "report/benchmark_q6_results.csv"
    if not os.path.exists(results_file):
        print(f"Error: {results_file} not found. Run benchmark_q6.py first.")
        return

    df = pd.read_csv(results_file)
    df = df.sort_values(by="Size")

    # 1. Plot Time vs Size (Log Scale for Time)
    plt.figure(figsize=(12, 6))
    
    # Filter out N/A or Timeout for plotting
    plt.plot(df["Size"], df["Constructive_Time"], marker='o', label="Constructive (NN)")
    plt.plot(df["Size"], df["LocalSearch_Time"], marker='s', label="Local Search (2-Opt)")
    plt.plot(df["Size"], df["GRASP_Time"], marker='^', label="GRASP")
    
    # Handle Exact times - might be sparse
    exact_data = df[pd.to_numeric(df["Exact_Time"], errors='coerce').notnull()]
    if not exact_data.empty:
        plt.plot(exact_data["Size"], exact_data["Exact_Time"], marker='x', label="Exact (B&B)", linestyle='--')

    plt.yscale("log")
    plt.xlabel("Number of Cities (n)")
    plt.ylabel("Execution Time (s) [Log Scale]")
    plt.title("Execution Time vs Instance Size")
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    
    output_path = "report/plot_time_complexity.png"
    plt.savefig(output_path)
    print(f"Time plot saved to {output_path}")
    plt.close()

    # 2. Plot Solution Quality (Cost) vs Size
    plt.figure(figsize=(12, 6))
    
    plt.plot(df["Size"], df["Constructive_Cost"], marker='o', label="Constructive (NN)")
    plt.plot(df["Size"], df["LocalSearch_Cost"], marker='s', label="Local Search (2-Opt)")
    plt.plot(df["Size"], df["GRASP_Cost"], marker='^', label="GRASP")
    
    # Exact costs
    exact_costs = df[pd.to_numeric(df["Exact_Cost"], errors='coerce').notnull()]
    if not exact_costs.empty:
         plt.plot(exact_costs["Size"], exact_costs["Exact_Cost"], marker='x', label="Exact (Optimal)", linestyle='--', color='black')

    plt.xlabel("Number of Cities (n)")
    plt.ylabel("Tour Cost")
    plt.title("Solution Cost vs Instance Size")
    plt.legend()
    plt.grid(True)
    
    output_path = "report/plot_quality.png"
    plt.savefig(output_path)
    print(f"Quality plot saved to {output_path}")
    plt.close()
    
    # 3. Gap Analysis (if Exact available)
    if not exact_costs.empty:
        plt.figure(figsize=(12, 6))
        # Need to re-calculate gaps here or use CSV columns if they are numeric
        # The CSV might have "N/A", so let's be careful
        
        # Use only rows where Exact is available
        df_gap = df[pd.to_numeric(df["Exact_Cost"], errors='coerce').notnull()].copy()
        
        if not df_gap.empty:
            plt.plot(df_gap["Size"], df_gap["Constructive_Gap"], marker='o', label="Constructive Gap %")
            plt.plot(df_gap["Size"], df_gap["LocalSearch_Gap"], marker='s', label="Local Search Gap %")
            plt.plot(df_gap["Size"], df_gap["GRASP_Gap"], marker='^', label="GRASP Gap %")
            
            plt.xlabel("Number of Cities (n)")
            plt.ylabel("Gap directly to Optimal (%)")
            plt.title("Optimality Gap for Small Instances")
            plt.legend()
            plt.grid(True)
            
            output_path = "report/plot_gap.png"
            plt.savefig(output_path)
            print(f"Gap plot saved to {output_path}")
            plt.close()

if __name__ == "__main__":
    plot_benchmark_results()
