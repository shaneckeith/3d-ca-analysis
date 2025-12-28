"""
Core cellular automaton simulation engine.

Implements a 3D low-count totalistic-style CA using a 27-cell (3×3×3) neighborhood sum
(self + 26 neighbors), with an 8-bit rule for sums 0–7 and forced death for sums ≥ 8.
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
      - Only neighborhood sums 0–7 are addressable.
      - Neighborhood sums ≥ 8 always map to 0 (dead).

    Bit mapping convention:
      - LSB maps to sum = 0
      - MSB maps to sum = 7
    Implemented via: rule[7 - sum]

    Example:
      Rule 54 = 00110110 (binary) -> live for sums {1, 2, 4, 5}
    """
    if not 0 <= rule_number <= 255:
        raise ValueError("Rule number must be between 0 and 255")
    return np.array([int(x) for x in np.binary_repr(rule_number, width=8)], dtype=int)


def apply_rule(grid: np.ndarray, rule_number: int) -> np.ndarray:
    """
    Apply the low-count totalistic rule using a 27-cell neighborhood sum.

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
    Neighborhood sum includes self + 26 surrounding cells (27 total).
    Update is state-independent: next state depends only on the neighborhood sum.
    Sums 0–7 are mapped by the 8-bit rule; sums ≥ 8 remain 0 (dead).
    """
    kernel = np.ones((3, 3, 3))
    neighbor_sum = convolve(grid, kernel, mode="constant", cval=0)
    rule = rule_to_binary(rule_number)

    new_grid = np.zeros_like(grid)
    for s in range(8):
        new_grid[neighbor_sum == s] = rule[7 - s]

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
        - mean_neighbor_sum: Average neighborhood sum among live cells
        - max_neighbor_sum: Max neighborhood sum among live cells
        - min_neighbor_sum: Min neighborhood sum among live cells
        - max_distance_from_center: Spatial extent
        - density: Structural density (spherical approximation)
        - cells_sum_eq_1: Live cells whose neighborhood sum == 1
        - std_neighbor_sum: Neighborhood sum standard deviation among live cells
    """
    grid = create_initial_pattern(size)
    kernel = np.ones((3, 3, 3))
    rule = rule_to_binary(rule_number)

    metrics = {
        "rule_number": rule_number,
        "generation": [],
        "total_cells": [],
        "mean_neighbor_sum": [],
        "max_neighbor_sum": [],
        "min_neighbor_sum": [],
        "max_distance_from_center": [],
        "density": [],
        "cells_sum_eq_1": [],
        "std_neighbor_sum": [],
    }

    center = np.array([size // 2, size // 2, size // 2])

    for gen in range(generations):
        # Compute neighborhood sum for CURRENT grid
        neighbor_sum = convolve(grid, kernel, mode="constant", cval=0)

        # Apply rule (sums 0–7 only; sums ≥ 8 remain 0)
        new_grid = np.zeros_like(grid)
        for s in range(8):
            new_grid[neighbor_sum == s] = rule[7 - s]
        grid = new_grid

        # Recompute neighborhood sum for UPDATED grid so metrics align
        neighbor_sum = convolve(grid, kernel, mode="constant", cval=0)

        # Population
        total = int(np.sum(grid))
        metrics["generation"].append(gen + 1)
        metrics["total_cells"].append(total)

        if total > 0:
            occupied = np.argwhere(grid == 1)
            neighbor_sums_active = neighbor_sum[grid == 1]

            # Spatial extent
            distances = np.linalg.norm(occupied - center, axis=1)
            max_dist = float(distances.max())

            # Density (spherical approximation around center)
            volume = (4 / 3) * np.pi * (max_dist ** 3) if max_dist > 0 else 1.0
            density = float(total / volume)

            metrics["mean_neighbor_sum"].append(float(neighbor_sums_active.mean()))
            metrics["max_neighbor_sum"].append(int(neighbor_sums_active.max()))
            metrics["min_neighbor_sum"].append(int(neighbor_sums_active.min()))
            metrics["max_distance_from_center"].append(max_dist)
            metrics["density"].append(density)
            metrics["cells_sum_eq_1"].append(int(np.sum(neighbor_sums_active == 1)))
            metrics["std_neighbor_sum"].append(float(neighbor_sums_active.std()))

            if verbose and (gen + 1) % 10 == 0:
                print(f"  Gen {gen+1}: {total} cells, max_dist={max_dist:.1f}")
        else:
            # Extinct
            metrics["mean_neighbor_sum"].append(0.0)
            metrics["max_neighbor_sum"].append(0)
            metrics["min_neighbor_sum"].append(0)
            metrics["max_distance_from_center"].append(0.0)
            metrics["density"].append(0.0)
            metrics["cells_sum_eq_1"].append(0)
            metrics["std_neighbor_sum"].append(0.0)

            if verbose:
                print(f"  Gen {gen+1}: EXTINCT")

    return metrics
