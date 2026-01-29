#!/usr/bin/env python3
"""
Script de comparaison AVEC GRAPHIQUES des 4 algorithmes TSP.

Usage:
    python compare_with_plots.py <fichier.in> [OPTIONS]

Exemple:
    python compare_with_plots.py instances/17.in
    python compare_with_plots.py instances/100.in --timeout 120
"""

import sys
import time
import argparse
import signal
from pathlib import Path
from typing import Optional, Dict, Any, List
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Backend pour sauvegarder sans afficher

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent))

from src.model.tsp_model import TSPInstance, Solution
from src.exact.branch_and_bound import BranchAndBoundSolver
from src.constructive.nearest_neighbor import NearestNeighborSolver
from src.local_search.two_opt import LocalSearchSolver
from src.grasp.grasp_solver import GRASPSolver


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException("Timeout!")


def run_algorithm_with_timeout(solver_class, instance, timeout, **kwargs):
    """Exécute un algorithme avec timeout."""
    start_time = time.time()
    
    if timeout is not None and timeout > 0:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(int(timeout))
    
    try:
        solver = solver_class(instance, **kwargs)
        solution = solver.solve()
        elapsed_time = time.time() - start_time
        
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
        signal.alarm(0)
        return {
            'solution': None,
            'cost': float('inf'),
            'time': elapsed_time,
            'status': f'error: {str(e)}'
        }


def compare_algorithms(instance_file: str, exact_timeout: int = 60,
                      grasp_iterations: int = 50, grasp_alpha: float = 0.2):
    """Compare les 4 algorithmes."""
    print(f"\n{'='*80}")
    print(f"Comparaison des algorithmes sur: {instance_file}")
    print(f"{'='*80}\n")
    
    instance = TSPInstance.from_file(instance_file)
    print(f"Instance chargée: {instance.n} villes\n")
    
    results = {}
    
    # 1. Exact (Branch & Bound)
    print("1. Algorithme Exact (Branch & Bound)...")
    if instance.n > 20:
        print(f"   ⚠️  Instance trop grande (n={instance.n}), ignoré\n")
        results['exact'] = {'solution': None, 'cost': float('inf'), 'time': 0, 'status': 'skipped'}
    else:
        results['exact'] = run_algorithm_with_timeout(
            BranchAndBoundSolver, instance, exact_timeout, time_limit=exact_timeout
        )
        print(f"   Statut: {results['exact']['status']}")
        if results['exact']['status'] == 'completed':
            print(f"   Coût: {results['exact']['cost']}")
        print(f"   Temps: {results['exact']['time']:.3f}s\n")
    
    # 2. Constructive (Nearest Neighbor)
    print("2. Heuristique Constructive (Nearest Neighbor)...")
    results['constructive'] = run_algorithm_with_timeout(NearestNeighborSolver, instance, None)
    print(f"   Coût: {results['constructive']['cost']}")
    print(f"   Temps: {results['constructive']['time']:.3f}s\n")
    
    # 3. Local Search (2-Opt)
    print("3. Recherche Locale (2-Opt)...")
    nn_solution = Solution(results['constructive']['solution'], results['constructive']['cost'])
    results['local_search'] = run_algorithm_with_timeout(
        LocalSearchSolver, instance, None, initial_solution=nn_solution
    )
    print(f"   Coût: {results['local_search']['cost']}")
    print(f"   Temps: {results['local_search']['time']:.3f}s\n")
    
    # 4. GRASP
    print(f"4. Méta-heuristique (GRASP, {grasp_iterations} itérations)...")
    results['grasp'] = run_algorithm_with_timeout(
        GRASPSolver, instance, None, max_iterations=grasp_iterations, alpha=grasp_alpha
    )
    print(f"   Coût: {results['grasp']['cost']}")
    print(f"   Temps: {results['grasp']['time']:.3f}s\n")
    
    return {
        'instance_file': instance_file,
        'instance_size': instance.n,
        'results': results
    }


