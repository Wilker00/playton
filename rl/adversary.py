"""Adversarial scenario generator."""

from dataclasses import dataclass
from typing import List


@dataclass
class Perturbation:
    """Representation of a stress scenario."""

    name: str
    severity: float


def list_default_perturbations() -> List[Perturbation]:
    """Return a list of default perturbations."""
    return [
        Perturbation(name="gaussian_noise", severity=0.1),
        Perturbation(name="latency_spike", severity=0.2),
        Perturbation(name="liquidity_crunch", severity=0.3),
    ]
