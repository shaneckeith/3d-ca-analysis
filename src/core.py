"""
Core cellular automaton simulation engine.

Implements 3D totalistic CA with Moore neighborhood (26 neighbors).
"""

import numpy as np
from scipy.ndimage import convolve


def create_initial_pattern(size):
    """
    Create a single live cell in the center of a cubic grid.
    
    Parameters
    ----------
    size : int
        Grid dimension (creates size³ grid)
        
    Returns
    -------
    numpy.ndarray
        3D binary grid with single cell at center
    """
    grid = np.zeros((size, size, size), dtype=int)
    grid[size // 2, size // 2, size // 2] = 1
    return grid


def rule_to_binary(rule_number):
    """
    Convert rule number to 8-bit binary representation.
    
    Parameters
    ----------
    rule_number : int
        Rule number (0-255)
        
    Returns
    -------
    numpy.ndarray
        8-element binary array representing the rule
        
    Notes
    -----
    Bit i determines survival for neighbor count i (for i=0-7).
    Example: Rule 54 = 00110110 means survive if count = 1,2,4,5
    """
    if not 0 <= rule_number <= 255:
        raise ValueError("Rule number must be between 0 and 255")
    return np.array([int(x) for x in np.binary_repr(rule_number, width=8)], dtype=int)


def apply_rule(grid, rule_number):
    """
    Apply totalistic rule with Moore neighborhood.
    
    Parameters
    ----------
    grid : numpy.ndarray
        Current state (3D binary array)
    rule_number : int
        Rule to apply (0-255)
        
    Returns
    -------
    numpy.ndarray
        Next generation grid
        
    Notes
    -----
    Moore neighborhood includes all 26 surrounding cells.
    Cells survive based on total neighbor count matching rule bits.
    """
    # Create Moore neighborhood kernel (26 neighbors + self)
    kernel = np.ones((3, 3, 3))
    kernel[1, 1, 1] = 1
    
    # Count neighbors
    neighbor_count = convolve(grid, kernel, mode='constant', cval=0)
    
    # Get rule bits
    rule = rule_to_binary(rule_number)
    
    # Apply rule
    new_grid = np.zeros_like(grid)
    for i in range(8):
        pattern = (neighbor_count == i)
        new_grid[pattern] = rule[7 - i]
    
    return new_grid


def analyze_rule_systematic(size, generations, rule_number, verbose=False):
    """
    Run CA rule and collect comprehensive metrics.
    
    Parameters
    ----------
    size : int
        Grid dimension
    generations : int
        Number of generations to simulate
    rule_number : int
        Rule to analyze (0-255)
    verbose : bool, optional
        Print progress updates
        
    Returns
    -------
    dict
        Comprehensive metrics for each generation including:
        - total_cells: Population count
        - mean_neighbor_count: Average neighbor density
        - max_distance_from_center: Spatial extent
        - density: Structural density
        - std_neighbor_count: Neighbor count variance
        And more...
    """
    grid = create_initial_pattern(size)
    kernel = np.ones((3, 3, 3))
    kernel[1, 1, 1] = 1
    rule = rule_to_binary(rule_number)
    
    # Initialize metrics storage
    metrics = {
        'rule_number': rule_number,
        'generation': [],
        'total_cells': [],
        'mean_neighbor_count': [],
        'max_neighbor_count': [],
        'min_neighbor_count': [],
        'max_distance_from_center': [],
        'density': [],
        'cells_in_survival_zone': [],
        'std_neighbor_count': []
    }
    
    center = np.array([size//2, size//2, size//2])
    
    for gen in range(generations):
        # Count neighbors
        neighbor_count = convolve(grid, kernel, mode='constant', cval=0)
        
        # Apply rule
        new_grid = np.zeros_like(grid)
        for i in range(8):
            pattern = (neighbor_count == i)
            new_grid[pattern] = rule[7 - i]
        grid = new_grid
        
        # Collect metrics
        total = np.sum(grid)
        
        if total > 0:
            occupied = np.argwhere(grid == 1)
            neighbor_counts_active = neighbor_count[grid == 1]
            
            # Spatial metrics
            distances = np.linalg.norm(occupied - center, axis=1)
            max_dist = distances.max()
            
            # Density
            volume = (4/3) * np.pi * (max_dist ** 3) if max_dist > 0 else 1
            density = total / volume
            
            # Store metrics
            metrics['generation'].append(gen + 1)
            metrics['total_cells'].append(int(total))
            metrics['mean_neighbor_count'].append(float(neighbor_counts_active.mean()))
            metrics['max_neighbor_count'].append(int(neighbor_counts_active.max()))
            metrics['min_neighbor_count'].append(int(neighbor_counts_active.min()))
            metrics['max_distance_from_center'].append(float(max_dist))
            metrics['density'].append(float(density))
            metrics['cells_in_survival_zone'].append(int(np.sum(neighbor_counts_active == 1)))
            metrics['std_neighbor_count'].append(float(neighbor_counts_active.std()))
            
            if verbose and (gen + 1) % 10 == 0:
                print(f"  Gen {gen+1}: {total} cells, max_dist={max_dist:.1f}")
        else:
            # Extinct
            metrics['generation'].append(gen + 1)
            metrics['total_cells'].append(0)
            metrics['mean_neighbor_count'].append(0.0)
            metrics['max_neighbor_count'].append(0)
            metrics['min_neighbor_count'].append(0)
            metrics['max_distance_from_center'].append(0.0)
            metrics['density'].append(0.0)
            metrics['cells_in_survival_zone'].append(0)
            metrics['std_neighbor_count'].append(0.0)
            
            if verbose:
                print(f"  Gen {gen+1}: EXTINCT")
    
    return metrics