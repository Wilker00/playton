"""Policy configuration utilities."""

from dataclasses import dataclass


@dataclass
class PolicyConfig:
    """Minimal policy configuration container."""

    policy_type: str
    backbone: str
