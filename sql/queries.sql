-- 1. Reporting mensuel : Actual vs Budget avec écart
SELECT
    month,
    SUM(budget) AS total_budget,
    SUM(actual) AS total_actual,
    SUM(variance) AS total_variance,
    ROUND(SUM(variance) / NULLIF(SUM(budget), 0) * 100, 2) AS variance_pct
FROM financial_data
GROUP BY month
ORDER BY month;

-- 2. Top 5 départements avec les plus grands écarts
SELECT
    department,
    SUM(budget) AS total_budget,
    SUM(actual) AS total_actual,
    SUM(variance) AS total_variance,
    ROUND(SUM(variance) / NULLIF(SUM(budget), 0) * 100, 2) AS variance_pct
FROM financial_data
GROUP BY department
ORDER BY ABS(SUM(variance)) DESC
    LIMIT 5;

-- 3. Détection d'anomalies (SQL pur)
SELECT month, department, budget, actual, variance_pct
FROM financial_data
WHERE ABS(variance_pct) > 40
ORDER BY ABS(variance_pct) DESC;

-- 4. Contrôle de cohérence : lignes suspectes
SELECT * FROM financial_data
WHERE actual < 0
   OR budget < 0
   OR variance != (actual - budget);

-- 5. Traçabilité : nombre de lignes par mois (détection doublons)
SELECT month, department, COUNT(*) as n_rows
FROM financial_data
GROUP BY month, department
HAVING COUNT(*) > 1;