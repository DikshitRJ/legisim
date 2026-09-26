# LegiSim Prototype: Demo Video Workflow Guide

This document outlines the step-by-step workflow to record a highly coherent and impressive demo video using the current hardcoded prototype. 

Because the prototype's output data is hardcoded to a specific scenario—**Fuel Price Deregulation (Diesel Subsidy Removal)**—you must input the corresponding parameters during the setup phase so that the generated output feels like a magical, direct result of your inputs.

---

## 🎯 The Demo Scenario: Diesel Subsidy Removal
**Objective**: Show how LegiSim simulates 1st, 2nd, and 3rd-order socio-economic impacts of removing diesel subsidies across different demographics.

### Preparation
1. Ensure the development server is running (`npm run dev`).
2. Open the app in your browser at `http://localhost:3000/notebooks`.
3. Set your screen recording software to capture the browser window cleanly.

---

## 🎬 Step-by-Step Recording Workflow

### 1. The Notebooks Dashboard (`/notebooks`)
* **Action**: Start recording here. 
* **Talking Track**: *"Welcome to LegiSim. Here is our central dashboard where policymakers manage their analysis workspaces. We have some historical notebooks, but today we are going to evaluate a new, highly sensitive policy: the complete removal of diesel subsidies."*
* **Action**: Click the big orange **`+ ADD NOTEBOOK`** button.

### 2. Simulation Configuration / Setup Wizard (`/notebooks/[id]/new`)
This is the most critical step. You need to make selections that logically lead to the hardcoded data waiting on the next screens.

* **Talking Track**: *"First, we define our target demographic cohorts and feed the policy parameters into the simulation engine."*
* **Actions (Select the following pills)**:
  * **Population & Age Groups**: Select `Active Productive (25-59)` and `Elderly (60+)`.
  * **Income Groups**: Select `Wealth Quintiles` and `Household Amenities Access`.
  * **Occupations**: Select `Cultivators`, `Agricultural Labourers`, and `Other Workers` (to represent truck drivers).
  * **Urban vs. Rural**: Select `Rural Revenue Villages` and `Statutory Towns`.
* **Policy Notes (CRITICAL)**: Type the following text *exactly* into the text area. This matches the hardcoded output perfectly:
  > **"Evaluate the socio-economic and ripple effects of Fuel Price Deregulation, specifically the complete removal of diesel subsidies with a phased implementation over 6 months."**
* **Action**: Click **`Proceed / Save Cohort`**.

### 3. The "AI Processing" Loading Screen (`/runs/demo-run-1/loading`)
* **Talking Track**: *"LegiSim's engine is now ingesting census data, overlaying our selected cohorts, and running a multi-layered simulation to predict the outcomes of this subsidy removal."*
* **Action**: Let the loading animations play out. It automatically transitions to the dashboard.

### 4. The Executive Dashboard (`/runs/demo-run-1/dashboard`)
* **Action**: Pause briefly to let the viewer take in the metrics.
* **Talking Track**: *"Here are the macro-level predictions. We see substantial fiscal savings of ₹1.3L Crores, but it comes at a heavy socio-economic cost: an average household income drop of 4.2%, a 6.3% spike in cost of living, and over 2 million jobs affected."*

### 5. Detailed Summary & Recommendations (`/runs/demo-run-1/summary`)
* **Action**: Navigate to the **Summary** tab using the left sidebar.
* **Talking Track**: *"The AI has generated a comprehensive breakdown. Notice how it picked up our 6-month phased implementation from the prompt, and correctly identified that low-income rural households will face a disproportionate burden due to transport costs."*

### 6. Demographic Group Breakdown (`/runs/demo-run-1/groups`)
* **Action**: Navigate to the **Groups** tab.
* **Talking Track**: *"Because we selected specific cohorts like Cultivators and Urban populations, the engine isolated their unique impacts. Rural Farmers are facing a severe 12.4% income drop and are predicted to shift to manual labor, while the Urban Middle Class absorbs the shock better at just a 3.1% drop, shifting towards public transport."*

### 7. The Ripple Effects Engine (`/runs/demo-run-1/ripple`)
* **Action**: Navigate to the **Ripple** tab.
* **Talking Track**: *"This is LegiSim's systems-thinking at work. Removing the subsidy (Layer 0) directly spikes transport and agricultural input costs (Layer 1). This cascades into food price increases and rural income decline (Layer 2), eventually leading to macro-economic inflation and high risk of political backlash (Layer 3). It maps out the unintended consequences before the policy is even drafted."*

### 8. Wrap Up
* **Action**: You can briefly click on **Time** or **Map** to show that temporal and spatial data is also generated.
* **Talking Track**: *"With LegiSim, policymakers move from guesswork to high-confidence, data-driven decisions."*
* **Action**: Stop recording.

---

## 🛠️ How to Change the Demo Topic (Optional)
If you want to record a demo about a **different policy** (e.g., "Farmer Loan Waiver" instead of "Diesel Subsidy"), you must modify the hardcoded data files before recording:

1. **`src/data/mockResults.ts`**: Update the `policyTitle`, `policyDescription`, metrics, chart data, and summary paragraphs to match your new policy.
2. **`src/data/mockRipple.ts`**: Update the nodes and edges to reflect the cascading effects of your new policy.
3. **`src/data/mockGroups.ts`**: Update the specific cohorts affected, their income changes, and predicted behaviors.
4. **`src/data/mockNotebooks.ts`**: (Optional) Update the mock list on the home screen.