def create_visualizations(comparison: Dict[str, Any], output_dir: str = "results"):
    """Crée des graphiques de comparaison."""
    
    Path(output_dir).mkdir(exist_ok=True)
    
    results = comparison['results']
    instance_name = Path(comparison['instance_file']).stem
    
    # Préparer les données
    algorithms = ['Exact\n(B&B)', 'Constructive\n(NN)', 'Local Search\n(2-Opt)', 'GRASP']
    keys = ['exact', 'constructive', 'local_search', 'grasp']
    
    costs = [results[k]['cost'] if results[k]['cost'] != float('inf') else None for k in keys]
    times = [results[k]['time'] for k in keys]
    
    # Couleurs cohérentes
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
    
    # =========================================================================
    # Graphique 1: Comparaison des Coûts
    # =========================================================================
    fig, ax = plt.subplots(figsize=(10, 6))
    
    valid_costs = [(alg, cost, col) for alg, cost, col in zip(algorithms, costs, colors) if cost is not None]
    
    if valid_costs:
        algs, vals, cols = zip(*valid_costs)
        bars = ax.bar(algs, vals, color=cols, alpha=0.7, edgecolor='black', linewidth=1.5)
        
        # Ajouter les valeurs sur les barres
        for bar, val in zip(bars, vals):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{val:.0f}',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # Trouver le meilleur
        min_cost = min(vals)
        for bar, val in zip(bars, vals):
            if val == min_cost:
                bar.set_edgecolor('gold')
                bar.set_linewidth(3)
    
    ax.set_ylabel('Coût de la solution', fontsize=12, fontweight='bold')
    ax.set_title(f'Comparaison des Coûts - Instance {instance_name} ({comparison["instance_size"]} villes)', 
                 fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/{instance_name}_costs.png', dpi=300, bbox_inches='tight')
    print(f"✅ Graphique des coûts sauvegardé: {output_dir}/{instance_name}_costs.png")
    plt.close()
    
    # =========================================================================
    # Graphique 2: Comparaison des Temps
    # =========================================================================
    fig, ax = plt.subplots(figsize=(10, 6))
    
    valid_times = [(alg, t, col) for alg, t, col in zip(algorithms, times, colors) if t > 0]
    
    if valid_times:
        algs, vals, cols = zip(*valid_times)
        bars = ax.bar(algs, vals, color=cols, alpha=0.7, edgecolor='black', linewidth=1.5)
        
        for bar, val in zip(bars, vals):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{val:.3f}s',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_ylabel('Temps d\'exécution (secondes)', fontsize=12, fontweight='bold')
    ax.set_title(f'Comparaison des Temps d\'Exécution - Instance {instance_name}', 
                 fontsize=14, fontweight='bold')
    ax.set_yscale('log')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/{instance_name}_times.png', dpi=300, bbox_inches='tight')
    print(f"✅ Graphique des temps sauvegardé: {output_dir}/{instance_name}_times.png")
    plt.close()
    
    # =========================================================================
    # Graphique 3: Gap à la meilleure solution
    # =========================================================================
    valid_costs_for_gap = [c for c in costs if c is not None and c != float('inf')]
    
    if len(valid_costs_for_gap) > 1:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        best_cost = min(valid_costs_for_gap)
        gaps = []
        gap_labels = []
        gap_colors = []
        
        for alg, cost, col in zip(algorithms, costs, colors):
            if cost is not None and cost != float('inf') and best_cost > 0:
                gap = ((cost - best_cost) / best_cost) * 100
                gaps.append(gap)
                gap_labels.append(alg)
                gap_colors.append(col)
        
        if gaps:
            bars = ax.bar(gap_labels, gaps, color=gap_colors, alpha=0.7, edgecolor='black', linewidth=1.5)
            
            for bar, gap in zip(bars, gaps):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{gap:+.2f}%',
                       ha='center', va='bottom', fontsize=11, fontweight='bold')
            
            # Mettre en valeur le meilleur (gap = 0)
            for bar, gap in zip(bars, gaps):
                if abs(gap) < 0.01:
                    bar.set_edgecolor('gold')
                    bar.set_linewidth(3)
        
        ax.set_ylabel('Gap par rapport au meilleur (%)', fontsize=12, fontweight='bold')
        ax.set_title(f'Écart à la Meilleure Solution - Instance {instance_name}', 
                     fontsize=14, fontweight='bold')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/{instance_name}_gaps.png', dpi=300, bbox_inches='tight')
        print(f"✅ Graphique des gaps sauvegardé: {output_dir}/{instance_name}_gaps.png")
        plt.close()
    
    # =========================================================================
    # Graphique 4: Ratio Qualité/Temps
    # =========================================================================
    fig, ax = plt.subplots(figsize=(10, 6))
    
    valid_points = []
    for alg, cost, time_val, col in zip(algorithms, costs, times, colors):
        if cost is not None and cost != float('inf') and time_val > 0:
            valid_points.append((alg, cost, time_val, col))
    
    if valid_points:
        for alg, cost, time_val, col in valid_points:
            ax.scatter(time_val, cost, s=300, alpha=0.7, c=col, edgecolors='black', linewidth=2)
            ax.annotate(alg.replace('\n', ' '), (time_val, cost), 
                       xytext=(10, 10), textcoords='offset points',
                       fontsize=10, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor=col, alpha=0.3))
    
    ax.set_xlabel('Temps d\'exécution (secondes)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Coût de la solution', fontsize=12, fontweight='bold')
    ax.set_title(f'Compromis Qualité/Temps - Instance {instance_name}', 
                 fontsize=14, fontweight='bold')
    ax.set_xscale('log')
    ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/{instance_name}_tradeoff.png', dpi=300, bbox_inches='tight')
    print(f"✅ Graphique compromis sauvegardé: {output_dir}/{instance_name}_tradeoff.png")
    plt.close()
    
    print(f"\n{'='*80}")
    print(f"🎨 4 graphiques créés dans le dossier '{output_dir}/'")
    print(f"{'='*80}\n")


