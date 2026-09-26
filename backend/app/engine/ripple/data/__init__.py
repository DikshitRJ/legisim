"""Data package for Ripple Effect Engine containing static seed map assets."""

from pathlib import Path

SEED_MAP_V1_PATH: Path = Path(__file__).resolve().parent / "seed_map_v1.json"

__all__ = ["SEED_MAP_V1_PATH"]
