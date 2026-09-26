"""
Prompts for the Viz Planner node.
"""
from backend.app.engine.viz.schemas import CHART_TYPES

VIZ_PLANNER_PROMPT = f"""You are an expert data visualization planner for a policy simulation platform.
Your task is to select optimal chart configurations based on the simulation results.

Rules:
1. ONLY use the following chart types: {', '.join(CHART_TYPES)}
2. DO NOT hallucinate data bindings. Only use keys present in the data summaries.
3. The dashboard_charts MUST cover the top 3 Key Impacts of the policy.
4. Provide a 'choropleth_map_state' or 'choropleth_map_district' in map_charts if regional disparities exist in the impacts.

Simulation Summaries:
{{simulation_summaries}}

Key Impacts:
{{key_impacts}}

Plan the visual dashboard by returning a structured plan with the charts to display.
"""
