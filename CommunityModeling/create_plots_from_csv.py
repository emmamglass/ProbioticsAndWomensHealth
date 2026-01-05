#!/usr/bin/env python3
"""
Create visualization plots from pairwise_summary.csv
This allows you to iterate on plot styling without re-running simulations.
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Output directory
OUTPUT_DIR = 'pairwise_results'

def create_visualizations(df_summary):
    """Create visualization plots for results."""
    print("\nCreating visualizations from CSV data...")
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)
    
    # 1. Growth Suppression Comparison
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Growth suppression by category
    ax1 = axes[0, 0]
    sns.boxplot(data=df_summary, x='Category', y='Growth_Suppression', ax=ax1)
    ax1.set_title('Growth Suppression: Safe Candidate vs BV-Associated', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Growth Suppression (fractional reduction)')
    ax1.set_xlabel('Partner Category')
    
    # Niche overlap comparison
    ax2 = axes[0, 1]
    sns.boxplot(data=df_summary, x='Category', y='Niche_Overlap', ax=ax2)
    ax2.set_title('Niche Overlap (Jaccard Distance)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Niche Overlap (Jaccard Distance)')
    ax2.set_xlabel('Partner Category')
    
    # D-lactate production
    ax3 = axes[1, 0]
    sns.boxplot(data=df_summary, x='Category', y='D_Lactate_Production', ax=ax3)
    ax3.set_title('D-Lactate Production', fontsize=12, fontweight='bold')
    ax3.set_ylabel('D-Lactate Production Flux')
    ax3.set_xlabel('Partner Category')
    
    # Growth suppression vs D-lactate production
    ax4 = axes[1, 1]
    for category in df_summary['Category'].unique():
        data = df_summary[df_summary['Category'] == category]
        ax4.scatter(data['D_Lactate_Production'], data['Growth_Suppression'], 
                   label=category, alpha=0.6, s=100)
    ax4.set_xlabel('D-Lactate Production Flux')
    ax4.set_ylabel('Growth Suppression')
    ax4.set_title('Growth Suppression vs D-Lactate Production', fontsize=12, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_path = os.path.join(OUTPUT_DIR, 'pairwise_comparison_plots.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"  Saved: {plot_path}")
    plt.close()
    
    # 2. Abundance-dependent effects
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Get unique abundance ratios from the data
    abundance_ratios = df_summary['Abundance_Ratio'].unique()
    
    for idx, ratio in enumerate(abundance_ratios[:3]):  # Limit to first 3 ratios
        if idx >= 3:
            break
        ax = axes[idx]
        data = df_summary[df_summary['Abundance_Ratio'] == ratio]
        
        if len(data) > 0:
            sns.barplot(data=data, x='Partner_Name', y='Growth_Suppression', 
                       hue='Category', ax=ax)
            ax.set_title(f'Abundance Ratio {ratio}', fontsize=11, fontweight='bold')
            ax.set_ylabel('Growth Suppression')
            ax.set_xlabel('Partner Organism')
            ax.set_ylim(0.8, 1.0)  # Set y-axis range to focus on high suppression values
            ax.tick_params(axis='x', rotation=45)
            ax.legend(title='Category')
    
    plt.tight_layout()
    plot_path = os.path.join(OUTPUT_DIR, 'abundance_dependent_effects.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"  Saved: {plot_path}")
    plt.close()
    
    print("\n✓ All plots generated successfully!")

def main():
    """Main execution function."""
    print("="*60)
    print("CREATING PLOTS FROM CSV DATA")
    print("="*60)
    
    # Check if CSV file exists
    csv_path = os.path.join(OUTPUT_DIR, 'pairwise_summary.csv')
    
    if not os.path.exists(csv_path):
        print(f"\nError: CSV file not found at {csv_path}")
        print("Please run pairwise_community_modeling.py first to generate the data.")
        return
    
    # Read the CSV file
    print(f"\nReading data from: {csv_path}")
    try:
        df_summary = pd.read_csv(csv_path)
        print(f"  Loaded {len(df_summary)} rows")
        print(f"  Columns: {', '.join(df_summary.columns)}")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    # Check required columns
    required_columns = ['Category', 'Growth_Suppression', 'Niche_Overlap', 
                       'D_Lactate_Production', 'Abundance_Ratio', 'Partner_Name']
    missing_columns = [col for col in required_columns if col not in df_summary.columns]
    
    if missing_columns:
        print(f"\nError: Missing required columns: {', '.join(missing_columns)}")
        print(f"Available columns: {', '.join(df_summary.columns)}")
        return
    
    # Create visualizations
    create_visualizations(df_summary)
    
    print("\n" + "="*60)
    print("PLOTS CREATED SUCCESSFULLY")
    print("="*60)
    print(f"\nPlots saved to: {OUTPUT_DIR}/")
    print("  - pairwise_comparison_plots.png")
    print("  - abundance_dependent_effects.png")

if __name__ == '__main__':
    main()


