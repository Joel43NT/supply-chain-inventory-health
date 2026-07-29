"""
==============================================================================
PROJECT: Supply Chain & Inventory Health Analysis
FILE: notebooks/01_inventory_health_analysis.py
DESCRIPTION: Data processing pipeline for inventory segmentation, 
             financial risk exposure, and asset graphic export.
==============================================================================
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------------------------------------------------
# 1. Pipeline Setup & Data Loading
# -----------------------------------------------------------------------------
# Ensure the assets directory exists for saving output charts
os.makedirs('../assets', exist_ok=True)

# Load raw operational data
# Note: Replace with your relative data path if executing inside Jupyter
try:
    df = pd.read_csv('../data/raw_inventory.csv')
except FileNotFoundError:
    print("Warning: CSV not found in relative path. Loading dummy structure for validation.")
    # Fallback simulation structure if run isolated
    data = {
        'sku_id': [f'SKU-{1000+i}' for i in range(10)],
        'category': ['Food & Beverages', 'Food & Beverages', 'Electronics', 'Personal Care'] * 2 + ['Electronics', 'Food & Beverages'],
        'unit_cost_usd': [12.5, 45.0, 120.0, 8.5, 15.0, 210.0, 5.0, 32.0, 85.0, 14.0],
        'stock_on_hand': [12000, 45000, 300, 8000, 15000, 150, 25000, 200, 500, 18000],
        'annual_sales_units': [35000, 40000, 1200, 24000, 18000, 2000, 60000, 1500, 2400, 12000]
    }
    df = pd.DataFrame(data)

# -----------------------------------------------------------------------------
# 2. Key Supply Chain Metrics Calculation
# -----------------------------------------------------------------------------
# Daily Consumption Rate
df['daily_sales_rate'] = df['annual_sales_units'] / 365.0

# Capital Tied Up ($ USD)
df['total_capital_usd'] = df['stock_on_hand'] * df['unit_cost_usd']

# Days of Supply (DSI)
df['dsi_days'] = np.where(
    df['daily_sales_rate'] > 0, 
    df['stock_on_hand'] / df['daily_sales_rate'], 
    999.0
)

# Operational Status Assignment
def assign_status(row):
    if row['dsi_days'] < 7:
        return 'Stockout Risk'
    elif 7 <= row['dsi_days'] <= 30:
        return 'Optimal Stock'
    elif row['dsi_days'] > 45 and row['category'] == 'Food & Beverages':
        return 'High Risk Perishable'
    else:
        return 'General Overstock'

df['inventory_status'] = df.apply(assign_status, axis=1)

# -----------------------------------------------------------------------------
# 3. Financial Summary Aggregation
# -----------------------------------------------------------------------------
summary_by_category = df.groupby(['category', 'inventory_status'])['total_capital_usd'].sum().reset_index()
summary_by_category['capital_millions_usd'] = summary_by_category['total_capital_usd'] / 1_000_000.0

print("\n--- EXECUTIVE CAPITAL EXPOSURE SUMMARY ---")
print(summary_by_category)

# -----------------------------------------------------------------------------
# 4. Executive Data Visualization Export
# -----------------------------------------------------------------------------
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 5))

color_palette = {
    'High Risk Perishable': '#d63031', # Dark Red
    'General Overstock': '#e17055',     # Orange/Red
    'Stockout Risk': '#fdcb6e',         # Yellow
    'Optimal Stock': '#00b894'          # Green
}

sns.barplot(
    data=summary_by_category,
    x='category',
    y='capital_millions_usd',
    hue='inventory_status',
    palette=color_palette,
    ax=ax
)

# Chart Formatting
ax.set_title('Capital Exposure by Product Category & Inventory Status ($M USD)', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Product Category', fontsize=11, fontweight='bold')
ax.set_ylabel('Capital Tied Up ($ Millions USD)', fontsize=11, fontweight='bold')
ax.legend(title='Operational Status', frameon=True)

plt.tight_layout()

# Save render directly to assets folder for README integration
output_path = '../assets/dsi_distribution.png'
plt.savefig(output_path, dpi=300)
print(f"\n[SUCCESS] Executive chart saved to: {output_path}")

# Export processed dataset for downstream BI tools
df.to_csv('../data/inventory_health_output.csv', index=False)
print("[SUCCESS] Processed data saved to: ../data/inventory_health_output.csv")
