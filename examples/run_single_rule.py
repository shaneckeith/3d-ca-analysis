"""
Example: Analyze a single CA rule in detail.

This script demonstrates how to analyze and visualize a single rule.
"""

import sys
sys.path.append('..')

from src import analyze_rule_systematic, plot_individual_rule, classify_rule_v2


def main():
    """Run analysis on a single rule."""
    
    # Configuration
    RULE_NUMBER = 54
    GRID_SIZE = 51
    GENERATIONS = 100
    
    print(f"Analyzing Rule {RULE_NUMBER}...")
    print(f"Grid size: {GRID_SIZE}³")
    print(f"Generations: {GENERATIONS}\n")
    
    # Run simulation
    metrics = analyze_rule_systematic(
        size=GRID_SIZE,
        generations=GENERATIONS,
        rule_number=RULE_NUMBER,
        verbose=True
    )
    
    # Classify
    class_name, class_code = classify_rule_v2(metrics)
    print(f"\nClassification: {class_name} ({class_code})")
    
    # Summary statistics
    print(f"\nSummary Statistics:")
    print(f"  Max population: {max(metrics['total_cells']):,}")
    print(f"  Final population: {metrics['total_cells'][-1]:,}")
    print(f"  Max spatial extent: {max(metrics['max_distance_from_center']):.2f}")
    print(f"  Mean variance: {sum(metrics['std_neighbor_count'][-20:]) / 20:.3f}")
    
    # Visualize
    print(f"\nGenerating visualization...")
    plot_individual_rule(metrics)
    
    print(f"\nAnalysis complete!")


if __name__ == "__main__":
    main()