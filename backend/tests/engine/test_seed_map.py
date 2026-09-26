"""Tests for the initial hand-built Ripple Seed Map JSON (seed_map_v1.json).

Validates schema constraints, node and edge counts, domain coverage,
and required causal chain paths for LegiSim's Indian economy model.
"""

import json
from pathlib import Path
import re
import pytest

SEED_MAP_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "app"
    / "engine"
    / "ripple"
    / "data"
    / "seed_map_v1.json"
)


@pytest.fixture(scope="module")
def seed_map():
    """Load and return the parsed seed map JSON."""
    assert SEED_MAP_PATH.exists(), f"Seed map file not found at {SEED_MAP_PATH}"
    with open(SEED_MAP_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def test_seed_map_structure(seed_map):
    """Verify version, nodes, and edges keys exist."""
    assert "version" in seed_map
    assert seed_map["version"] == 1
    assert "nodes" in seed_map
    assert "edges" in seed_map
    assert isinstance(seed_map["nodes"], list)
    assert isinstance(seed_map["edges"], list)


def test_seed_map_counts(seed_map):
    """Verify minimum 100 nodes and 200 edges requirements."""
    nodes = seed_map["nodes"]
    edges = seed_map["edges"]
    assert len(nodes) >= 100, f"Expected at least 100 nodes, got {len(nodes)}"
    assert len(edges) >= 200, f"Expected at least 200 edges, got {len(edges)}"


def test_seed_map_nodes_valid(seed_map):
    """Verify each node has correct schema, snake_case ID, and reasonable fields."""
    slug_regex = re.compile(r"^[a-z0-9_]+$")
    node_ids = set()

    required_domains = {
        "energy",
        "transport",
        "agriculture",
        "consumer",
        "income",
        "employment",
        "economy",
        "fiscal",
        "social",
        "political",
        "health",
        "business",
    }
    found_domains = set()

    for node in seed_map["nodes"]:
        nid = node.get("id")
        assert nid, f"Node missing ID: {node}"
        assert slug_regex.match(nid), f"Node ID must be snake_case slug: {nid}"
        assert nid not in node_ids, f"Duplicate node ID: {nid}"
        node_ids.add(nid)

        assert "label" in node and isinstance(node["label"], str) and len(node["label"]) > 0
        assert "domain" in node and isinstance(node["domain"], str)
        found_domains.add(node["domain"])

        assert "unit" in node and isinstance(node["unit"], str) and len(node["unit"]) > 0
        assert "baseline_value" in node and isinstance(node["baseline_value"], (int, float))
        assert "description" in node and isinstance(node["description"], str) and len(node["description"]) >= 10

    # Ensure all target domains are present
    assert required_domains.issubset(found_domains), f"Missing domains: {required_domains - found_domains}"


def test_seed_map_edges_valid(seed_map):
    """Verify each edge has valid source/target, bounds, mechanisms, and citations."""
    node_ids = {node["id"] for node in seed_map["nodes"]}
    edge_pairs = set()

    for edge in seed_map["edges"]:
        src = edge.get("source")
        tgt = edge.get("target")

        assert src in node_ids, f"Source '{src}' not in nodes list"
        assert tgt in node_ids, f"Target '{tgt}' not in nodes list"
        assert src != tgt, f"Self-loop detected: {src} -> {tgt}"

        pair = (src, tgt)
        assert pair not in edge_pairs, f"Duplicate edge: {src} -> {tgt}"
        edge_pairs.add(pair)

        # Strength between -1.0 and 1.0
        strength = edge.get("strength")
        assert isinstance(strength, (int, float))
        assert -1.0 <= strength <= 1.0, f"Strength out of bounds: {strength} on {pair}"

        # Lag months between 0 and 24
        lag = edge.get("lag_months")
        assert isinstance(lag, int)
        assert 0 <= lag <= 24, f"Lag months out of bounds: {lag} on {pair}"

        # Mechanism explanation
        mech = edge.get("mechanism")
        assert isinstance(mech, str) and len(mech) >= 15, f"Mechanism too short: {pair}"

        # Source citation
        citation = edge.get("source_citation")
        assert isinstance(citation, str) and len(citation) >= 3, f"Citation missing: {pair}"

        # Confidence
        confidence = edge.get("confidence")
        assert confidence in ["high", "medium", "low"], f"Invalid confidence: {confidence}"

        # Feedback & damping
        is_fb = edge.get("is_feedback")
        assert isinstance(is_fb, bool)
        damping = edge.get("damping")
        assert isinstance(damping, (int, float))
        assert 0.0 <= damping <= 1.0
        if is_fb:
            assert damping > 0.0, f"Feedback edge {pair} must have damping > 0"


def test_seed_map_no_isolated_nodes(seed_map):
    """Ensure no node is disconnected from the causal graph."""
    node_ids = {node["id"] for node in seed_map["nodes"]}
    connected_nodes = set()

    for edge in seed_map["edges"]:
        connected_nodes.add(edge["source"])
        connected_nodes.add(edge["target"])

    isolated = node_ids - connected_nodes
    assert len(isolated) == 0, f"Found isolated nodes: {isolated}"


def test_seed_map_key_causal_chains(seed_map):
    """Verify all 10 key transmission channels specified in requirements exist."""
    edge_pairs = {(e["source"], e["target"]) for e in seed_map["edges"]}

    required_chains = [
        # 1. fuel_price → freight_cost → food_basket_cost → cpi_inflation
        ("fuel_price", "freight_cost", "food_basket_cost", "cpi_inflation"),
        # 2. fuel_price → agri_input_cost → farm_income → rural_wage
        ("fuel_price", "agri_input_cost", "farm_income", "rural_wage"),
        # 3. fuel_price → public_transit_fare → commute_cost → urban_salary
        ("fuel_price", "public_transit_fare", "commute_cost", "urban_salary"),
        # 4. interest_rate → bank_lending → manufacturing_jobs
        ("interest_rate", "bank_lending", "manufacturing_jobs"),
        # 5. gst_collection → tax_revenue → govt_spending → capital_expenditure
        ("gst_collection", "tax_revenue", "govt_spending", "capital_expenditure"),
        # 6. subsidy_expenditure → fiscal_deficit → interest_rate
        ("subsidy_expenditure", "fiscal_deficit", "interest_rate"),
        # 7. rural_wage → food_basket_cost
        ("rural_wage", "food_basket_cost"),
        # 8. cpi_inflation → interest_rate
        ("cpi_inflation", "interest_rate"),
        # 9. exchange_rate → fuel_price
        ("exchange_rate", "fuel_price"),
        # 10. farm_income → migration_rate
        ("farm_income", "migration_rate"),
    ]

    for chain in required_chains:
        for i in range(len(chain) - 1):
            src, tgt = chain[i], chain[i + 1]
            assert (src, tgt) in edge_pairs, f"Missing required causal link: {src} -> {tgt} in chain {' -> '.join(chain)}"
