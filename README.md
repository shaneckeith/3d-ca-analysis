# 3D Low-Count Totalistic Cellular Automata Analysis

A systematic framework for analyzing a fully enumerable 256-rule 3D low-count, state-independent cellular automata family using 26-neighbor Moore count.

---

## Overview

This project implements and analyzes a restricted family of 3D "totalistic-style" cellular automata. Starting from a single seed cell at the center of a cubic grid, each rule evolves according to an 8-bit rule number (0–255).

The update rule is **state-independent** (depends only on the neighbor count, not the cell's current state) and is intentionally restricted so the entire family can be exhaustively scanned and classified.

Metrics are recorded on the post-update grid each step (generation t corresponds to the state after t rule applications from the seed).

**Boundary condition**: Constant-zero padding (outside the grid is treated as dead).

---

## Key Design Choices (Defines the Rule Family)

This implementation is a deliberate, tractable restriction:

1. **26-neighbor Moore count (excludes self)**  
   Each cell's next state depends on the count of its **26 surrounding neighbors** in the 3×3×3 Moore neighborhood (the center cell itself is **excluded**).

2. **8-bit rule space (0–255)**  
   Only neighbor counts **0–7** are addressable by the rule. Any location with count **≥ 8** is forced to 0 (dead) in the next generation.

3. **State-independent update**  
   The next state depends only on the neighbor count, not on whether the cell is currently alive. Unlike Life-like (outer-totalistic) rules, there is no separate birth/survival condition—cells are set solely by neighbor count each step.

These restrictions define a fully enumerable family of **2^8 = 256** rules that emphasizes sparse, frontier-driven dynamics.

---

## Relationship to Wolfram's 3D Count-Mask Totalistic Rules

Wolfram's canonical 3D count-mask totalistic rules (as commonly presented in the Demonstrations Project) use:

- **26-neighbor Moore count** (excluding the center cell)
- **27-bit mask** over counts 0–26 (a space of **2^27 = 134,217,728** rules)
- **Full count range 0–26 addressable**

This project uses the **same neighbor counting convention** but with a **different mask width and truncation**:

- **26-neighbor Moore count** (excluding the center cell) ✓ same
- **8-bit mask** over counts 0–7 (256 rules)
- **Counts 0–7 addressable, counts ≥8 forced dead**

This systematic restriction is optimized for:

- Complete enumeration and classification
- Reproducible comparisons across all rules
- Analysis of behavior in the low-density regime

---

## Key Features

- ✅ Complete implementation of 256 low-count totalistic 3D CA rules
- ✅ Automated classification into distinct behavioral classes
- ✅ Quantitative metrics: population dynamics, spatial expansion, density, variance
- ✅ Batch processing for systematic analysis
- ✅ Visual and statistical analysis tools

---

## Installation

```bash
git clone https://github.com/shaneckeith/3d-ca-analysis.git
cd 3d-ca-analysis
pip install -r requirements.txt
pip install -e .  # Install package in editable mode
```

---

## Quick Start

### Analyze a Single Rule

```python
from src.core import analyze_rule_systematic
from src.visualization import plot_individual_rule

# Run Rule 54 for 100 generations
metrics = analyze_rule_systematic(size=51, generations=100, rule_number=54)

# Visualize results
plot_individual_rule(metrics)
```

### Analyze All 256 Rules

```bash
python examples/run_all_256.py
```

This will:
- Run all 256 rules (run time depends on hardware; typically minutes to tens of minutes)
- Save raw data to `data/`
- Generate classification report
- Create summary visualizations in `output/`

---

## Classification System

Rules are classified into distinct behavioral classes based on empirical observation:

| Class | Name | Description |
|-------|------|-------------|
| **1A** | Immediate Extinction | Dies within 5 generations |
| **1B** | Delayed Extinction | Dies after initial growth |
| **2A** | Extinction Blink | Oscillates between 0 and full grid |
| **2B** | Sparse-Full Blink | Oscillates between sparse pattern and full grid |
| **2C** | Static/Local Periodic | Small stable or periodic patterns |
| **2D** | Expanding Oscillator | Growing oscillating structures |
| **3** | Chaotic Turbulent | High variance, sustained chaos |
| **4A** | Structured Expander | Directed growth, satellite formation |
| **4B** | Structured Bounded | Complex but contained |
| **5** | Complex Stable | High complexity that stabilizes |
| **6** | Simple Growth | Low complexity expansion |

**Note**: Classification thresholds are currently tuned for `size=51` and constant-zero boundaries; changing `size` may require re-tuning thresholds.

---

## Methodology

### Rule Encoding

Each 8-bit rule number controls neighbor counts 0–7.

**Example: Rule 54 = 00110110 (binary)**

```
Bit 7 (MSB) → count 7 → 0 (die)
Bit 6       → count 6 → 0 (die)
Bit 5       → count 5 → 1 (live)
Bit 4       → count 4 → 1 (live)
Bit 3       → count 3 → 0 (die)
Bit 2       → count 2 → 1 (live)
Bit 1       → count 1 → 1 (live)
Bit 0 (LSB) → count 0 → 0 (die)
```

**Result**: Rule 54 produces live cells for counts **{1, 2, 4, 5}**. All counts **≥ 8** produce dead cells.

### Update Algorithm

```python
# 1) Create 3×3×3 Moore neighborhood kernel (excludes center cell)
kernel = np.ones((3, 3, 3))
kernel[1, 1, 1] = 0  # Exclude self → 26-neighbor count

# 2) Compute 26-neighbor count for each cell
neighbor_count = convolve(grid, kernel, mode="constant", cval=0)

# 3) Convert rule number to binary (MSB to LSB order)
rule = rule_to_binary(rule_number)  # 8-bit array

# 4) Apply rule based on count (0–7 only)
new_grid = np.zeros_like(grid)
for c in range(8):
    new_grid[neighbor_count == c] = rule[7 - c]  # LSB maps to count 0

# All cells with count ≥ 8 remain 0 (dead)
```

### Initial Condition

All simulations start from a **single live cell** at the center of a cubic grid (typically 51×51×51), allowing pure rule-driven evolution without bias from complex seeds.

### Metrics Collected

For each generation:

- **Population**: Total cells alive
- **Spatial extent**: Maximum distance from center
- **Density**: Cells per unit volume (spherical approximation)
- **Neighbor count statistics**: Mean, min, max, standard deviation
- **Structural metrics**: Cells with specific neighbor counts

---

## Results

From systematic analysis of all 256 rules (size=51³, constant-zero boundaries, single-seed initial condition):

- **~50%** die immediately (Class 1A)
- **~25%** show blinking universe behavior (Class 2B)
- **~10%** show structured expansion (Class 4A)
- **~3%** achieve complex stable states (Class 5)
- Several rules exhibit maximum chaos (Class 3)

The dominance of extinction and blinking behaviors reflects the low-count truncation: high-density regions (count ≥8) are forced to die, creating dramatic global dynamics in finite grids.

---

## Project Structure

```
3d-ca-analysis/
│
├── src/
│   ├── core.py              # CA simulation engine
│   ├── classification.py    # Classification logic
│   ├── visualization.py     # Plotting functions
│   └── batch_analysis.py    # Batch processing pipeline
│
├── examples/
│   ├── run_single_rule.py   # Single rule analysis
│   └── run_all_256.py       # Full 256-rule batch analysis
│
├── data/                    # Generated data outputs
├── output/                  # Visualizations and results
├── setup.py                 # Package installation
└── README.md
```

---

## Citation

If you use this work, please cite:

```
Keith, Shane. (2025). 3D Low-Count Totalistic Cellular Automata Analysis.
GitHub repository: https://github.com/shaneckeith/3d-ca-analysis
```

---

## Acknowledgments

This work builds on foundational concepts from:

- Wolfram, S. (2002). *A New Kind of Science*. Wolfram Media.
- Wolfram, S. (2007). "3D Totalistic Cellular Automata." *Wolfram Demonstrations Project*.

Our implementation explores a specific 8-bit restricted subfamily optimized for systematic analysis.

---

## Future Directions

Possible extensions of this work:

1. **Full 27-bit canonical rules**: Extend to address all counts 0–26 (2^27 rule space)
2. **Outer-totalistic (Life-like)**: Add birth/survival distinction based on current state
3. **Alternative mappings**: Map counts 0–26 to 8 bins via modulo or range binning
4. **Sparse sampling**: Heuristically explore the 2^27 canonical space
5. **3D Life variants**: Implement known 3D Life rules for comparison
6. **27-cell sum variant**: Compare behavior when self is included in the sum

---

## License

MIT License — see [LICENSE](LICENSE) file for details.

---

## Contact

Shane Keith  
[GitHub](https://github.com/shaneckeith) | [LinkedIn](https://linkedin.com/in/shaneckeith)

---

**Note**: This project documents what was actually implemented (8-bit low-count totalistic rules with 26-neighbor count), not theoretical capabilities. The code is complete, tested, and reproducible as described.
