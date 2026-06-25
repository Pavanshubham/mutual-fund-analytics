-- =========================================================
-- Day 2 Analytical SQL Queries
-- Mutual Fund Analytics Project
-- =========================================================

-- 1. Top 5 fund houses by AUM
SELECT fund_house, aum_crore
FROM fact_aum
ORDER BY aum_crore DESC
LIMIT 5;

-- 2. Average NAV per month across all funds
SELECT strftime('%Y-%m', nav_date) AS month,
       ROUND(AVG(nav), 2) AS avg_nav
FROM fact_nav
GROUP BY month
ORDER BY month;

-- 3. Monthly average NAV for each scheme
SELECT amfi_code,
       strftime('%Y-%m', nav_date) AS month,
       ROUND(AVG(nav), 2) AS avg_monthly_nav
FROM fact_nav
GROUP BY amfi_code, month
ORDER BY amfi_code, month;

-- 4. Total transaction amount by state
SELECT state,
       COUNT(*) AS total_transactions,
       ROUND(SUM(amount_inr), 2) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

-- 5. Transaction type distribution
SELECT transaction_type,
       COUNT(*) AS transaction_count,
       ROUND(SUM(amount_inr), 2) AS total_amount
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount DESC;

-- 6. Funds with expense ratio below 1%
SELECT scheme_name, fund_house, expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct ASC;

-- 7. Top 10 schemes by 5-year return
SELECT d.scheme_name,
       d.fund_house,
       f.return_5yr_pct
FROM fact_performance f
JOIN dim_fund d ON f.amfi_code = d.amfi_code
ORDER BY f.return_5yr_pct DESC
LIMIT 10;

-- 8. Average 1-year return by fund house
SELECT d.fund_house,
       ROUND(AVG(f.return_1yr_pct), 2) AS avg_1yr_return
FROM fact_performance f
JOIN dim_fund d ON f.amfi_code = d.amfi_code
GROUP BY d.fund_house
ORDER BY avg_1yr_return DESC;

-- 9. Redemption amount by city tier
SELECT city_tier,
       ROUND(SUM(amount_inr), 2) AS redemption_amount
FROM fact_transactions
WHERE transaction_type = 'REDEMPTION'
GROUP BY city_tier
ORDER BY redemption_amount DESC;

-- 10. KYC status distribution
SELECT kyc_status,
       COUNT(*) AS investor_count
FROM fact_transactions
GROUP BY kyc_status
ORDER BY investor_count DESC;