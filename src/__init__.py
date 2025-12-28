"""
3D Totalistic Cellular Automata Analysis Package

A systematic framework for analyzing all 256 totalistic 3D cellular automata rules.
"""

__version__ = "1.0.0"
__author__ = "Shane Keith"

from .core import (
    create_initial_pattern,
    rule_to_binary,
    apply_rule,
    analyze_rule_systematic
)

from .classification import (
    classify_rule_v2,
    classify_all_rules_v2
)

from .visualization import (
    plot_individual_rule,
    plot_classification_summary_v2,
    print_classification_report_v2
)

from .batch_analysis import (
    run_all_256_rules,
    run_batch_analysis
)

__all__ = [
    'create_initial_pattern',
    'rule_to_binary',
    'apply_rule',
    'analyze_rule_systematic',
    'classify_rule_v2',
    'classify_all_rules_v2',
    'plot_individual_rule',
    'plot_classification_summary_v2',
    'print_classification_report_v2',
    'run_all_256_rules',
    'run_batch_analysis'
]