# 3D Totalistic Cellular Automata Analysis

Systematic quantitative analysis of all 256 totalistic 3D cellular automata rules using Moore neighborhood (26 neighbors).

## Overview

This project extends Wolfram's elementary cellular automata to 3D space using a totalistic approach, where cell survival depends only on the count of neighboring cells, not their specific configuration. Starting from a single seed cell in a cubic lattice, each rule evolves according to its 8-bit rule number (0-255).

**Key Features:**
- Complete implementation of 256 totalistic 3D CA rules
- Automated classification into distinct behavioral classes
- Quantitative metrics: population dynamics, spatial expansion, density, variance
- Batch processing for systematic analysis
- Visual and statistical analysis tools

## Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/3d-ca-analysis.git
cd 3d-ca-analysis

# Install dependencies
pip install -r requirements.txt
```

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
1. Run all 256 rules (takes 1-2 hours)
2. Save raw data to `data/`
3. Generate classification report
4. Create summary visualizations in `output/`

## Classification System

Rules are classified into distinct behavioral classes:

- **Class 1A:** Immediate Extinction - Dies within 5 generations
- **Class 1B:** Delayed Extinction - Dies after initial growth
- **Class 2A:** Extinction Blink - Oscillates between 0 and full grid
- **Class 2B:** Sparse-Full Blink - Oscillates between sparse pattern and full grid
- **Class 2C:** Static/Local Periodic - Small stable or periodic patterns
- **Class 2D:** Expanding Oscillator - Growing oscillating structures
- **Class 3:** Chaotic Turbulent - High variance, sustained chaos
- **Class 4A:** Structured Expander - Directed growth, satellite formation
- **Class 4B:** Structured Bounded - Complex but contained
- **Class 5:** Complex Stable - High complexity that stabilizes
- **Class 6:** Simple Growth - Low complexity expansion

## Project Structure
```
src/
├── core.py              # CA simulation engine
├── classification.py    # Classification logic
├── visualization.py     # Plotting functions
└── batch_analysis.py    # Batch processing pipeline

examples/
├── run_single_rule.py   # Single rule analysis
└── run_all_256.py       # Full 256-rule batch analysis
```

## Methodology

### Totalistic Rules

Each cell evolves based on the **total count** of its 26 Moore neighborhood neighbors:
- Count neighbors (0-7 mapped to 8-bit rule)
- If rule bit at that count is 1, cell lives; if 0, cell dies

Example: **Rule 54** (binary: 00110110)
- Survives if neighbor count = 1, 2, 4, or 5
- Dies otherwise

### Metrics Collected

For each generation:
- Total cells alive
- Mean/min/max neighbor counts
- Spatial extent (max distance from center)
- Structural density
- Neighbor count variance
- Cells in survival zone

## Results

From systematic analysis of all 256 rules:
- **50%** die immediately (Class 1A)
- **25%** show blinking universe behavior (Class 2B)
- **~10%** show structured expansion (Class 4A)
- **~3%** achieve complex stable states (Class 5)
- **8 rules** exhibit maximum chaos (Class 3)

**Most complex rules:** 134, 198, 138, 166, 230 (variance > 2.4)

## Citation

If you use this work, please cite:
```
Keith, Shane. (2025). 3D Totalistic Cellular Automata Analysis. 
GitHub repository: https://github.com/yourusername/3d-ca-analysis
```

## Acknowledgments

Built upon Stephen Wolfram's foundational work on cellular automata:
- Wolfram, S. (2002). *A New Kind of Science*. Wolfram Media.
- Wolfram, S. (2007). *3D Totalistic Cellular Automata*. Wolfram Demonstrations Project.

## License

MIT License - See LICENSE file for details

## Future Work

- Perturbation experiments (mortality events)
- Von Neumann neighborhood comparison
- Extended generation analysis
- Rule interaction studies
- Connection to assembly theory