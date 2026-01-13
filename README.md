# TSP Optimization Project

This project implements various algorithms to solve the Traveling Salesperson Problem (TSP).

## Structure

- **src/**: Source code.
  - **model/**: Base classes (`TSPInstance`, `Solution`, `Solver`).
  - **constructive/**: Nearest Neighbor implementation.
  - **local_search/**: 2-opt implementation.
  - **grasp/**: GRASP metaheuristic implementation.
  - **exact/**: Branch and Bound implementation.
- **instances/**: Directory for problem instances.
  - **new_instances/**: The set of instances used for benchmarking.
- **report/**: Contains the final report (`RAPPORT.md`) and benchmark results.
- **benchmark.py**: Script to run experiments.

## Usage

### Prerequisites
- Python 3.x
- `pandas` and `tabulate` (install via `pip install pandas tabulate`)

### Running the Benchmark
To run the solvers on all instances in `instances/new_instances/` and generate results:

```bash
python3 benchmark.py
```

### Running Individual Solvers
Because of the project structure (relative imports), you must run files as modules from the project root.

**Do not run:** `python src/exact/branch_and_bound.py` (This will cause an ImportError).

**Instead, run:**
```bash
python3 -m src.exact.branch_and_bound
```
*(Note: Currently the individual files do not have a main block to execute logic, they just define classes. Use `benchmark.py` to run them.)*

## Authors
[Your Name/Team]
