# 3D Low-Count Totalistic Cellular Automata Analysis

Systematic quantitative analysis of a fully enumerable **256-rule** family of 3D cellular automata using a **27-cell neighborhood sum (self + 26 neighbors)**.

---

## Overview

This project implements and analyzes a restricted family of 3D "totalistic-style" cellular automata. Starting from a single seed cell at the center of a cubic grid, each rule evolves according to an 8-bit rule number (0–255).

The update rule is **state-independent** (depends only on the local neighborhood sum, not the cell's current state) and is intentionally restricted so the entire family can be exhaustively scanned and classified.

### Key Design Choices (Defines the Rule Family)

This implementation is a deliberate, tractable restriction:

1. **27-cell neighborhood sum (self + 26 neighbors)**  
   Each cell's next state depends on the sum of the **entire 3×3×3 cube**: the cell itself plus its 26 Moore neighbors (27 sites total).

2. **8-bit rule space (0–255)**  
   Only sums **0–7** are addressable by the rule. Any location with sum **≥ 8** is forced to 0 (dead) in the next generation.

3. **State-independent update**  
   The next state depends only on the neighborhood sum, not on whether the cell is currently alive.

These restrictions define a fully enumerable family of **2^8 = 256** rules that emphasizes sparse, frontier-driven dynamics.

### Relationship to Wolfram's 3D Count-Mask Totalistic Rules

Wolfram's 3D count-mask totalistic rules (as commonly presented in the [Demonstrations Project](https://demonstrations.wolfram.com/)) specify which neighbor counts 0–26 produce a live cell, using:

- **26-neighbor Moore count** (excluding the center cell)
- **27-bit mask** over counts 0–26 (a space of **2^27 = 134,217,728** rules)
- Full count range 0–26 addressable

This project explores a systematic restriction of that larger space optimized for:

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
# Clone the repository
git clone https://github.com/shaneckeith/3d-ca-analysis.git
cd 3d-ca-analysis

# Install dependencies
pip install -r requirements.txt
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
- Run all 256 rules (takes 1-2 hours)
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

---

## Methodology

### Rule Encoding

Each 8-bit rule number controls neighborhood sums 0–7.

**Example: Rule 54 = 00110110 (binary)**
```
Bit 7 (MSB) → sum 7 → 0 (die)
Bit 6       → sum 6 → 0 (die)
Bit 5       → sum 5 → 1 (live)
Bit 4       → sum 4 → 1 (live)
Bit 3       → sum 3 → 0 (die)
Bit 2       → sum 2 → 1 (live)
Bit 1       → sum 1 → 1 (live)
Bit 0 (LSB) → sum 0 → 0 (die)
```

**Result**: Rule 54 produces live cells for sums **{1, 2, 4, 5}**. All sums **≥ 8** produce dead cells.

### Update Algorithm
```python
# 1. Create 3×3×3 cubic kernel (includes center cell)
kernel = np.ones((3, 3, 3))

# 2. Compute 27-cell neighborhood sum for each cell
neighbor_sum = convolve(grid, kernel, mode='constant', cval=0)

# 3. Convert rule number to binary (MSB to LSB order)
rule = rule_to_binary(rule_number)  # 8-bit array

# 4. Apply rule based on sum (0-7 only)
new_grid = np.zeros_like(grid)
for s in range(8):
    new_grid[neighbor_sum == s] = rule[7 - s]  # LSB maps to sum 0

# All cells with sum ≥8 remain 0 (dead)
```

### Initial Condition

All simulations start from a **single live cell** at the center of a cubic grid (typically 51×51×51), allowing pure rule-driven evolution without bias from complex seeds.

### Metrics Collected

For each generation:

- **Population**: Total cells alive
- **Spatial extent**: Maximum distance from center
- **Density**: Cells per unit volume (spherical approximation)
- **Neighborhood sum statistics**: Mean, min, max, standard deviation
- **Structural metrics**: Cells in specific sum ranges

---

## Results

From systematic analysis of all 256 rules (size=51³, constant-zero boundaries, single-seed initial condition):

- **50%** die immediately (Class 1A)
- **25%** show blinking universe behavior (Class 2B)
- **~10%** show structured expansion (Class 4A)
- **~3%** achieve complex stable states (Class 5)
- **8 rules** exhibit maximum chaos (Class 3)
- **Most complex rules**: 134, 198, 138, 166, 230 (variance > 2.4)

The dominance of extinction and blinking behaviors reflects the low-count truncation: high-density regions (sum ≥8) are forced to die, creating dramatic global dynamics in finite grids.

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
├── output/                  # Visualizations
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

Our implementation explores a specific restricted subfamily optimized for systematic analysis.

---

## Future Directions

Possible extensions of this work:

1. **Canonical 3D count-mask totalistic**: Implement true 26-neighbor (self-excluded) rules with 27-bit masks
2. **Outer-totalistic (Life-like)**: Add birth/survival distinction based on current state
3. **Extended count ranges**: Map counts 0-26 to 8 bins via modulo or binning functions
4. **Sparse rule sampling**: Heuristically explore the 2^27 canonical space
5. **3D Life variants**: Implement known 3D Life rules for comparison

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

## Contact

Shane Keith  
[GitHub](https://github.com/shaneckeith) | [LinkedIn](https://linkedin.com/in/shaneckeith)

---

**Note**: This project documents what was actually implemented (8-bit low-count totalistic rules), not theoretical capabilities. The code is complete, tested, and reproducible as described.