def print_summary_table(comparison: Dict[str, Any]):
    """Affiche un tableau récapitulatif."""
    print(f"\n{'='*80}")
    print("📊 RÉSUMÉ DE LA COMPARAISON")
    print(f"{'='*80}\n")
    
    results = comparison['results']
    costs = {name: r['cost'] for name, r in results.items() if r['cost'] != float('inf')}
    best_cost = min(costs.values()) if costs else float('inf')
    
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
        
        # Mettre une étoile pour la meilleure solution
        if r['cost'] == best_cost and best_cost != float('inf'):
            name = f"🏆 {name}"
        
        print(f"{name:<25} {cost_str:<15} {time_str:<12} {gap_str:<10} {status_str}")
    
    print("\n" + "="*80)
    print(f"Instance: {comparison['instance_file']} ({comparison['instance_size']} villes)")
    print("="*80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Compare les 4 algorithmes TSP avec génération de graphiques",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python compare_with_plots.py instances/17.in
  python compare_with_plots.py instances/100.in --timeout 120
  python compare_with_plots.py instances/51.in --output-dir mes_resultats
        """
    )
    
    parser.add_argument('instance', help='Fichier d\'instance TSP (.in)')
    parser.add_argument('--timeout', type=int, default=60,
                        help='Timeout pour l\'algorithme exact (défaut: 60s)')
    parser.add_argument('--grasp-iterations', type=int, default=50,
                        help='Nombre d\'itérations GRASP (défaut: 50)')
    parser.add_argument('--grasp-alpha', type=float, default=0.2,
                        help='Paramètre alpha GRASP (défaut: 0.2)')
    parser.add_argument('--output-dir', type=str, default='results',
                        help='Dossier pour sauvegarder les graphiques (défaut: results)')
    
    args = parser.parse_args()
    
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
    
    # Afficher le résumé
    print_summary_table(comparison)
    
    # Créer les graphiques
    create_visualizations(comparison, args.output_dir)
    
    print("\n✨ Analyse terminée avec succès!")
    print(f"📊 Consultez les graphiques dans le dossier '{args.output_dir}/'")
    print(f"💡 Vous pouvez intégrer ces images dans votre rapport LaTeX\n")


if __name__ == '__main__':
    main()
