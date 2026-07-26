"""Tests for github_tool.py

Reproduction for issue #50: "Add a `has_tests` boolean to the repo analysis
output" (https://github.com/ascherj/pathreview/issues/50).

The GitHubTool assembles repository metadata (language, stars, has_readme, ...)
in `_fetch_repo_metadata`, but never reports whether the repository contains
automated tests. `test_output_includes_has_tests_field` documents that gap: it
mocks the GitHub API so no network is required and asserts the analysis output
exposes a `has_tests` boolean. It currently FAILS because the field is missing.
"""

from unittest.mock import MagicMock

import pytest

from agent.tools import github_tool as github_tool_module
from agent.tools.github_tool import GitHubTool


class _FakeResponse:
    """Minimal stand-in for an httpx.Response."""

    def __init__(self, status_code: int = 200, json_data: dict | None = None) -> None:
        self.status_code = status_code
        self._json_data = json_data or {}

    def json(self) -> dict:
        return self._json_data

    def raise_for_status(self) -> None:
        return None


REPO_JSON = {
    "name": "portfolio-project",
    "description": "A sample project",
    "language": "Python",
    "stargazers_count": 12,
    "forks_count": 3,
    "open_issues_count": 1,
    "pushed_at": "2026-01-01T00:00:00Z",
    "topics": ["python", "portfolio"],
    "homepage": "",
}


@pytest.mark.unit
class TestGitHubToolHasTests:
    """Reproduction + future coverage for the has_tests field (issue #50)."""

    @pytest.fixture
    def tool(self, monkeypatch: pytest.MonkeyPatch) -> GitHubTool:
        """GitHubTool with all outbound httpx calls stubbed out."""
        monkeypatch.setattr(
            github_tool_module.httpx,
            "get",
            MagicMock(return_value=_FakeResponse(200, REPO_JSON)),
        )
        # _has_readme (and any future _has_tests HEAD probes) resolve to 200.
        monkeypatch.setattr(
            github_tool_module.httpx,
            "head",
            MagicMock(return_value=_FakeResponse(200)),
        )
        return GitHubTool()

    def test_output_includes_has_tests_field(self, tool: GitHubTool) -> None:
        """The analysis output must expose a has_tests boolean.

        Reproduces issue #50 — fails today because `_fetch_repo_metadata`
        does not populate `has_tests`.
        """
        result = tool.execute({"github_username": "octocat", "repo_name": "portfolio-project"})

        assert result.success is True
        assert (
            "has_tests" in result.data
        ), "analysis output is missing the `has_tests` field (issue #50)"
        assert isinstance(result.data["has_tests"], bool)
