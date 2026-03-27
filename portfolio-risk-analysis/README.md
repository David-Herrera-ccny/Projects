# Portfolio Risk Analysis (Equity Portfolio)

## Overview
This project analyzes the risk characteristics of a multi-asset equity portfolio using real-time market data. Key metrics such as volatility and beta are calculated to evaluate portfolio sensitivity to market movements.

## Objective
Evaluate the risk profile of a diversified portfolio and assess how individual assets respond to different market benchmarks.

## Dataset
- Source: Yahoo Finance (yfinance API)
- Assets: AAPL, TSLA, NVDA, GOOGL, MSFT, AMZN, META
- Benchmarks: SPY (S&P 500), IWM (Russell 2000), DIA (Dow Jones)

## Methods
- Pulled historical price data using `yfinance`
- Calculated daily returns over:
  - 3-month period (short-term volatility)
  - 12-month period (beta calculation)
- Computed:
  - **Annualized volatility** using standard deviation of returns
  - **Beta** using covariance with benchmark indices
- Constructed an equally weighted portfolio

## Key Results
- High-growth assets such as NVDA and TSLA exhibited the highest volatility
- Several assets showed **beta > 1**, indicating higher sensitivity to market movements
- Differences in beta across SPY, IWM, and DIA highlight varying exposure to large-cap vs small-cap markets

## Example Output
| Ticker | Volatility | Beta (SPY) |
|--------|-----------|-----------|
| NVDA   | High      | > 1       |
| TSLA   | High      | > 1       |
| AAPL   | Moderate  | < 1       |

## Tech Stack
- Python
- Pandas, NumPy
- yfinance

## Key Skills
- Financial risk analysis
- Volatility and beta calculation
- Time-series data analysis
- Data extraction via APIs

## File
- `portfolio-risk-analysis.ipynb`

## Future Improvements
- Add Sharpe ratio and risk-adjusted returns
- Visualize volatility and beta comparisons
- Expand to portfolio-level risk metrics (covariance matrix, VaR)

## Author
David Herrera
