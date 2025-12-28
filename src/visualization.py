"""
Visualization tools for 3D cellular automata analysis.

Provides plotting functions for individual rules and batch analysis summaries.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def plot_individual_rule(metrics, save=True):
    """
    Generate detailed 6-panel analysis plot for a single rule.
    
    Parameters
    ----------
    metrics : dict
        Metrics from analyze_rule_systematic()
    save : bool, optional
        Save plot to file (default: True)
        
    Notes
    -----
    Creates plots showing:
    - Population dynamics over time
    - Density oscillation
    - Spatial expansion
    - Structural density
    - Cells with count=1
    - Neighbor count variance
    """
    rule_number = metrics['rule_number']
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle(f'Rule {rule_number} Analysis - 26-Neighbor Moore Count', 
                 fontsize=16, fontweight='bold')
    
    # 1. Population Dynamics
    ax1 = axes[0, 0]
    ax1.plot(metrics['generation'], metrics['total_cells'], 'b-', linewidth=2)
    ax1.set_xlabel('Generation', fontsize=10)
    ax1.set_ylabel('Total Cells', fontsize=10)
    ax1.set_title('Population Dynamics', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # 2. Density Oscillation
    ax2 = axes[0, 1]
    ax2.plot(metrics['generation'], metrics['mean_neighbor_count'], 'r-', linewidth=2)
    ax2.set_xlabel('Generation', fontsize=10)
    ax2.set_ylabel('Mean Neighbor Count', fontsize=10)
    ax2.set_title('Density Oscillation', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # 3. Spatial Expansion
    ax3 = axes[0, 2]
    ax3.plot(metrics['generation'], metrics['max_distance_from_center'], 'g-', linewidth=2)
    ax3.set_xlabel('Generation', fontsize=10)
    ax3.set_ylabel('Max Distance from Center', fontsize=10)
    ax3.set_title('Spatial Expansion', fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # 4. Structural Density
    ax4 = axes[1, 0]
    ax4.plot(metrics['generation'], metrics['density'], 'm-', linewidth=2)
    ax4.set_xlabel('Generation', fontsize=10)
    ax4.set_ylabel('Density (cells/volume)', fontsize=10)
    ax4.set_title('Structural Density', fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # 5. Cells with count=1
    ax5 = axes[1, 1]
    ax5.plot(metrics['generation'], metrics['cells_count_eq_1'], 'c-', linewidth=2)
    ax5.set_xlabel('Generation', fontsize=10)
    ax5.set_ylabel('Cells with count=1', fontsize=10)
    ax5.set_title('Isolated Live Cells', fontweight='bold')
    ax5.grid(True, alpha=0.3)
    
    # 6. Neighbor Count Variance
    ax6 = axes[1, 2]
    ax6.plot(metrics['generation'], metrics['std_neighbor_count'], 'orange', linewidth=2)
    ax6.set_xlabel('Generation', fontsize=10)
    ax6.set_ylabel('Std Dev of Neighbor Count', fontsize=10)
    ax6.set_title('Neighbor Count Variance', fontweight='bold')
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save:
        filename = f'output/rule_{rule_number}_detailed.png'
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Plot saved: {filename}")
    
    plt.show()


def plot_classification_summary_v2(df, save=True):
    """
    Create comprehensive summary visualization of all 256 rules.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Classification results from classify_all_rules_v2()
    save : bool, optional
        Save plot to file (default: True)
    """
    fig = plt.figure(figsize=(18, 12))
    
    # 1. Class distribution pie chart
    ax1 = plt.subplot(3, 3, 1)
    class_counts = df['class_code'].value_counts().sort_index()
    colors = plt.cm.tab20(np.linspace(0, 1, len(class_counts)))
    ax1.pie(class_counts.values, labels=class_counts.index, 
            autopct='%1.1f%%', colors=colors)
    ax1.set_title('Distribution by Class Code', fontweight='bold')
    
    # 2. Detailed class breakdown
    ax2 = plt.subplot(3, 3, 2)
    class_counts.plot(kind='bar', ax=ax2, color=colors)
    ax2.set_xlabel('Class Code')
    ax2.set_ylabel('Number of Rules')
    ax2.set_title('Rules per Class', fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    
    # 3. Heatmap of final populations
    ax3 = plt.subplot(3, 3, 3)
    pop_grid = df.set_index('rule')['final_population'].values.reshape(16, 16)
    im = ax3.imshow(pop_grid, cmap='viridis', aspect='auto')
    ax3.set_xlabel('Rule (mod 16)')
    ax3.set_ylabel('Rule (// 16)')
    ax3.set_title('Final Population Heatmap', fontweight='bold')
    plt.colorbar(im, ax=ax3, label='Population')
    
    # 4. Scatter: Extent vs Population
    ax4 = plt.subplot(3, 3, 4)
    class_to_num = {code: i for i, code in enumerate(df['class_code'].unique())}
    colors_scatter = [class_to_num[code] for code in df['class_code']]
    scatter = ax4.scatter(df['final_extent'], df['final_population'], 
                         c=colors_scatter, cmap='tab20', alpha=0.6, s=30)
    ax4.set_xlabel('Final Spatial Extent')
    ax4.set_ylabel('Final Population')
    ax4.set_title('Extent vs Population', fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # 5. Variance distribution by class
    ax5 = plt.subplot(3, 3, 5)
    for class_code in sorted(df['class_code'].unique()):
        subset = df[df['class_code'] == class_code]['mean_variance']
        if len(subset) > 0:
            ax5.hist(subset, bins=20, alpha=0.5, label=class_code)
    ax5.set_xlabel('Mean Variance')
    ax5.set_ylabel('Count')
    ax5.set_title('Variance Distribution by Class', fontweight='bold')
    ax5.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    ax5.grid(True, alpha=0.3)
    
    # 6. Top interesting rules table
    ax6 = plt.subplot(3, 3, 6)
    ax6.axis('off')
    
    interesting = df[(df['final_population'] > 1000) & 
                     (df['mean_variance'] > 0.5)].sort_values('mean_variance', 
                                                               ascending=False).head(15)
    
    table_data = []
    for _, row in interesting.iterrows():
        table_data.append([
            int(row['rule']),
            row['class_code'],
            f"{int(row['final_population']):,}",
            f"{row['mean_variance']:.2f}"
        ])
    
    if len(table_data) > 0:
        table = ax6.table(cellText=table_data,
                         colLabels=['Rule', 'Class', 'Pop', 'Var'],
                         cellLoc='center',
                         loc='center',
                         colWidths=[0.15, 0.2, 0.3, 0.2])
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 1.5)
        ax6.set_title('Top 15 Most Complex Rules', fontweight='bold', pad=20)
    
    # 7-9: Class examples
    example_classes = ['2A', '4A', '3']
    for idx, class_code in enumerate(example_classes):
        ax = plt.subplot(3, 3, 7 + idx)
        ax.axis('off')
        
        examples = df[df['class_code'] == class_code]
        if len(examples) > 0:
            class_name = examples.iloc[0]['class_name']
            rule_list = sorted(examples['rule'].values)[:20]
            
            text = f"{class_name}\n({len(examples)} rules)\n\nExamples:\n"
            text += ", ".join([str(r) for r in rule_list])
            if len(examples) > 20:
                text += f"\n... and {len(examples) - 20} more"
            
            ax.text(0.1, 0.5, text, fontsize=9, verticalalignment='center',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout()
    
    if save:
        filename = 'output/256_rules_summary_v2.png'
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Summary plot saved: {filename}")
    
    plt.show()


def print_classification_report_v2(df):
    """
    Print detailed text report of classification results.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Classification results from classify_all_rules_v2()
    """
    print(f"\n{'='*80}")
    print(f"CLASSIFICATION REPORT - 256 3D Totalistic CA Rules")
    print(f"{'='*80}\n")
    
    print("OVERALL STATISTICS:")
    print(f"Total rules analyzed: {len(df)}")
    print(f"Unique classes found: {df['class_code'].nunique()}")
    print(f"Rules with sustained growth: {len(df[df['final_population'] > 0])}")
    print(f"Rules reaching boundary: {len(df[df['final_extent'] > 40])}\n")
    
    print("CLASS BREAKDOWN:")
    for class_code in sorted(df['class_code'].unique()):
        subset = df[df['class_code'] == class_code]
        class_name = subset.iloc[0]['class_name']
        print(f"\n{class_code}: {class_name} - {len(subset)} rules")
        
        rule_list = sorted(subset['rule'].values)
        if len(rule_list) <= 15:
            print(f"  Rules: {rule_list}")
        else:
            print(f"  First 15: {rule_list[:15]}")
            print(f"  ... and {len(rule_list) - 15} more")
        
        if len(subset) > 0:
            print(f"  Avg final pop: {subset['final_population'].mean():.0f}")
            print(f"  Avg variance: {subset['mean_variance'].mean():.3f}")
    
    print(f"\n{'='*80}")
    print("MOST INTERESTING RULES:")
    print(f"{'='*80}")
    
    interesting = df[(df['final_population'] > 1000) & 
                     (df['mean_variance'] > 0.5)].sort_values('mean_variance', 
                                                               ascending=False)
    
    for idx, row in interesting.head(20).iterrows():
        print(f"\nRule {int(row['rule'])}: {row['class_name']}")
        print(f"  Pop: {int(row['final_population']):,} | "
              f"Extent: {row['final_extent']:.1f} | "
              f"Variance: {row['mean_variance']:.3f}")
    
    print(f"\n{'='*80}\n")
