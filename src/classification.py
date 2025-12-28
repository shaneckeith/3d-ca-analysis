"""
Classification system for 3D cellular automata behavioral patterns.

Classifies rules into distinct behavioral classes based on quantitative metrics.
"""

import numpy as np
import pandas as pd


def classify_rule_v2(metrics):
    """
    Classify rule behavior based on comprehensive metrics.
    
    Parameters
    ----------
    metrics : dict
        Metrics from analyze_rule_systematic()
        
    Returns
    -------
    tuple
        (class_name: str, class_code: str)
        
    Notes
    -----
    Classification scheme:
    - Class 1A/1B: Extinction patterns
    - Class 2A: Extinction blink (0 ↔ full)
    - Class 2B: Sparse-full blink (N ↔ full)
    - Class 2C/2D: Static/oscillating patterns
    - Class 3: Chaotic turbulent
    - Class 4A/4B: Structured complex
    - Class 5: Complex stable
    - Class 6: Simple growth
    """
    final_pop = metrics['total_cells'][-1]
    max_pop = max(metrics['total_cells'])
    min_pop = min(metrics['total_cells'])
    final_extent = metrics['max_distance_from_center'][-1]
    grid_volume = 51**3  # Assuming 51³ grid
    
    # Variance metrics
    mean_variance = np.mean(metrics['std_neighbor_count'][-20:]) if final_pop > 0 else 0
    variance_trend = np.std(metrics['std_neighbor_count'][-20:])
    
    # Population metrics
    pop_last_20 = metrics['total_cells'][-20:]
    unique_pops = len(set(pop_last_20))
    
    # Min population after initial growth
    if len(metrics['total_cells']) > 20:
        min_pop_after_growth = min(metrics['total_cells'][20:])
    else:
        min_pop_after_growth = min_pop
    
    # ========================================================================
    # CLASS 1: EXTINCTION
    # ========================================================================
    if final_pop == 0:
        extinct_gen = next((i for i, p in enumerate(metrics['total_cells']) if p == 0), 
                          len(metrics['total_cells']))
        if extinct_gen < 5:
            return ("Class 1A: Immediate Extinction", "1A")
        else:
            return ("Class 1B: Delayed Extinction", "1B")
    
    # ========================================================================
    # CLASS 2: PERIODIC PATTERNS
    # ========================================================================
    
    fills_grid = (max_pop > 0.7 * grid_volume)
    
    if fills_grid:
        # 2A: Complete Extinction Blink
        if min_pop_after_growth == 0:
            return ("Class 2A: Extinction Blink (0↔Full)", "2A")
        
        # 2B: Sparse-to-Full Blink
        if min_pop_after_growth > 0 and min_pop_after_growth < 1000:
            return ("Class 2B: Sparse-Full Blink (N↔Full)", "2B")
    
    # Check for periodicity
    if unique_pops < 10:
        # 2C: Small Static/Periodic
        if mean_variance < 0.5 and max_pop < 5000:
            return ("Class 2C: Static/Local Periodic", "2C")
        
        # 2D: Expanding Oscillator
        if mean_variance < 0.5 and max_pop >= 5000:
            if len(metrics['total_cells']) > 40:
                early_avg = np.mean(metrics['total_cells'][10:20])
                late_avg = np.mean(metrics['total_cells'][-20:])
                if late_avg > early_avg * 2:
                    return ("Class 2D: Expanding Oscillator", "2D")
                else:
                    return ("Class 2C: Stable Oscillator", "2C")
            else:
                return ("Class 2C: Stable Oscillator", "2C")
    
    # ========================================================================
    # CLASS 3: CHAOTIC TURBULENT FILL
    # ========================================================================
    
    if mean_variance > 2.0 and max_pop > 20000:
        if variance_trend > 0.1:
            return ("Class 3: Chaotic Turbulent", "3")
    
    # ========================================================================
    # CLASS 4: STRUCTURED COMPLEX
    # ========================================================================
    
    if 1.3 < mean_variance <= 2.0 and final_pop > 10000:
        if final_extent > 40:
            return ("Class 4A: Structured Expander (Boundary)", "4A")
        else:
            return ("Class 4B: Structured Bounded", "4B")
    
    # ========================================================================
    # CLASS 5: COMPLEX STABLE
    # ========================================================================
    
    if mean_variance >= 1.8 and variance_trend < 0.1:
        return ("Class 5: Complex Stable", "5")
    
    # ========================================================================
    # CLASS 6: SIMPLE GROWTH
    # ========================================================================
    
    if final_pop > 1000 and mean_variance < 1.3:
        return ("Class 6: Simple Growth", "6")
    
    # ========================================================================
    # UNCLASSIFIED
    # ========================================================================
    return ("Class 0: Unclassified", "0")


def classify_all_rules_v2(all_results):
    """
    Classify all rules in a batch analysis.
    
    Parameters
    ----------
    all_results : dict
        Dictionary mapping rule numbers to their metrics
        
    Returns
    -------
    pandas.DataFrame
        Classification results with columns:
        - rule: Rule number
        - class_code: Classification code
        - class_name: Full classification name
        - final_population: Final cell count
        - mean_variance: Average variance
        - And more...
    """
    classifications = []
    
    for rule, metrics in all_results.items():
        class_name, class_code = classify_rule_v2(metrics)
        
        classifications.append({
            'rule': rule,
            'class_code': class_code,
            'class_name': class_name,
            'final_population': metrics['total_cells'][-1],
            'max_population': max(metrics['total_cells']),
            'min_population': min(metrics['total_cells']),
            'final_extent': metrics['max_distance_from_center'][-1],
            'mean_variance': np.mean(metrics['std_neighbor_count'][-20:]) if metrics['total_cells'][-1] > 0 else 0,
            'mean_density': np.mean(metrics['density'][-20:]) if metrics['total_cells'][-1] > 0 else 0
        })
    
    return pd.DataFrame(classifications)