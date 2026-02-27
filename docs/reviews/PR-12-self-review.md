# PR-12 Self Review (Issue #6: Flight Status Integration Tests)

## What changed and why?
- Added integration tests for the `/flight_status` endpoint using Flask’s test client.
- Covered two cases: a known seeded flight returns a status (“On Time”), and an unknown flight does not crash and behaves gracefully.
- Added a DB assertion to confirm the seeded flight exists and matches the expected status, reducing brittleness if the HTML format changes.

## Why is this the right test layer (unit/integration/UI)?
- The flight status feature depends on database queries and template rendering, so an integration test (Flask client + real DB) best represents real regressions.
- Unit tests alone wouldn’t catch issues in query filtering, template rendering, or database wiring.

## What could still break / what’s not covered?
- We don’t yet assert the full content/format of the status table (cities/times) beyond key indicators.
- Date filtering edge cases (invalid date format, missing partial parameters) are not covered.
- Staff/agent status update routes are not covered.

## Risks / follow-ups
- Address SQLAlchemy warnings (relationship overlaps and legacy `Query.get()` usage) in Project 2 refactoring work.
- Add tests for invalid input (bad date strings) and partial parameter combinations.
- Expand coverage for `/search_result` date boundary conditions and for customer purchase flows.
