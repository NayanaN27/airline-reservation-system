# PR-9 Self Review

## What changed and why?
- Added a pytest harness (tests/ + conftest fixtures) and three smoke tests for `/`, `/login`, and `/flight_status`.
- Installed/recorded the `cryptography` dependency required for PyMySQL when connecting to MySQL 8 (caching_sha2_password).

## Why is this the right test layer (unit/integration/UI)?
- These are lightweight integration/smoke tests using Flask’s test client.
- They protect core routing/template/DB wiring without brittle UI automation.

## What could still break / what’s not covered?
- No assertions on detailed page content beyond successful HTTP responses.
- No coverage yet for flight search (`/search_result`), authentication POST flows, or purchases.
- Tests currently assume a reachable local MySQL with expected credentials/data.

## Risks / follow-ups
- Add `pytest.ini` to remove the need for `PYTHONPATH=.` when running tests.
- Add automated DB reset/seed for deterministic integration tests.
- Add regression tests for `/search_result` and `/flight_status` with seeded flight data.
