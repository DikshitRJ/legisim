"""
Module for handling cohort population loading and generation.
"""

import json
import glob
import os
from pathlib import Path
from typing import List, Dict, Any

def build_population() -> List[Dict[str, Any]]:
    """Loads all cohort personas from the /personas/ JSON directory."""
    # Resolve the project root assuming this file is in backend/app/engine/cohort/
    project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
    personas_dir = project_root / "personas"
    
    population = []
    
    # If directory doesn't exist, return empty
    if not personas_dir.exists():
        return population
        
    for filepath in personas_dir.glob("*.json"):
        try:
            with open(filepath, "r") as f:
                persona_data = json.load(f)
                
                # Transform to flat structure expected by the engine if needed,
                # or keep the nested structure. We flatten key variables for JEV/LangGraph convenience.
                # E.g., JEV uses region and occupation for targeting.
                
                # Normalize keys for the pipeline
                cohort = {
                    "cohort_id": persona_data.get("id", filepath.stem),
                    "region": persona_data.get("demographics", {}).get("region", "Unknown"),
                    "occupation": persona_data.get("demographics", {}).get("occupation", "Unknown"),
                    "income_band": persona_data.get("demographics", {}).get("income_band", "Unknown"),
                    "spend_mix": persona_data.get("spend_mix", {}),
                    "trust_in_govt": persona_data.get("trust_in_govt", 0.5),
                    "ideological_lean": persona_data.get("ideological_lean", 0.5),
                    "agreeableness_lean": persona_data.get("agreeableness", 0.5),
                    "weight": persona_data.get("weight", 1.0),
                    "size": persona_data.get("size", 1000)
                }
                population.append(cohort)
        except Exception as e:
            print(f"Error loading persona {filepath}: {e}")
            
    return population
