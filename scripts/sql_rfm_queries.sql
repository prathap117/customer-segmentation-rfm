-- ============================================================
-- SQL RFM Queries — Customer Segmentation Analysis
-- Author: Yaradoni Prathapa
-- ============================================================

-- ── 1. COMPUTE RFM METRICS (SQLite syntax) ────────────────────────────────────
WITH snapshot AS (
    SELECT MAX(InvoiceDate) AS max_date FROM retail_sales
),
rfm_raw AS (
    SELECT
        CustomerID,
        CAST(julianday((SELECT max_date FROM snapshot)) -
             julianday(MAX(InvoiceDate)) AS INTEGER)       AS recency_days,
        COUNT(DISTINCT InvoiceNo)                          AS frequency,
        ROUND(SUM(Quantity * UnitPrice), 2)                AS monetary
    FROM retail_sales
    WHERE InvoiceNo NOT LIKE 'C%'
      AND Quantity > 0
      AND UnitPrice > 0
      AND CustomerID IS NOT NULL
    GROUP BY CustomerID
)
SELECT *
FROM rfm_raw
ORDER BY monetary DESC;

-- ── 2. SEGMENT CUSTOMERS BY THRESHOLDS ───────────────────────────────────────
WITH snapshot AS (
    SELECT MAX(InvoiceDate) AS max_date FROM retail_sales
),
rfm_raw AS (
    SELECT
        CustomerID,
        CAST(julianday((SELECT max_date FROM snapshot)) -
             julianday(MAX(InvoiceDate)) AS INTEGER)       AS recency_days,
        COUNT(DISTINCT InvoiceNo)                          AS frequency,
        ROUND(SUM(Quantity * UnitPrice), 2)                AS monetary
    FROM retail_sales
    WHERE InvoiceNo NOT LIKE 'C%'
      AND Quantity > 0
      AND UnitPrice > 0
      AND CustomerID IS NOT NULL
    GROUP BY CustomerID
)
SELECT
    CustomerID,
    recency_days,
    frequency,
    monetary,
    CASE
        WHEN recency_days <= 30  AND frequency >= 10 AND monetary >= 1000 THEN 'Champions'
        WHEN recency_days <= 90  AND frequency >= 5                        THEN 'Loyal Customers'
        WHEN recency_days <= 30  AND frequency < 5                         THEN 'Potential Loyalists'
        WHEN recency_days BETWEEN 91 AND 180 AND frequency >= 5            THEN 'At Risk'
        WHEN recency_days > 180                                            THEN 'Lost Customers'
        ELSE 'Need Attention'
    END AS segment
FROM rfm_raw
ORDER BY monetary DESC;

-- ── 3. SEGMENT SUMMARY — Count, Avg RFM, Revenue Share ───────────────────────
WITH snapshot AS (
    SELECT MAX(InvoiceDate) AS max_date FROM retail_sales
),
rfm_raw AS (
    SELECT
        CustomerID,
        CAST(julianday((SELECT max_date FROM snapshot)) -
             julianday(MAX(InvoiceDate)) AS INTEGER)       AS recency_days,
        COUNT(DISTINCT InvoiceNo)                          AS frequency,
        ROUND(SUM(Quantity * UnitPrice), 2)                AS monetary
    FROM retail_sales
    WHERE InvoiceNo NOT LIKE 'C%'
      AND Quantity > 0
      AND UnitPrice > 0
      AND CustomerID IS NOT NULL
    GROUP BY CustomerID
),
segmented AS (
    SELECT *,
        CASE
            WHEN recency_days <= 30  AND frequency >= 10 AND monetary >= 1000 THEN 'Champions'
            WHEN recency_days <= 90  AND frequency >= 5                        THEN 'Loyal Customers'
            WHEN recency_days <= 30  AND frequency < 5                         THEN 'Potential Loyalists'
            WHEN recency_days BETWEEN 91 AND 180 AND frequency >= 5            THEN 'At Risk'
            WHEN recency_days > 180                                            THEN 'Lost Customers'
            ELSE 'Need Attention'
        END AS segment
    FROM rfm_raw
)
SELECT
    segment,
    COUNT(*)                                             AS customer_count,
    ROUND(AVG(recency_days), 1)                         AS avg_recency_days,
    ROUND(AVG(frequency), 1)                            AS avg_frequency,
    ROUND(AVG(monetary), 2)                             AS avg_monetary,
    ROUND(SUM(monetary), 2)                             AS total_revenue,
    ROUND(100.0 * SUM(monetary) /
          SUM(SUM(monetary)) OVER (), 2)                AS revenue_share_pct
FROM segmented
GROUP BY segment
ORDER BY total_revenue DESC;

-- ── 4. TOP 10 CHAMPIONS ───────────────────────────────────────────────────────
WITH snapshot AS (SELECT MAX(InvoiceDate) AS max_date FROM retail_sales),
rfm_raw AS (
    SELECT
        CustomerID,
        CAST(julianday((SELECT max_date FROM snapshot)) -
             julianday(MAX(InvoiceDate)) AS INTEGER) AS recency_days,
        COUNT(DISTINCT InvoiceNo)                    AS frequency,
        ROUND(SUM(Quantity * UnitPrice), 2)          AS monetary
    FROM retail_sales
    WHERE InvoiceNo NOT LIKE 'C%' AND Quantity > 0 AND UnitPrice > 0
      AND CustomerID IS NOT NULL
    GROUP BY CustomerID
)
SELECT CustomerID, recency_days, frequency, monetary
FROM rfm_raw
WHERE recency_days <= 30 AND frequency >= 10 AND monetary >= 1000
ORDER BY monetary DESC
LIMIT 10;
