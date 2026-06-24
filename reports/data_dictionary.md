# Data Dictionary – Mutual Fund Analytics Project

## 1. dim_fund

Source: `01_fund_master_cleaned.csv`

| Column             | Data Type | Business Definition                                                          |
| ------------------ | --------- | ---------------------------------------------------------------------------- |
| amfi_code          | INTEGER   | Unique AMFI scheme code identifying each mutual fund scheme                  |
| fund_house         | TEXT      | Mutual fund company / AMC name                                               |
| scheme_name        | TEXT      | Name of the mutual fund scheme                                               |
| category           | TEXT      | High-level scheme category such as Equity, Debt, Hybrid                      |
| sub_category       | TEXT      | Detailed fund classification such as Large Cap, Flexi Cap, Liquid Fund       |
| plan               | TEXT      | Scheme plan type such as Direct or Regular                                   |
| launch_date        | DATE      | Date on which the scheme was launched                                        |
| benchmark          | TEXT      | Benchmark index used for scheme performance comparison                       |
| expense_ratio_pct  | REAL      | Annual expense ratio charged by the fund                                     |
| exit_load_pct      | REAL      | Exit load percentage charged on redemption before a specified holding period |
| min_sip_amount     | INTEGER   | Minimum SIP investment amount allowed for the scheme                         |
| min_lumpsum_amount | INTEGER   | Minimum lumpsum investment amount allowed for the scheme                     |
| fund_manager       | TEXT      | Name of the fund manager handling the scheme                                 |
| risk_category      | TEXT      | Risk classification of the scheme                                            |
| sebi_category_code | TEXT      | SEBI-defined category code for the scheme                                    |

---

## 2. dim_date

Generated from all cleaned date columns across datasets

| Column       | Data Type | Business Definition               |
| ------------ | --------- | --------------------------------- |
| full_date    | DATE      | Calendar date used in fact tables |
| year         | INTEGER   | Calendar year                     |
| quarter      | INTEGER   | Calendar quarter (1 to 4)         |
| month        | INTEGER   | Month number (1 to 12)            |
| month_name   | TEXT      | Month name                        |
| day          | INTEGER   | Day of month                      |
| weekday_name | TEXT      | Day name such as Monday, Tuesday  |

---

## 3. fact_nav

Source: `02_nav_history_cleaned.csv`

| Column    | Data Type | Business Definition                        |
| --------- | --------- | ------------------------------------------ |
| amfi_code | INTEGER   | Mutual fund scheme code                    |
| nav_date  | DATE      | Date on which NAV was recorded             |
| nav       | REAL      | Net Asset Value of the scheme on that date |

---

## 4. fact_transactions

Source: `08_investor_transactions_cleaned.csv`

| Column             | Data Type | Business Definition                                     |
| ------------------ | --------- | ------------------------------------------------------- |
| investor_id        | TEXT      | Unique identifier for an investor                       |
| transaction_date   | DATE      | Date of investment or redemption transaction            |
| amfi_code          | INTEGER   | Mutual fund scheme code associated with the transaction |
| transaction_type   | TEXT      | Transaction type such as SIP, Lumpsum, or Redemption    |
| amount_inr         | REAL      | Transaction amount in Indian Rupees                     |
| state              | TEXT      | Investor state                                          |
| city               | TEXT      | Investor city                                           |
| city_tier          | TEXT      | Tier classification of investor city                    |
| age_group          | TEXT      | Investor age bucket                                     |
| gender             | TEXT      | Investor gender                                         |
| annual_income_lakh | REAL      | Investor annual income in lakhs                         |
| payment_mode       | TEXT      | Payment method such as UPI, Net Banking, Cheque         |
| kyc_status         | TEXT      | KYC verification status of investor                     |

---

## 5. fact_performance

Source: `07_scheme_performance_cleaned.csv`

| Column             | Data Type | Business Definition                                 |
| ------------------ | --------- | --------------------------------------------------- |
| amfi_code          | INTEGER   | Mutual fund scheme code                             |
| return_1yr_pct     | REAL      | Scheme return over the last 1 year in percentage    |
| return_3yr_pct     | REAL      | Scheme return over the last 3 years in percentage   |
| return_5yr_pct     | REAL      | Scheme return over the last 5 years in percentage   |
| benchmark_3yr_pct  | REAL      | Benchmark return over the last 3 years              |
| alpha              | REAL      | Alpha value indicating excess return over benchmark |
| beta               | REAL      | Beta value indicating volatility relative to market |
| sharpe_ratio       | REAL      | Risk-adjusted return metric                         |
| sortino_ratio      | REAL      | Downside-risk-adjusted return metric                |
| std_dev_ann_pct    | REAL      | Annualized standard deviation of returns            |
| max_drawdown_pct   | REAL      | Maximum peak-to-trough fall in scheme value         |
| aum_crore          | REAL      | Assets under management for the scheme in crore     |
| expense_ratio_pct  | REAL      | Annual expense ratio charged by the scheme          |
| morningstar_rating | INTEGER   | Morningstar star rating of the scheme               |
| risk_grade         | TEXT      | Risk grade label of the scheme                      |

---

## 6. fact_aum

Source: `03_aum_by_fund_house_cleaned.csv`

| Column         | Data Type | Business Definition                         |
| -------------- | --------- | ------------------------------------------- |
| aum_date       | DATE      | Reporting date for AUM                      |
| fund_house     | TEXT      | Mutual fund house / AMC name                |
| aum_lakh_crore | REAL      | Assets under management in lakh crore       |
| aum_crore      | REAL      | Assets under management in crore rupees     |
| num_schemes    | INTEGER   | Number of schemes offered by the fund house |
