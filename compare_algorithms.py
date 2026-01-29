#!/usr/bin/env python3
"""
Script de comparaison des 4 algorithmes TSP avec gestion des timeouts.

Usage:
    python compare_algorithms.py <fichier.in> [--timeout SECONDS] [--grasp-iterations N] [--grasp-alpha A]

Exemple:
    python compare_algorithms.py instances/17.in --timeout 60
    python compare_algorithms.py instances/100.in --timeout 120 --grasp-iterations 50
"""

import sys
import time
import argparse
import signal
from pathlib import Path
from typing import Optional, Dict, Any
import multiprocessing as mp

# Ajouter le dossier parent au path pour importer les modules
sys.path.insert(0, str(Path(__file__).parent))

from src.model.tsp_model import TSPInstance, Solution
from src.exact.branch_and_bound import BranchAndBoundSolver
from src.constructive.nearest_neighbor import NearestNeighborSolver
from src.local_search.two_opt import LocalSearchSolver
from src.grasp.grasp_solver import GRASPSolver


class TimeoutException(Exception):
    """Exception levée quand un timeout se produit."""
    pass


def timeout_handler(signum, frame):
    """Handler pour le signal d'alarme (timeout)."""
    raise TimeoutException("Timeout!")


def run_algorithm_with_timeout(solver_class, instance, timeout, **kwargs):
    """
    Exécute un algorithme avec un timeout.
    
    Args:
        solver_class: Classe du solver à utiliser
        instance: Instance TSP
        timeout: Temps limite en secondes (None = pas de limite)
        **kwargs: Arguments supplémentaires pour le solver
    
    Returns:
        dict: Résultats avec 'solution', 'cost', 'time', 'status'
    """
    start_time = time.time()
    
    if timeout is not None and timeout > 0:
        # Configurer le signal d'alarme pour le timeout
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(int(timeout))
    
    try:
        solver = solver_class(instance, **kwargs)
        solution = solver.solve()
        elapsed_time = time.time() - start_time
        
        # Annuler l'alarme si elle existe
        if timeout is not None:
            signal.alarm(0)
        
        return {
            'solution': solution.tour if solution else None,
            'cost': solution.cost if solution else float('inf'),
            'time': elapsed_time,
            'status': 'completed'
        }
    
    except TimeoutException:
        elapsed_time = time.time() - start_time
        return {
            'solution': None,
            'cost': float('inf'),
            'time': elapsed_time,
            'status': 'timeout'
        }
    
    except Exception as e:
        elapsed_time = time.time() - start_time
        signal.alarm(0)  # Annuler l'alarme
        return {
            'solution': None,
            'cost': float('inf'),
            'time': elapsed_time,
            'status': f'error: {str(e)}'
        }


