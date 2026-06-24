# Data Dictionary – Mutual Fund Analytics Project

## Project Overview

This data dictionary documents the cleaned datasets and SQLite star schema created for the Mutual Fund Analytics project. The project focuses on mutual fund performance, NAV trends, investor transactions, AUM analysis, and industry-level SIP/folio trends.

---

# 1. Dimension Table: `dim_fund`

**Source:** `01_fund_master_cleaned.csv`

| Column             | Data Type | Business Definition                                                          |
| ------------------ | --------- | ---------------------------------------------------------------------------- |
| amfi_code          | INTEGER   | Unique AMFI scheme code identifying a mutual fund scheme                     |
| fund_house         | TEXT      | Mutual fund company / AMC name                                               |
| scheme_name        | TEXT      | Name of the mutual fund scheme                                               |
| category           | TEXT      | Broad scheme category such as Equity, Debt, or Hybrid                        |
| sub_category       | TEXT      | Detailed scheme classification such as Large Cap, Mid Cap, Liquid, Flexi Cap |
| plan               | TEXT      | Plan type such as Direct or Regular                                          |
| launch_date        | DATE      | Date on which the scheme was launched                                        |
| benchmark          | TEXT      | Benchmark index used to evaluate scheme performance                          |
| expense_ratio_pct  | REAL      | Annual expense ratio charged by the fund                                     |
| exit_load_pct      | REAL      | Exit load percentage charged on redemption                                   |
| min_sip_amount     | INTEGER   | Minimum SIP investment amount for the scheme                                 |
| min_lumpsum_amount | INTEGER   | Minimum lumpsum investment amount for the scheme                             |
| fund_manager       | TEXT      | Fund manager responsible for the scheme                                      |
| risk_category      | TEXT      | Risk label of the fund such as Low, Moderate, High                           |
| sebi_category_code | TEXT      | SEBI-defined scheme category code                                            |

---

# 2. Dimension Table: `dim_date`

**Source:** Derived from all date columns across cleaned datasets

| Column       | Data Type | Business Definition              |
| ------------ | --------- | -------------------------------- |
| date_id      | INTEGER   | Surrogate key for date dimension |
| full_date    | DATE      | Full calendar date               |
| year         | INTEGER   | Calendar year                    |
| quarter      | INTEGER   | Calendar quarter (1–4)           |
| month        | INTEGER   | Month number (1–12)              |
| month_name   | TEXT      | Month name                       |
| day          | INTEGER   | Day of month                     |
| weekday_name | TEXT      | Day name such as Monday, Tuesday |

---

# 3. Fact Table: `fact_nav`

**Source:** `02_nav_history_cleaned.csv`

| Column    | Data Type | Business Definition                        |
| --------- | --------- | ------------------------------------------ |
| nav_id    | INTEGER   | Surrogate key for NAV fact table           |
| amfi_code | INTEGER   | Mutual fund scheme code                    |
| nav_date  | DATE      | Date on which NAV was recorded             |
| nav       | REAL      | Net Asset Value of the scheme on that date |

---

# 4. Fact Table: `fact_transactions`

**Source:** `08_investor_transactions_cleaned.csv`

| Column             | Data Type | Business Definition                                     |
| ------------------ | --------- | ------------------------------------------------------- |
| transaction_id     | INTEGER   | Surrogate key for transaction record                    |
| investor_id        | TEXT      | Unique investor identifier                              |
| transaction_date   | DATE      | Date of transaction                                     |
| amfi_code          | INTEGER   | Mutual fund scheme code                                 |
| transaction_type   | TEXT      | Type of transaction such as SIP, Lumpsum, or Redemption |
| amount_inr         | REAL      | Transaction amount in Indian Rupees                     |
| state              | TEXT      | State of investor                                       |
| city               | TEXT      | City of investor                                        |
| city_tier          | TEXT      | Tier classification of investor city                    |
| age_group          | TEXT      | Investor age bucket                                     |
| gender             | TEXT      | Investor gender                                         |
| annual_income_lakh | REAL      | Annual income of investor in lakhs                      |
| payment_mode       | TEXT      | Payment method used for the transaction                 |
| kyc_status         | TEXT      | KYC verification status of the investor                 |

---

# 5. Fact Table: `fact_performance`

**Source:** `07_scheme_performance_cleaned.csv`

