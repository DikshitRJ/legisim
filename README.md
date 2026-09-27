# LegiSim

**A flight simulator for policies — because a law should not be test-flown on real people first.**

Built by **Team neuro-cooked** for the *Build for Billions* hackathon (Track: Agentic AI For Billions — Autonomous workflows for public and social services), National Institute of Technology Karnataka.

---

## The Problem

Fuel gets ₹10 a litre costlier. Somewhere, a tomato gets more expensive, and nobody mentioned it in the press release.

Every policy arrives with a one-line promise and a long list of surprises. A fuel hike raises freight costs, which raises food prices, which tightens household budgets, which reduces footfall at local shops — none of which is in the announcement. The same policy also lands differently on a farmer in Vidarbha versus a software engineer in Bengaluru.

Today, "who gets hit, and when?" sits scattered across think-tank reports and expert opinion. Students, journalists, and policy teams either wait weeks for a deep study or guess — and a wrong guess about a policy touching over a billion people is expensive.

## The Solution

LegiSim puts a whole country in a browser tab. Customize a country (India first), introduce a policy, run the simulation, and watch different groups of people respond in their own way — then see how those reactions ripple across the economy and society over time.

**How it works:** Instead of simulating a billion individual people, LegiSim simulates a few hundred to a few thousand *weighted cohorts* (e.g. urban salaried households, small farmers in a region). Each cohort adjusts its spending, work, and travel using real data, simple economic models, and precedent from similar past policies. A **ripple engine** pushes the initial change through a cause-and-effect map, hop by hop — showing how big each effect is, how long it takes, and how confident the model is.

### Key Features
- **Ripple Explorer** – animated cause-and-effect chain (policy → prices → household budgets) with filters for group, topic, depth, and time
- **Time Slider** – short vs. long-term effects, including cohort adoption/acceptance lag
- **Impact Dashboard & India Map** – sliced by income, region, urban/rural, education, and duration
- **Plain-language Summary Report** – reads like a short research note
- **Evidence Drawer** – every number shows its reasoning, data, and sources, tagged as *measured*, *modelled*, or *judged*

### Who It's For
Government researchers and analysts, policy teams and think tanks comparing options before a deep study, and curious citizens and teachers. Also planned: Hindi and Kannada UI, lakh/crore number formats, and a guest mode with no sign-up required.

---

## Tech Stack

| Layer | Tools |
|---|---|
| **Frontend** | Next.js (TypeScript), Tailwind CSS, shadcn/ui, Apache ECharts (charts), React Flow (ripple graph), MapLibre GL + deck.gl (India map) |
| **Backend** | Python, FastAPI, LangGraph (pipeline orchestration: research → cohort reactions → economic step → ripple engine → report → critic check) |
| **AI Models** | Two-tier setup — a stronger model for planning/ripple links/reports, a small fast model for cohort reactions. Structured JSON I/O, model names in a single config file |
| **Data & Numbers** | NumPy, pandas, SciPy, PostgreSQL + pgvector, Redis (background jobs), government data feeds |
| **Infra & Tooling** | MongoDB, LangGraph tracing, Pytest, Playwright, Docker |

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/DikshitRJ/legisim.git
cd legisim

# Run with Docker
docker compose up --build
```

The app should then be available at `http://localhost:3000` (frontend) with the API served separately by FastAPI — check `docker-compose.yml` for exact ports and required environment variables (`.env`) if not already configured.

> **Note:** Update this section with exact env vars / ports / service names once the Docker setup is finalized.

---

## Demo & Resources

- **Demo Video:** [Add link here]
- **Pitch Deck (PPT):** [Add link here]
- **Repository:** https://github.com/DikshitRJ/legisim

---

## Team

| Member | Role |
|---|---|
| Dikshit Rishi Jain (Lead) | Backend & AI — LangGraph pipeline, cohort builder, economic model, ripple engine, API, database |
| Vaishnavi Saraf | Data collection — data gathering/cleaning, population tables, past policy library |
| Sowmiyanathan Raja | Frontend & integration — results layout, shared state, live progress streaming, dashboard sliders |
| Sayan Maity | Frontend, ideation & design — design system, UI pages, ripple graph & map visuals, demo story |
| Shreya Devendra | Evidence & validation — backtests, report review, methodology page |
