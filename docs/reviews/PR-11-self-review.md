# PR-11 Self Review (Issue #5: Search Result Integration Tests)

## What changed and why?
Added integration tests for `/search_result` to protect flight search behavior using seeded test data.

## Why this is the right test layer?
The search behavior depends on the database and query filtering, so an integration test with Flask test client + seeded DB best represents real regressions.

## What’s not covered yet?
We don’t yet validate the full rendered table contents or date filtering edge cases; purchase and auth POST flows remain untested.

## Risks / follow-ups
Add integration tests for `/flight_status` and customer purchase flow, and consider reducing SQLAlchemy warnings as a later refactor.
