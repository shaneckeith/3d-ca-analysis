"""
Core cellular automaton simulation engine.

Implements a 3D low-count totalistic CA using 26-neighbor Moore count
(excludes self), with an 8-bit rule for counts 0–7 and forced death for counts ≥8.
"""

import numpy as np
from scipy.ndimage import convolve


def create_initial_pattern(size: int) -> np.ndarray:
    """
    Create a single live cell in the center of a cubic grid.

    Parameters
    ----------
    size : int
        Grid dimension (creates size³ grid)

    Returns
    -------
    numpy.ndarray
        3D binary grid with a single live cell at the center
    """
    grid = np.zeros((size, size, size), dtype=int)
    grid[size // 2, size // 2, size // 2] = 1
    return grid


def rule_to_binary(rule_number: int) -> np.ndarray:
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
    This project uses an 8-bit "low-count" rule family:
      - Only neighbor counts 0–7 are addressable.
      - Neighbor counts ≥8 always map to 0 (dead).

    Bit mapping convention:
      - LSB maps to count = 0
      - MSB maps to count = 7
    Implemented via: rule[7 - count]

    Example:
      Rule 54 = 00110110 (binary) -> live for counts {1, 2, 4, 5}
    """
    if not 0 <= rule_number <= 255:
        raise ValueError("Rule number must be between 0 and 255")
    return np.array([int(x) for x in np.binary_repr(rule_number, width=8)], dtype=int)


def apply_rule(grid: np.ndarray, rule_number: int) -> np.ndarray:
    """
    Apply the low-count totalistic rule using 26-neighbor Moore count.

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
    Neighbor count uses 26 surrounding cells (excludes center/self).
    Update is state-independent: next state depends only on neighbor count.
    Counts 0–7 are mapped by the 8-bit rule; counts ≥8 remain 0 (dead).
    """
    kernel = np.ones((3, 3, 3))
    kernel[1, 1, 1] = 0  # Exclude self → true 26-neighbor count
    
    neighbor_count = convolve(grid, kernel, mode="constant", cval=0)
    rule = rule_to_binary(rule_number)

    new_grid = np.zeros_like(grid)
    for c in range(8):
        new_grid[neighbor_count == c] = rule[7 - c]

    return new_grid


def analyze_rule_systematic(
    size: int,
    generations: int,
    rule_number: int,
    verbose: bool = False
) -> dict:
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
        Metrics per generation including:
        - total_cells: Population count
        - mean_neighbor_count: Average neighbor count among live cells
        - max_neighbor_count: Max neighbor count among live cells
        - min_neighbor_count: Min neighbor count among live cells
        - max_distance_from_center: Spatial extent
        - density: Structural density (spherical approximation)
        - cells_count_eq_1: Live cells whose neighbor count == 1
        - std_neighbor_count: Neighbor count standard deviation among live cells
    """
    grid = create_initial_pattern(size)
    kernel = np.ones((3, 3, 3))
    kernel[1, 1, 1] = 0  # Exclude self → 26-neighbor count
    rule = rule_to_binary(rule_number)

    metrics = {
        "rule_number": rule_number,
        "generation": [],
        "total_cells": [],
        "mean_neighbor_count": [],
        "max_neighbor_count": [],
        "min_neighbor_count": [],
        "max_distance_from_center": [],
        "density": [],
        "cells_count_eq_1": [],
        "std_neighbor_count": [],
    }

    center = np.array([size // 2, size // 2, size // 2])

    for gen in range(generations):
        # Compute neighbor count for CURRENT grid
        neighbor_count = convolve(grid, kernel, mode="constant", cval=0)

        # Apply rule (counts 0–7 only; counts ≥8 remain 0)
        new_grid = np.zeros_like(grid)
        for c in range(8):
            new_grid[neighbor_count == c] = rule[7 - c]
        grid = new_grid

        # Recompute neighbor count for UPDATED grid so metrics align
        neighbor_count = convolve(grid, kernel, mode="constant", cval=0)

        # Population
        total = int(np.sum(grid))
        metrics["generation"].append(gen + 1)
        metrics["total_cells"].append(total)

        if total > 0:
            occupied = np.argwhere(grid == 1)
            neighbor_counts_active = neighbor_count[grid == 1]

            # Spatial extent
            distances = np.linalg.norm(occupied - center, axis=1)
            max_dist = float(distances.max())

            # Density (spherical approximation around center)
            volume = (4 / 3) * np.pi * (max_dist ** 3) if max_dist > 0 else 1.0
            density = float(total / volume)

            metrics["mean_neighbor_count"].append(float(neighbor_counts_active.mean()))
            metrics["max_neighbor_count"].append(int(neighbor_counts_active.max()))
            metrics["min_neighbor_count"].append(int(neighbor_counts_active.min()))
            metrics["max_distance_from_center"].append(max_dist)
            metrics["density"].append(density)
            metrics["cells_count_eq_1"].append(int(np.sum(neighbor_counts_active == 1)))
            metrics["std_neighbor_count"].append(float(neighbor_counts_active.std()))

            if verbose and (gen + 1) % 10 == 0:
                print(f"  Gen {gen+1}: {total} cells, max_dist={max_dist:.1f}")
        else:
            # Extinct
            metrics["mean_neighbor_count"].append(0.0)
            metrics["max_neighbor_count"].append(0)
            metrics["min_neighbor_count"].append(0)
            metrics["max_distance_from_center"].append(0.0)
            metrics["density"].append(0.0)
            metrics["cells_count_eq_1"].append(0)
            metrics["std_neighbor_count"].append(0.0)

            if verbose:
                print(f"  Gen {gen+1}: EXTINCT")

    return metrics
