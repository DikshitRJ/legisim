"""Prompts for the Research Subgraph."""

SEARCH_PLANNING_PROMPT = """You are an expert policy researcher.
Given the following policy context, generate 3-5 search queries that will help find relevant facts, economic figures, and demographic data.

Policy Context:
{policy}

Output ONLY a comma-separated list of search queries."""

FACT_EXTRACTION_PROMPT = """Extract structured facts from the following page content.
Focus on numbers, economic figures, regional data, and dates relevant to policy impacts.

Content:
{content}

Format your output as a JSON list of objects, where each object contains:
- name (string)
- value (string/number)
- unit (string)
- region (string)
- source_url (string)
- as_of_date (string)"""

CONFLICT_RESOLUTION_PROMPT = """You are a data synthesis engine.
Review the following extracted facts and identify/resolve any conflicting data points.
Always prefer official government sources or reputable international bodies (e.g., World Bank, IMF).

Facts:
{facts}

Output a consolidated JSON list of assumptions to be used in the economic simulation model."""

TARGETING_PROFILE_PROMPT = """Generate a precise targeting profile based on the consolidated assumptions and the initial policy context.

Policy:
{policy}

Assumptions:
{assumptions}

Extract the target demographics, exclusion criteria, primary sector, and income bracket."""
