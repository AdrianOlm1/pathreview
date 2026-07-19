# Module 3 Journal — PathReview

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/50

**Issue title:** Add a `has_tests` boolean to the repo analysis output

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
When PathReview analyzes a GitHub repository, it collects metadata (language,
stars, README presence, etc.) but never reports whether the project actually
has automated tests — even though test coverage is one of the strongest signals
of a mature portfolio project. The goal is to add a `has_tests` boolean to the
repo analysis output, set by detection logic that checks for a `tests/` or
`test/` directory, a `pytest.ini`, or files matching `test_*.py`. A successful
fix surfaces this field alongside the existing metadata so the agent can factor
test coverage into its feedback. The work lives in the agent tooling layer —
specifically `agent/tools/github_tool.py`, whose `_fetch_repo_metadata` method
builds the metadata dict and already has a `_has_readme` helper I can mirror.

**Branch name:** feat/50-has-tests-detection

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger

### Selection notes — "Is this right for me?" reasoning

- **Scope is bounded and clear.** The change is a single new boolean field plus
  one detection helper, following the existing `has_readme` / `_has_readme`
  pattern already in the file. No architectural changes required.
- **Files affected are few.** Realistically just `agent/tools/github_tool.py`
  (plus a unit test). Note: the issue also lists `agent/tools/repo_analyzer.py`,
  but that file does not exist in the repo — the metadata is assembled in
  `github_tool.py`, so that is where the change belongs. Worth confirming with
  the maintainer.
- **Effort matches the estimate.** Labeled Tier 1 / "good first issue",
  estimated 2–4 hours, which fits a first contribution to a large codebase.
- **Testable.** Behavior is a deterministic boolean, easy to cover with unit
  tests using mocked GitHub API responses (fixtures pattern per CONTRIBUTING.md).
- **Dependencies understood.** Uses the same `httpx` + GitHub API approach as
  the existing README check; the main open question is which GitHub endpoint to
  use for directory/file detection (contents API vs. git tree API), which I'll
  decide during implementation.
