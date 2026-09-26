"""Prompts for Ripple AI Proposer."""

RIPPLE_PROPOSAL_PROMPT = """
You are an expert policy simulator and systems thinker.
Given the following policy, existing seed graph, research facts, and historical analogues, 
propose NEW causal edges (up to 5) that represent likely downstream effects not yet captured.

Policy:
{policy}

Seed Graph:
{seed_map}

Research Facts:
{research_facts}

Historical Analogues:
{analogues}

Rules for new edges:
1. Must not create a duplicate edge.
2. Must not create a self-loop.
3. Strength must be between -1.0 and 1.0.
4. Mechanism must clearly explain the causal link.
5. Identify or propose target nodes with correct domains.
6. Target nodes must be valid JSON objects with id, label, domain, kind.
"""
