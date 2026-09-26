"""
Critic engine module for validating simulation reports.
"""
from backend.app.engine.critic.critic_node import critic
from backend.app.engine.critic.hard_limits import check_hard_limits
from backend.app.engine.critic.claim_auditor import audit_claims, CriticFeedback

__all__ = ["critic", "check_hard_limits", "audit_claims", "CriticFeedback"]
