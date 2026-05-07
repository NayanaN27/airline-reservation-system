# app/auth/access.py
from __future__ import annotations

from dataclasses import dataclass
from functools import wraps
from typing import Callable, Optional, Protocol, Tuple

from flask import current_app, flash, redirect, session, url_for


@dataclass(frozen=True)
class AccessDecision:
    allowed: bool
    redirect_endpoint: str = "auth.login"
    flash_message: Optional[str] = None
    flash_category: str = "danger"


class AccessPolicy(Protocol):
    """Role-specific rules. Keep this tiny and behavior-preserving."""
    def evaluate(self) -> AccessDecision: ...


class CustomerPolicy:
    def evaluate(self) -> AccessDecision:
        if session.get("user_type") != "customer":
            return AccessDecision(allowed=False)
        return AccessDecision(allowed=True)


class StaffPolicy:
    def evaluate(self) -> AccessDecision:
        if session.get("user_type") != "staff":
            return AccessDecision(allowed=False)
        return AccessDecision(allowed=True)


class AgentPolicy:
    def evaluate(self) -> AccessDecision:
        if session.get("user_type") != "agent":
            return AccessDecision(allowed=False)

        # Preserve existing behavior: agent must be approved.
        connection = current_app.config["GET_DB"]()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                SELECT approved
                FROM booking_agent
                WHERE email = %s
                """,
                (session.get("user"),),
            )
            result = cursor.fetchone()
            if not result or not result.get("approved"):
                return AccessDecision(
                    allowed=False,
                    flash_message="Your account is pending approval. Please contact airline staff.",
                )
        finally:
            cursor.close()
            connection.close()

        return AccessDecision(allowed=True)


def require_access(policy: AccessPolicy) -> Callable:
    """Decorator factory to enforce access using a policy strategy."""
    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            decision = policy.evaluate()
            if decision.allowed:
                return view_func(*args, **kwargs)

            if decision.flash_message:
                flash(decision.flash_message, decision.flash_category)

            return redirect(url_for(decision.redirect_endpoint))

        return wrapper
    return decorator