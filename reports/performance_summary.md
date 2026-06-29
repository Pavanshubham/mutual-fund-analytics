# Mutual Fund Performance Analytics Summary

## Project Overview

This report summarizes the performance analytics conducted on 40 mutual fund schemes using historical NAV data (2022–2026). Various financial metrics were calculated to evaluate fund performance, risk, and consistency.

---

# Performance Metrics Calculated

## 1. Daily Returns

Daily returns were calculated using the percentage change in NAV.

Formula:

Daily Return = (NAV_today / NAV_yesterday) - 1

The return distribution appeared approximately normal with occasional extreme market movements corresponding to periods of high volatility.

---

## 2. Compound Annual Growth Rate (CAGR)

CAGR was computed for the following investment horizons:

* 1 Year
* 3 Years
* 5 Years

Formula:

CAGR = (Ending NAV / Beginning NAV)^(1/n) - 1

This metric measures the annualized growth rate assuming returns are compounded.

---

## 3. Sharpe Ratio

Risk-adjusted performance was measured using the Sharpe Ratio.

Formula:

Sharpe = (Portfolio Return − Risk-Free Rate) / Portfolio Volatility × √252

Risk-Free Rate Assumed:

6.5%

Funds with higher Sharpe Ratios demonstrated superior return generation relative to their overall risk.

---

## 4. Sortino Ratio

Unlike the Sharpe Ratio, the Sortino Ratio penalizes only downside volatility.

Formula:

Sortino = (Portfolio Return − Risk-Free Rate) / Downside Standard Deviation × √252

This metric better reflects downside investment risk.

---

## 5. Alpha & Beta

Alpha and Beta were estimated using Ordinary Least Squares (OLS) regression against the NIFTY 100 benchmark.

Alpha measures excess annualized return beyond benchmark expectations.

Beta measures market sensitivity.

Interpretation:

* Beta > 1 : More volatile than benchmark
* Beta < 1 : Less volatile than benchmark
* Positive Alpha : Outperformed benchmark
* Negative Alpha : Underperformed benchmark

---

## 6. Maximum Drawdown

Maximum Drawdown measures the largest historical decline from a portfolio peak.

Formula:

Drawdown = NAV / Running Maximum NAV − 1

Lower drawdowns indicate better downside protection.

---

## 7. Composite Fund Score

Each mutual fund received an overall score between 0 and 100 based on the following weighted metrics:

| Metric                          | Weight |
| ------------------------------- | ------ |
| 3-Year CAGR Rank                | 30%    |
| Sharpe Ratio Rank               | 25%    |
| Alpha Rank                      | 20%    |
| Expense Ratio Rank (Inverse)    | 15%    |
| Maximum Drawdown Rank (Inverse) | 10%    |

The resulting Fund Score enables easy ranking of schemes based on return, consistency, risk-adjusted performance, cost efficiency, and downside protection.

---

# Benchmark Comparison

The top-performing mutual funds were compared against:

* NIFTY 50
* NIFTY 100

Performance comparison included:

* Normalized NAV Growth
* Tracking Error
* Relative Outperformance
* Volatility Comparison

---

# Key Findings

• Most equity schemes generated positive long-term CAGR over the analysis period.

• Higher Sharpe Ratios generally corresponded with stronger long-term fund performance.

• Funds with lower expense ratios consistently ranked higher in composite scoring.

• Maximum Drawdown varied considerably across schemes, highlighting differences in downside risk management.

• Alpha values identified funds that generated returns beyond benchmark expectations.

• Benchmark comparison showed that several actively managed funds outperformed market indices over the three-year period.

---

# Deliverables Generated

* Performance_Analytics.ipynb
* alpha_beta.csv
* fund_scorecard.csv
* benchmark_comparison.png
* performance_summary.md

---

# Conclusion

This performance analytics study demonstrates a complete quantitative evaluation framework for mutual fund analysis. The combination of return-based metrics, risk-adjusted measures, regression analysis, and composite scoring provides investors with a comprehensive assessment of fund quality and investment potential.
