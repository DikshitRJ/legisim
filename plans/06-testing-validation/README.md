# Testing and Validation Strategy

This directory contains the comprehensive testing, validation, and Continuous Integration/Continuous Deployment (CI/CD) plans for the LegiSim project. 

LegiSim is a complex system involving LLM orchestration, vector databases, and real-time streaming interfaces. Traditional unit and integration testing must be augmented with robust validation against historical policies (backtesting) to ensure the system produces reliable, grounded simulations.

## Table of Contents

1. [Backtesting & Validation Strategy](./01-backtesting/plan.md)
   - Methodology for validating simulation accuracy using historical policies (Demonetisation, GST, etc.).
   - Metrics for evaluating predictions against actual macroeconomic outcomes.
   - Guardrails and sanity limits.

2. [Integration & Automated Testing](./02-integration-tests/plan.md)
   - Standard automated testing layers.
   - Frontend: Jest, React Testing Library, Playwright.
   - Backend: Pytest, httpx for API tests, mock LangGraph pipelines.
   - Database and SSE streaming tests.

3. [CI/CD Pipeline](./03-ci-cd/plan.md)
   - GitHub Actions workflows for continuous integration.
   - Code quality checks (mypy, Ruff, ESLint).
   - Automated test execution.
   - Docker image builds and deployment strategies.

## Guiding Principles

- **Deterministic Testing Where Possible**: LLMs introduce non-determinism. Standard automated tests will mock LLM responses to ensure test reliability.
- **Probabilistic Validation Where Necessary**: The core simulation logic will be tested via statistical backtesting over multiple Monte Carlo runs.
- **Fail Fast CI/CD**: Quick code quality checks before spinning up heavy testing environments.
