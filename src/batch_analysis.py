"""
Batch processing pipeline for analyzing all 256 rules.

Coordinates data collection, classification, and output generation.
"""

import pickle
import os
from datetime import datetime
from .core import analyze_rule_systematic
from .classification import classify_all_rules_v2
from .visualization import plot_classification_summary_v2, print_classification_report_v2, plot_individual_rule


def run_all_256_rules(size=51, generations=100, save_data=True):
    """
    Run all 256 rules and collect metrics.
    
    Parameters
    ----------
    size : int, optional
        Grid size (default: 51)
    generations : int, optional
        Number of generations (default: 100)
    save_data : bool, optional
        Save raw data to pickle file (default: True)
        
    Returns
    -------
    dict
        Metrics for all 256 rules
    """
    print(f"{'='*60}")
    print(f"BATCH PROCESSING: All 256 Rules")
    print(f"Grid size: {size}³ = {size**3:,} cells")
    print(f"Generations: {generations}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    all_results = {}
    
    for rule in range(256):
        if rule % 10 == 0:
            print(f"Processing Rule {rule}...")
        
        metrics = analyze_rule_systematic(
            size=size,
            generations=generations,
            rule_number=rule,
            verbose=False
        )
        
        all_results[rule] = metrics
    
    print(f"\n{'='*60}")
    print(f"COMPLETED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    if save_data:
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'data/all_256_rules_{timestamp}.pkl'
        with open(filename, 'wb') as f:
            pickle.dump(all_results, f)
        print(f"Data saved to: {filename}\n")
    
    return all_results


def run_batch_analysis(size=51, generations=100, load_existing=None):
    """
    Complete pipeline: run, classify, visualize, and report.
    
    Parameters
    ----------
    size : int, optional
        Grid size (default: 51)
    generations : int, optional
        Number of generations (default: 100)
    load_existing : str, optional
        Path to existing .pkl file to skip computation
        
    Returns
    -------
    tuple
        (all_results dict, classification_df DataFrame)
    """
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    # Step 1: Get data (run or load)
    if load_existing and os.path.exists(load_existing):
        print(f"Loading existing data from: {load_existing}\n")
        with open(load_existing, 'rb') as f:
            all_results = pickle.load(f)
    else:
        print("Running all 256 rules...\n")
        all_results = run_all_256_rules(size, generations)
    
    # Step 2: Classify
    print("Classifying rules...\n")
    classification_df = classify_all_rules_v2(all_results)
    
    # Save classification CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_filename = f'output/classification_{timestamp}.csv'
    classification_df.to_csv(csv_filename, index=False)
    print(f"Classification saved to: {csv_filename}\n")
    
    # Step 3: Generate summary visualizations
    print("Generating summary visualizations...\n")
    plot_classification_summary_v2(classification_df)
    
    # Step 4: Print text report
    print_classification_report_v2(classification_df)
    
    # Step 5: Plot top 5 interesting rules
    print("Generating detailed plots for top 5 interesting rules...\n")
    interesting = classification_df[
        (classification_df['final_population'] > 1000) & 
        (classification_df['mean_variance'] > 0.5)
    ].sort_values('mean_variance', ascending=False).head(5)
    
    for _, row in interesting.iterrows():
        rule = int(row['rule'])
        print(f"  Plotting Rule {rule}...")
        plot_individual_rule(all_results[rule])
    
    print(f"\n{'='*80}")
    print("ANALYSIS COMPLETE!")
    print(f"{'='*80}")
    print(f"\nGenerated files in output/:")
    print(f"  - classification_{timestamp}.csv")
    print(f"  - 256_rules_summary_v2.png")
    print(f"  - rule_X_detailed.png (top 5 rules)")
    print(f"\n{'='*80}\n")
    
    return all_results, classification_df