def compare_algorithms(
    instance_file: str,
    exact_timeout: int = 60,
    grasp_iterations: int = 50,
    grasp_alpha: float = 0.2
) -> Dict[str, Any]:
    """
    Compare les 4 algorithmes sur une instance donnée.
    
    Args:
        instance_file: Chemin vers le fichier d'instance
        exact_timeout: Timeout pour l'algorithme exact (secondes)
        grasp_iterations: Nombre d'itérations pour GRASP
        grasp_alpha: Paramètre alpha pour GRASP
    
    Returns:
        dict: Résultats de la comparaison
    """
    print(f"\n{'='*80}")
    print(f"Comparaison des algorithmes sur: {instance_file}")
    print(f"{'='*80}\n")
    
    # Charger l'instance
    instance = TSPInstance.from_file(instance_file)
    print(f"Instance chargée: {instance.n} villes\n")
    
    results = {}
    
    # 1. Algorithme Exact (Branch & Bound) avec timeout
    print("1. Algorithme Exact (Branch & Bound)...")
    print(f"   Timeout: {exact_timeout}s")
    
    # Pour les grandes instances, on skip l'exact
    if instance.n > 20:
        print(f"   ⚠️  Instance trop grande (n={instance.n} > 20), algorithme exact ignoré\n")
        results['exact'] = {
            'solution': None,
            'cost': float('inf'),
            'time': 0,
            'status': 'skipped (n > 20)'
        }
    else:
        results['exact'] = run_algorithm_with_timeout(
            BranchAndBoundSolver,
            instance,
            exact_timeout,
            time_limit=exact_timeout
        )
        print(f"   Statut: {results['exact']['status']}")
        if results['exact']['status'] == 'completed':
            print(f"   Coût: {results['exact']['cost']}")
        print(f"   Temps: {results['exact']['time']:.3f}s\n")
    
    # 2. Heuristique Constructive (Nearest Neighbor)
    print("2. Heuristique Constructive (Nearest Neighbor)...")
    results['constructive'] = run_algorithm_with_timeout(
        NearestNeighborSolver,
        instance,
        None  # Pas de timeout, c'est rapide
    )
    print(f"   Statut: {results['constructive']['status']}")
    print(f"   Coût: {results['constructive']['cost']}")
    print(f"   Temps: {results['constructive']['time']:.3f}s\n")
    
    # 3. Recherche Locale (2-Opt)
    print("3. Recherche Locale (2-Opt après Nearest Neighbor)...")
    # On utilise la solution constructive comme point de départ
    nn_solution = Solution(
        results['constructive']['solution'],
        results['constructive']['cost']
    )
    results['local_search'] = run_algorithm_with_timeout(
        LocalSearchSolver,
        instance,
        None,  # Pas de timeout normalement
        initial_solution=nn_solution
    )
    print(f"   Statut: {results['local_search']['status']}")
    print(f"   Coût: {results['local_search']['cost']}")
    print(f"   Temps: {results['local_search']['time']:.3f}s\n")
    
    # 4. Méta-heuristique (GRASP)
    print(f"4. Méta-heuristique (GRASP, {grasp_iterations} itérations, alpha={grasp_alpha})...")
    results['grasp'] = run_algorithm_with_timeout(
        GRASPSolver,
        instance,
        None,  # Pas de timeout, mais on peut en ajouter si besoin
        max_iterations=grasp_iterations,
        alpha=grasp_alpha
    )
    print(f"   Statut: {results['grasp']['status']}")
    print(f"   Coût: {results['grasp']['cost']}")
    print(f"   Temps: {results['grasp']['time']:.3f}s\n")
    
    return {
        'instance_file': instance_file,
        'instance_size': instance.n,
        'results': results
    }


def print_comparison_table(comparison: Dict[str, Any]):
    """Affiche un tableau récapitulatif de la comparaison."""
    print(f"\n{'='*80}")
    print("RÉSUMÉ DE LA COMPARAISON")
    print(f"{'='*80}\n")
    
    results = comparison['results']
    
    # Trouver le meilleur coût
    costs = {name: r['cost'] for name, r in results.items() if r['cost'] != float('inf')}
    best_cost = min(costs.values()) if costs else float('inf')
    
    # Tableau
    print(f"{'Algorithme':<25} {'Coût':<15} {'Temps (s)':<12} {'Gap (%)':<10} {'Statut'}")
    print("-" * 80)
    
    algorithms = [
        ('Exact (B&B)', 'exact'),
        ('Constructive (NN)', 'constructive'),
        ('Local Search (2-Opt)', 'local_search'),
        ('GRASP', 'grasp')
    ]
    
    for name, key in algorithms:
        r = results[key]
        
        # Formatage du coût
        if r['cost'] == float('inf'):
            cost_str = "N/A"
            gap_str = "N/A"
        else:
            cost_str = f"{r['cost']:.0f}"
            if best_cost > 0 and best_cost != float('inf'):
                gap = ((r['cost'] - best_cost) / best_cost) * 100
                gap_str = f"{gap:+.2f}%"
            else:
                gap_str = "0.00%"
        
        time_str = f"{r['time']:.3f}"
        status_str = r['status']
        
        print(f"{name:<25} {cost_str:<15} {time_str:<12} {gap_str:<10} {status_str}")
    
    print("\n" + "="*80)
    
    # Meilleure solution
    if best_cost != float('inf'):
        best_algo = [name for name, key in algorithms if results[key]['cost'] == best_cost][0]
        print(f"🏆 Meilleure solution: {best_algo} (coût: {best_cost:.0f})")
    
    print(f"Instance: {comparison['instance_file']} ({comparison['instance_size']} villes)")
    print("="*80 + "\n")


