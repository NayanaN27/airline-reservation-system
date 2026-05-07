from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional, Set


@dataclass(frozen=True)
class StatusDecision:
    ok: bool
    message: Optional[str] = None


class FlightStatusMachine:
    """
    Small 'State' validator for flight statuses (and optional transitions).
    Centralizes allowed values + transition rules.
    """

    # Keep aligned with what your UI already uses / expects.
    ALLOWED: Set[str] = {
        "On Time",
        "Delayed",
        "Cancelled",
        "In Air",
        "Arrived",
    }

    # Transition rules (kept permissive: if current is unknown, allow any ALLOWED)
    TRANSITIONS: Dict[str, Set[str]] = {
        "On Time": {"On Time", "Delayed", "Cancelled", "In Air", "Arrived"},
        "Delayed": {"Delayed", "On Time", "Cancelled", "In Air", "Arrived"},
        "In Air": {"In Air", "Arrived"},
        "Arrived": {"Arrived"},
        "Cancelled": {"Cancelled"},
    }

    @classmethod
    def validate_transition(cls, current: Optional[str], requested: str) -> StatusDecision:
        if requested not in cls.ALLOWED:
            return StatusDecision(
                ok=False,
                message=f"Invalid status '{requested}'. Allowed: {sorted(cls.ALLOWED)}",
            )

        if not current or current not in cls.TRANSITIONS:
            return StatusDecision(ok=True)

        allowed_next = cls.TRANSITIONS[current]
        if requested not in allowed_next:
            return StatusDecision(
                ok=False,
                message=f"Invalid transition: '{current}' → '{requested}'. Allowed next: {sorted(allowed_next)}",
            )

        return StatusDecision(ok=True)