-- ==============================================================================
-- PROJECT 2: Demand Planning & Forecast Accuracy
-- MODULE: sql/02_forecast_accuracy.sql
-- DESCRIPTION: Evaluates forecast accuracy (WAPE) and Sales Bias at category level
--              to drive S&OP consensus and prevent overstocking/carrying costs.
-- ==============================================================================

WITH demand_metrics AS (
    SELECT 
        category,
        sku_id,
        month,
        forecasted_units,
        actual_sales_units,
        unit_price_usd,
        -- Error absoluto y desvío de pronóstico en unidades
        ABS(actual_sales_units - forecasted_units) AS absolute_error_units,
        (forecasted_units - actual_sales_units) AS forecast_error_units,
        -- Impacto financiero del desvío
        (forecasted_units - actual_sales_units) * unit_price_usd AS variance_usd
    FROM demand_forecast_raw
)
SELECT 
    category,
    SUM(forecasted_units) AS total_forecasted_units,
    SUM(actual_sales_units) AS total_actual_sales_units,
    
    -- WAPE % = (Suma de Errores Absolutos / Suma de Ventas Reales) * 100
    ROUND(
        (SUM(absolute_error_units)::NUMERIC / NULLIF(SUM(actual_sales_units), 0)) * 100, 2
    ) AS wape_pct,
    
    -- Accuracy % = 100 - WAPE %
    ROUND(
        100 - ((SUM(absolute_error_units)::NUMERIC / NULLIF(SUM(actual_sales_units), 0)) * 100), 2
    ) AS forecast_accuracy_pct,
    
    -- Bias Rate % = ((Forecast - Actual) / Actual) * 100
    ROUND(
        ((SUM(forecasted_units) - SUM(actual_sales_units))::NUMERIC / NULLIF(SUM(actual_sales_units), 0)) * 100, 2
    ) AS bias_pct,
    
    -- Diagnóstico operativo automático para mesa de S&OP
    CASE 
        WHEN ((SUM(forecasted_units) - SUM(actual_sales_units))::NUMERIC / NULLIF(SUM(actual_sales_units), 0)) * 100 > 5.0 
            THEN 'OVER-PROMOTING (Optimistic Bias -> Risk of Overstock)'
        WHEN ((SUM(forecasted_units) - SUM(actual_sales_units))::NUMERIC / NULLIF(SUM(actual_sales_units), 0)) * 100 < -5.0 
            THEN 'UNDER-PROMOTING (Pessimistic Bias -> Risk of Stockout)'
        ELSE 'BALANCED FORECAST'
    END AS bias_diagnosis

FROM demand_metrics
GROUP BY category
ORDER BY forecast_accuracy_pct ASC;