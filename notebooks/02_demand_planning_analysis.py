"""
==============================================================================
PROJECT 2: Demand Planning & Forecast Accuracy
MODULE: notebooks/02_demand_planning_analysis.py
DESCRIPTION: Evaluates forecast error (MAPE/WAPE), measures Sales Bias, 
             and projects inventory cost impact for S&OP consensus.
==============================================================================
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Cargar datos desde la carpeta data/
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, '..', 'data', 'demand_forecast_raw.csv')

df = pd.read_csv(data_path)

# 2. Cálculos Estadísticos de Demanda
df['absolute_error_units'] = np.abs(df['actual_sales_units'] - df['forecasted_units'])
df['forecast_error_units'] = df['forecasted_units'] - df['actual_sales_units'] # (+) Over-forecast, (-) Under-forecast
df['variance_usd'] = df['forecast_error_units'] * df['unit_price_usd']

# 3. Agregación de Métricas por Categoría
category_metrics = df.groupby('category').agg(
    total_forecasted=('forecasted_units', 'sum'),
    total_actual=('actual_sales_units', 'sum'),
    total_abs_error=('absolute_error_units', 'sum'),
    total_variance_usd=('variance_usd', 'sum')
).reset_index()

# WAPE (Weighted Absolute Percentage Error) y Accuracy
category_metrics['wape_%'] = (category_metrics['total_abs_error'] / category_metrics['total_actual']) * 100
category_metrics['accuracy_%'] = 100 - category_metrics['wape_%']

# Bias Rate (%) = (Forecast - Actual) / Actual
category_metrics['bias_%'] = ((category_metrics['total_forecasted'] - category_metrics['total_actual']) / category_metrics['total_actual']) * 100

def interpret_bias(bias):
    if bias > 5.0:
        return 'OVER-PROMOTING (Optimistic Bias -> Risk of Overstock)'
    elif bias < -5.0:
        return 'UNDER-PROMOTING (Pessimistic Bias -> Risk of Stockout)'
    else:
        return 'BALANCED FORECAST'

category_metrics['bias_diagnosis'] = category_metrics['bias_%'].apply(interpret_bias)

print("--- S&OP DEMAND FORECAST PERFORMANCE SUMMARY ---")
print(category_metrics[['category', 'total_actual', 'accuracy_%', 'bias_%', 'bias_diagnosis']])

# 4. Generar Gráfico Ejecutivo
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 5))

df_melted = df.groupby('category')[['forecasted_units', 'actual_sales_units']].sum().reset_index()
df_melted = pd.melt(df_melted, id_vars=['category'], value_vars=['forecasted_units', 'actual_sales_units'],
                    var_name='Metric', value_name='Units')

df_melted['Metric'] = df_melted['Metric'].map({'forecasted_units': 'Sales Forecast (Commercial)', 'actual_sales_units': 'Actual Demand (Real)'})

sns.barplot(data=df_melted, x='category', y='Units', hue='Metric', palette=['#0984e3', '#00b894'], ax=ax)

ax.set_title('S&OP Consensus: Sales Forecast vs Actual Market Demand (Units)', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Product Category', fontsize=11, fontweight='bold')
ax.set_ylabel('Total Units', fontsize=11, fontweight='bold')
ax.legend(title='Demand Metric', frameon=True)

plt.tight_layout()

# Guardar la gráfica en la carpeta assets/
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
plt.savefig(os.path.join(assets_dir, 'forecast_vs_actual.png'), dpi=300)
print("\n[SUCCESS] S&OP Forecast chart saved to assets/forecast_vs_actual.png")