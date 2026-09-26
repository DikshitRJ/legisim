# Backtesting & Validation Plan

This document outlines the methodology for validating the LegiSim platform against known historical policies to guarantee logical rigor and empirical accuracy.

## 1. Subagent Assignment
- `test-writer`: Write the Python testing harnesses that orchestrate the backtests.
- `data-analyst`: Perform statistical comparison between simulated results and historical data.
- `copilot`: Implement custom validation and LLM evaluation criteria.

## 2. Historical Policies for Backtesting

We will use 3 historical scenarios with significant, observable impacts.

### 2.1 Demonetisation of ₹500 and ₹1,000 Banknotes (2016)
- **Policy Input**: "Invalidate ₹500 and ₹1,000 notes immediately. Allow a 50-day window to deposit old notes."
- **Data Cutoff Date**: October 31, 2016
- **Known Outcomes (Targets)**:
  - Short-term liquidity crunch (cash-in-circulation drop).
  - Temporary GDP growth slowdown (Q3/Q4 FY17).
  - Surge in digital payments (UPI, wallets).

### 2.2 Goods and Services Tax (GST) Implementation (2017)
- **Policy Input**: "Implement a comprehensive dual GST system replacing multiple cascading taxes. Slab rates at 5%, 12%, 18%, 28%."
- **Data Cutoff Date**: June 30, 2017
- **Known Outcomes (Targets)**:
  - Initial compliance bottlenecks and working capital crunches for MSMEs.
  - Gradual formalization of the economy.
  - Revenue shortfall for states initially requiring compensation cess.

### 2.3 Fuel Excise Duty Cuts (2022)
- **Policy Input**: "Cut excise duty on petrol by ₹8 and diesel by ₹6 per litre."
- **Data Cutoff Date**: May 20, 2022
- **Known Outcomes (Targets)**:
  - Direct inflation (CPI) moderation by ~0.2-0.3 percentage points.
  - Increased fiscal deficit by approximately ₹1 lakh crore annually.

## 3. Backtesting Execution Methodology

1. **Information Isolation**: Ensure the Vector DB is partitioned such that data generated *after* the `Data Cutoff Date` is completely hidden from the LLM context for that specific test run.
2. **Simulation Run**: Execute the LegiSim LangGraph pipeline for the policy input using the historical state.
3. **Monte Carlo Execution**: Run each simulation 30 times (N=30) to establish a distribution of outcomes and assess variance.

## 4. Accuracy Metrics and Acceptable Thresholds

Validation is performed by comparing the median predicted output across Monte Carlo runs to the actual historical outcome.

| Metric | Threshold / Acceptance Criteria |
|--------|---------------------------------|
| Directional Accuracy | The predicted trend (increase/decrease) matches reality >80% of the time. |
| Magnitude Variance | The predicted quantitative impact is within ±25% of the actual historical impact (e.g., predicted 0.25% inflation drop vs actual 0.2%). |
| Hallucination Rate | 0% introduction of anachronistic entities or events (e.g., citing COVID-19 in a 2017 GST simulation). |

## 5. Hard Sanity Limits & Guardrails

Embedded in the Python testing framework, the system will instantly fail a simulation step if these constraints are violated:
- **Inflation**: Cannot exceed 30% YoY dynamically without catastrophic hyperinflation triggers.
- **Fiscal Deficit**: Cannot exceed 15% of GDP in a single year under standard conditions.
- **Unemployment**: Cannot exceed 25% outside of total systemic collapse.

```python
def check_sanity_limits(simulation_state: dict):
    assert -0.05 <= simulation_state.get("inflation_rate") <= 0.30, "Inflation out of plausible bounds"
    assert simulation_state.get("unemployment_rate") <= 0.25, "Unemployment out of plausible bounds"
    # Fails test if LLM hallucinated extreme numbers
```

## 6. Expert Spot-Check Protocol

1. **Sampling**: 5% of simulated reports (both valid and out-of-bounds) are randomly sampled.
2. **Human Review**: Domain experts (economists, policy analysts) review the logical chain-of-thought of the LLM.
3. **Feedback Loop**: Errors identified by humans are converted into Few-Shot examples in the `system_prompts` database to prevent future regressions.