| Column             | Data Type | Business Definition                           |
| ------------------ | --------- | --------------------------------------------- |
| performance_id     | INTEGER   | Surrogate key for performance record          |
| amfi_code          | INTEGER   | Mutual fund scheme code                       |
| return_1yr_pct     | REAL      | Scheme return over the last 1 year (%)        |
| return_3yr_pct     | REAL      | Scheme return over the last 3 years (%)       |
| return_5yr_pct     | REAL      | Scheme return over the last 5 years (%)       |
| benchmark_3yr_pct  | REAL      | Benchmark return over the last 3 years (%)    |
| alpha              | REAL      | Excess return generated relative to benchmark |
| beta               | REAL      | Volatility relative to benchmark / market     |
| sharpe_ratio       | REAL      | Risk-adjusted return measure                  |
| sortino_ratio      | REAL      | Downside-risk-adjusted return measure         |
| std_dev_ann_pct    | REAL      | Annualized standard deviation of returns      |
| max_drawdown_pct   | REAL      | Maximum decline from peak to trough           |
| aum_crore          | REAL      | Assets under management in crore rupees       |
| expense_ratio_pct  | REAL      | Expense ratio of the scheme                   |
| morningstar_rating | INTEGER   | Morningstar star rating                       |
| risk_grade         | TEXT      | Risk grade assigned to the scheme             |

---

# 6. Fact Table: `fact_aum`

**Source:** `03_aum_by_fund_house_cleaned.csv`

| Column         | Data Type | Business Definition                         |
| -------------- | --------- | ------------------------------------------- |
| aum_id         | INTEGER   | Surrogate key for AUM record                |
| aum_date       | DATE      | Reporting date for AUM                      |
| fund_house     | TEXT      | Mutual fund company / AMC name              |
| aum_lakh_crore | REAL      | Assets under management in lakh crore       |
| aum_crore      | REAL      | Assets under management in crore rupees     |
| num_schemes    | INTEGER   | Number of schemes offered by the fund house |

---

# 7. Additional Cleaned Files (Available for analysis / dashboarding)

## `04_monthly_sip_inflows_cleaned.csv`

| Column                    | Data Type | Business Definition                          |
| ------------------------- | --------- | -------------------------------------------- |
| month                     | DATE      | Reporting month                              |
| sip_inflow_crore          | REAL      | SIP inflows during the month in crore rupees |
| active_sip_accounts_crore | REAL      | Active SIP accounts in crore                 |
| new_sip_accounts_lakh     | REAL      | New SIP accounts opened in lakh              |
| sip_aum_lakh_crore        | REAL      | SIP assets under management in lakh crore    |
| yoy_growth_pct            | REAL      | Year-over-year SIP inflow growth percentage  |

## `05_category_inflows_cleaned.csv`

| Column           | Data Type | Business Definition                          |
| ---------------- | --------- | -------------------------------------------- |
| month            | DATE      | Reporting month                              |
| category         | TEXT      | Mutual fund category                         |
| net_inflow_crore | REAL      | Net inflow into the category in crore rupees |

## `06_industry_folio_count_cleaned.csv`

| Column              | Data Type | Business Definition                |
| ------------------- | --------- | ---------------------------------- |
| month               | DATE      | Reporting month                    |
| total_folios_crore  | REAL      | Total mutual fund folios in crore  |
| equity_folios_crore | REAL      | Equity mutual fund folios in crore |
| debt_folios_crore   | REAL      | Debt mutual fund folios in crore   |
| hybrid_folios_crore | REAL      | Hybrid mutual fund folios in crore |
| others_folios_crore | REAL      | Other category folios in crore     |

## `09_portfolio_holdings_cleaned.csv`

| Column            | Data Type | Business Definition                           |
| ----------------- | --------- | --------------------------------------------- |
| amfi_code         | INTEGER   | Mutual fund scheme code                       |
| stock_symbol      | TEXT      | Stock ticker symbol                           |
| stock_name        | TEXT      | Company / stock name                          |
| sector            | TEXT      | Sector to which the holding belongs           |
| weight_pct        | REAL      | Portfolio weight of the holding in percentage |
| market_value_cr   | REAL      | Market value of holding in crore rupees       |
| current_price_inr | REAL      | Current stock price in INR                    |
| portfolio_date    | DATE      | Portfolio reporting date                      |

## `10_benchmark_indices_cleaned.csv`

| Column      | Data Type | Business Definition                  |
| ----------- | --------- | ------------------------------------ |
| date        | DATE      | Benchmark index date                 |
| index_name  | TEXT      | Name of the benchmark index          |
| close_value | REAL      | Closing value of the benchmark index |
