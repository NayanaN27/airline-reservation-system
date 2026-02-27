# PR-13 Self Review (Issue #7: Purchase Integration Test)

## What changed and why?
- Added an integration/data test covering the customer purchase flow.
- The test performs a purchase request and verifies database side effects: a `purchases` row is created for the customer and the referenced `ticket` row exists and points to the intended flight.

## Why is this the right test layer (unit/integration/UI)?
- Purchase behavior is database-backed and involves multi-step writes, so an integration/data test is the most realistic way to catch regressions (e.g., partial writes, missing rows, broken FK relationships).

## What could still break / what’s not covered?
- Does not test login POST form behavior or UI rendering details.
- Does not cover overbooking behavior beyond the default seat check logic.
- Does not cover agent/staff booking flows.

## Risks / follow-ups
- Add coverage for login/authorization edge cases and input validation.
- Address SQLAlchemy warnings in Project 2 refactoring work.
