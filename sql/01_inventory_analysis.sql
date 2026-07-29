-- ==============================================================================
-- PROJECT: Supply Chain & Inventory Health Analysis
-- MODULE: 01_inventory_health_analysis.sql
-- AUTHOR: Joel Banuelos Soto
-- DESCRIPTION: Computes Daily Sales Rate (DSR), Days of Supply (DSI), 
--              Inventory Turnover, and classifies stockout/overstock risk levels.
-- ==============================================================================

WITH base_inventory AS (
    SELECT 
        sku_id,
        sku_name,
        category,
        unit_cost_usd,
        stock_on_hand,
        annual_sales_units,
        -- Calculate Daily Sales Rate (DSR), preventing division by zero
        ROUND(annual_sales_units / 365.0, 4) AS daily_sales_rate,
        -- Calculate Total Working Capital tied up per SKU
        ROUND(stock_on_hand * unit_cost_usd, 2) AS capital_tied_up_usd
    FROM raw_inventory_data
),

dsi_calculations AS (
    SELECT 
        sku_id,
        sku_name,
        category,
        unit_cost_usd,
        stock_on_hand,
        annual_sales_units,
        daily_sales_rate,
        capital_tied_up_usd,
        -- DSI (Days of Supply) = Current Stock / Daily Consumption Rate
        CASE 
            WHEN daily_sales_rate > 0 THEN ROUND(stock_on_hand / daily_sales_rate, 1)
            ELSE 999.0 -- Indicator for zero-demand / obsolete stock
        END AS dsi_days
    FROM base_inventory
)

SELECT 
    sku_id,
    sku_name,
    category,
    unit_cost_usd,
    stock_on_hand,
    annual_sales_units,
    daily_sales_rate,
    capital_tied_up_usd,
    dsi_days,
    -- Operational Status Segmentation Strategy
    CASE 
        WHEN dsi_days < 7 THEN 'CRITICAL: Stockout Risk (<7d)'
        WHEN dsi_days BETWEEN 7 AND 30 THEN 'HEALTHY: Optimal Level (7-30d)'
        WHEN dsi_days BETWEEN 31 AND 45 THEN 'WARNING: Moderate Buffer (31-45d)'
        WHEN dsi_days > 45 AND category = 'Food & Beverages' THEN 'HIGH RISK: Perishable Overstock (>45d)'
        ELSE 'OVERSTOCK: Capital Tied Up (>45d)'
    END AS inventory_status_action
FROM dsi_calculations
ORDER BY capital_tied_up_usd DESC;
