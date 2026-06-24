-- 1. Top 5 fund houses by AUM
SELECT fund_house, aum_crore
FROM fact_aum
ORDER BY aum_crore DESC
LIMIT 5;

-- 2. Average NAV per month
SELECT strftime('%Y-%m', nav_date) AS month, ROUND(AVG(nav), 2) AS avg_nav
FROM fact_nav
GROUP BY month
ORDER BY month;

-- 3. Total transactions by state
SELECT state, COUNT(*) AS total_transactions, SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

-- 4. Funds with expense ratio below 1%
SELECT scheme_name, fund_house, expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;

-- 5. Top 10 funds by 5-year return
SELECT d.scheme_name, d.fund_house, f.return_5yr_pct
FROM fact_performance f
JOIN dim_fund d
ON f.amfi_code = d.amfi_code
ORDER BY f.return_5yr_pct DESC
LIMIT 10;

-- 6. Average 1-year return by fund house
SELECT d.fund_house, ROUND(AVG(f.return_1yr_pct), 2) AS avg_1yr_return
FROM fact_performance f
JOIN dim_fund d
ON f.amfi_code = d.amfi_code
GROUP BY d.fund_house
ORDER BY avg_1yr_return DESC;

-- 7. Redemption amount by city tier
SELECT city_tier, SUM(amount_inr) AS redemption_amount
FROM fact_transactions
WHERE transaction_type = 'REDEMPTION'
GROUP BY city_tier
ORDER BY redemption_amount DESC;

-- 8. KYC status distribution
SELECT kyc_status, COUNT(*) AS investor_count
FROM fact_transactions
GROUP BY kyc_status;

-- 9. Average NAV by scheme
SELECT amfi_code, ROUND(AVG(nav), 2) AS avg_nav
FROM fact_nav
GROUP BY amfi_code
ORDER BY avg_nav DESC;

-- 10. Highest Sharpe ratio schemes
SELECT d.scheme_name, d.fund_house, f.sharpe_ratio
FROM fact_performance f
JOIN dim_fund d
ON f.amfi_code = d.amfi_code
ORDER BY f.sharpe_ratio DESC
LIMIT 10;