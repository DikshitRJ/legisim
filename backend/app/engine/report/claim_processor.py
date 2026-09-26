"""
Claim processor for the LegiSim Report Writer.
"""
import re
from typing import Any, Dict, List, Tuple

CLAIM_PATTERN = re.compile(r'\[claim_(\d{2,3})\]')

def extract_claims_from_markdown(markdown: str, section_id: str) -> List[Tuple[str, str]]:
    """Extract claims from markdown text. Returns list of (claim_id, sentence)."""
    claims = []
    sentences = re.split(r'(?<=[.!?])\s+', markdown)
    for sentence in sentences:
        matches = CLAIM_PATTERN.findall(sentence)
        for match in matches:
            claims.append((match, sentence.strip()))
    return claims

def match_claim_to_source(
    sentence: str,
    metrics: Dict[str, Any],
    ripple: Dict[str, Any],
    reactions: Dict[str, Any],
    analogues: List[Any]
) -> Tuple[str, str, float]:
    """
    Match claim to source.
    Returns (source_type, source_ref, confidence).
    Priority: measured > modelled > judged > fallback
    """
    sentence_lower = sentence.lower()
    
    if any(m.lower() in sentence_lower for m in metrics.keys()):
        return ("measured", "metrics_data", 0.9)
    if "ripple" in sentence_lower or "effect" in sentence_lower:
        return ("modelled", "ripple_network", 0.8)
    if "reaction" in sentence_lower or "stance" in sentence_lower:
        return ("judged", "reaction_engine", 0.7)
        
    return ("fallback", "general_context", 0.5)

def build_claim_registry(
    sections: List[Dict[str, Any]],
    metrics: Dict[str, Any],
    ripple: Dict[str, Any],
    reactions: Dict[str, Any],
    analogues: List[Any]
) -> List[Dict[str, Any]]:
    """Build registry of all claims in the report."""
    registry = []
    
    for section in sections:
        section_id = section.get("id", "")
        content = section.get("content", "")
        claims = extract_claims_from_markdown(content, section_id)
        
        for claim_id, sentence in claims:
            source_type, source_ref, confidence = match_claim_to_source(
                sentence, metrics, ripple, reactions, analogues
            )
            registry.append({
                "claim_id": claim_id,
                "section_id": section_id,
                "text": sentence,
                "source_type": source_type,
                "source_ref": source_ref,
                "confidence": confidence
            })
            
    return registry
