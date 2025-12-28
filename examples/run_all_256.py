"""
Example: Batch analysis of all 256 CA rules.

This script runs the complete pipeline: simulation, classification, 
visualization, and reporting.
"""

import sys
sys.path.append('..')

from src import run_batch_analysis


def main():
    """Run complete batch analysis."""
    
    # Configuration
    GRID_SIZE = 51
    GENERATIONS = 100
    
    # Optional: load existing data instead of re-running
    # LOAD_EXISTING = 'data/all_256_rules_20251227_180000.pkl'
    LOAD_EXISTING = None
    
    print("="*80)
    print("3D TOTALISTIC CELLULAR AUTOMATA - BATCH ANALYSIS")
    print("="*80)
    print(f"\nConfiguration:")
    print(f"  Grid size: {GRID_SIZE}³ = {GRID_SIZE**3:,} cells")
    print(f"  Generations: {GENERATIONS}")
    print(f"  Total rules: 256")
    
    if LOAD_EXISTING:
        print(f"  Mode: Loading existing data")
    else:
        print(f"  Mode: Running fresh simulation (estimated time: 1-2 hours)")
    
    print("\n" + "="*80 + "\n")
    
    # Run complete analysis
    all_results, classification_df = run_batch_analysis(
        size=GRID_SIZE,
        generations=GENERATIONS,
        load_existing=LOAD_EXISTING
    )
    
    # Additional custom analysis can go here
    # For example:
    # - Extract specific rules for further study
    # - Generate custom plots
    # - Export data in different formats
    
    print("\nAll outputs saved to output/ directory")
    print("Raw data saved to data/ directory")


if __name__ == "__main__":
    main()