def export_to_latex_table(comparison: Dict[str, Any], output_file: Optional[str] = None):
    """
    Exporte les résultats en format tableau LaTeX.
    
    Args:
        comparison: Résultats de la comparaison
        output_file: Fichier de sortie (optionnel)
    """
    results = comparison['results']
    
    # Trouver le meilleur coût
    costs = {name: r['cost'] for name, r in results.items() if r['cost'] != float('inf')}
    best_cost = min(costs.values()) if costs else float('inf')
    
    latex = []
    latex.append("% Tableau de comparaison des algorithmes")
    latex.append("\\begin{table}[h]")
    latex.append("\\centering")
    latex.append("\\begin{tabular}{|l|r|r|r|l|}")
    latex.append("\\hline")
    latex.append("\\textbf{Algorithme} & \\textbf{Coût} & \\textbf{Temps (s)} & \\textbf{Gap (\\%)} & \\textbf{Statut} \\\\")
    latex.append("\\hline")
    
    algorithms = [
        ('Exact (B\\&B)', 'exact'),
        ('Constructive (NN)', 'constructive'),
        ('Local Search (2-Opt)', 'local_search'),
        ('GRASP', 'grasp')
    ]
    
    for name, key in algorithms:
        r = results[key]
        
        if r['cost'] == float('inf'):
            cost_str = "N/A"
            gap_str = "N/A"
        else:
            cost_str = f"{r['cost']:.0f}"
            if best_cost > 0 and best_cost != float('inf'):
                gap = ((r['cost'] - best_cost) / best_cost) * 100
                gap_str = f"{gap:+.2f}"
            else:
                gap_str = "0.00"
        
        time_str = f"{r['time']:.3f}"
        status_str = r['status'].replace('_', '\\_')
        
        # Mettre en gras la meilleure solution
        if r['cost'] == best_cost and best_cost != float('inf'):
            latex.append(f"\\textbf{{{name}}} & \\textbf{{{cost_str}}} & {time_str} & \\textbf{{{gap_str}}} & {status_str} \\\\")
        else:
            latex.append(f"{name} & {cost_str} & {time_str} & {gap_str} & {status_str} \\\\")
    
    latex.append("\\hline")
    latex.append("\\end{tabular}")
    latex.append(f"\\caption{{Comparaison des algorithmes sur l'instance {comparison['instance_file']} ({comparison['instance_size']} villes)}}")
    latex.append("\\label{tab:comparison}")
    latex.append("\\end{table}")
    
    latex_output = "\n".join(latex)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex_output)
        print(f"✅ Tableau LaTeX exporté dans: {output_file}")
    else:
        print("\n" + "="*80)
        print("TABLEAU LATEX")
        print("="*80 + "\n")
        print(latex_output)
        print("\n" + "="*80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Compare les 4 algorithmes TSP sur une instance donnée",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python compare_algorithms.py instances/17.in
  python compare_algorithms.py instances/100.in --timeout 120
  python compare_algorithms.py instances/51.in --grasp-iterations 100 --grasp-alpha 0.3
  python compare_algorithms.py instances/17.in --latex-output results.tex
        """
    )
    
    parser.add_argument('instance', help='Fichier d\'instance TSP (.in)')
    parser.add_argument('--timeout', type=int, default=60,
                        help='Timeout pour l\'algorithme exact en secondes (défaut: 60)')
    parser.add_argument('--grasp-iterations', type=int, default=50,
                        help='Nombre d\'itérations pour GRASP (défaut: 50)')
    parser.add_argument('--grasp-alpha', type=float, default=0.2,
                        help='Paramètre alpha pour GRASP (défaut: 0.2)')
    parser.add_argument('--latex-output', type=str, default=None,
                        help='Fichier de sortie pour le tableau LaTeX (optionnel)')
    
    args = parser.parse_args()
    
    # Vérifier que le fichier existe
    if not Path(args.instance).exists():
        print(f"❌ Erreur: Le fichier {args.instance} n'existe pas!")
        sys.exit(1)
    
    # Exécuter la comparaison
    comparison = compare_algorithms(
        args.instance,
        exact_timeout=args.timeout,
        grasp_iterations=args.grasp_iterations,
        grasp_alpha=args.grasp_alpha
    )
    
    # Afficher le tableau récapitulatif
    print_comparison_table(comparison)
    
    # Exporter en LaTeX si demandé
    export_to_latex_table(comparison, args.latex_output)


if __name__ == '__main__':
    main()
