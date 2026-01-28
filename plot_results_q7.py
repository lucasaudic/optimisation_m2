
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def plot_benchmark_results_q7():
    results_file = "report/benchmark_q7_results.csv"
    if not os.path.exists(results_file):
        print(f"Error: {results_file} not found. Run benchmark_q7.py first.")
        return

    df = pd.read_csv(results_file)
    df = df.sort_values(by="Size")

    # 1. Validation: Time vs Size
    plt.figure(figsize=(10, 6))
    plt.plot(df["Size"], df["GRASP_Time"], marker='^', color='green', label="GRASP (Validation)")
    plt.plot(df["Size"], df["LocalSearch_Time"], marker='s', color='blue', label="Local Search (Validation)")
    
    plt.yscale("log")
    plt.xlabel("Instance Size (n)")
    plt.ylabel("Time (s) [Log Scale]")
    plt.title("Validation: Scalability of Optimized GRASP")
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    plt.savefig("report/q7_validation_time.png")
    print("Saved report/q7_validation_time.png")
    plt.close()

    # 2. Validation: Quality (Cost)
    plt.figure(figsize=(10, 6))
    plt.plot(df["Size"], df["GRASP_Cost"], marker='^', color='green', label="GRASP Cost")
    plt.plot(df["Size"], df["LocalSearch_Cost"], marker='s', color='blue', label="Local Search Cost")
    
    plt.xlabel("Instance Size (n)")
    plt.ylabel("Cost")
    plt.title("Validation: Solution Quality")
    plt.legend()
    plt.grid(True)
    plt.savefig("report/q7_validation_quality.png")
    print("Saved report/q7_validation_quality.png")
    plt.close()
    
    # 3. Bar Chart for Gap comparison on key instances
    # Select a few representative instances if available
    subset = df[df["Size"] <= 200]
    if not subset.empty:
        plt.figure(figsize=(12, 6))
        # Comparison of Cost Improvement over Constructive
        # (Constructive - Method) / Constructive * 100
        grasp_imp = (subset["Constructive_Cost"] - subset["GRASP_Cost"]) / subset["Constructive_Cost"] * 100
        ls_imp = (subset["Constructive_Cost"] - subset["LocalSearch_Cost"]) / subset["Constructive_Cost"] * 100
        
        indices = range(len(subset))
        width = 0.35
        
        plt.bar([i - width/2 for i in indices], ls_imp, width, label='Local Search Improv.')
        plt.bar([i + width/2 for i in indices], grasp_imp, width, label='GRASP Improv.')
        
        plt.xlabel('Instance')
        plt.ylabel('Improvement over NN (%)')
        plt.title('Validation: Improvement over Constructive Heuristic')
        plt.xticks(indices, subset["Instance"], rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.savefig("report/q7_improvement.png")
        print("Saved report/q7_improvement.png")
        plt.close()

if __name__ == "__main__":
    plot_benchmark_results_q7()
