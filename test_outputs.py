"""
Verifier for dynamo/log-report.

Ground truth is computed independently from /app/access.log inside this file —
not imported from the agent's solution, not hardcoded — so the checks track the
actual log present at grade time instead of trusting fixed literals.

One test per instruction.md success criterion, nothing more:
  "how many requests there were"                  -> test_total_requests
  "how many distinct clients were involved"       -> test_unique_clients
  "which page was most popular"                   -> test_top_path
  "Save the report ... so it can be reviewed"     -> test_report_saved_and_reviewable
"""

import json
import re
from collections import Counter
from pathlib import Path

import pytest

ACCESS_LOG = Path("/app/access.log")
REPORT = Path("/app/report.json")


def _ground_truth():
    """Independently derive expected values from the log present at grade time."""
    total = 0
    ips = set()
    paths = Counter()
    for line in ACCESS_LOG.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        total += 1
        ips.add(line.split()[0])
        m = re.search(r'"[A-Z]+ (\S+) [^"]*"', line)
        if m:
            paths[m.group(1)] += 1
    top_path = paths.most_common(1)[0][0] if paths else None
    return total, len(ips), top_path


EXPECTED_TOTAL, EXPECTED_UNIQUE_IPS, EXPECTED_TOP_PATH = _ground_truth()


@pytest.fixture
def report():
    """Load the agent's report once for the content checks."""
    assert REPORT.is_file(), f"{REPORT} was not created"
    return json.loads(REPORT.read_text())


def test_report_saved_and_reviewable():
    """instruction.md: "Save the report as /app/report.json so it can be reviewed."
    The report must exist at the agreed path and be valid, parseable JSON."""
    assert REPORT.is_file(), f"{REPORT} was not created"
    json.loads(REPORT.read_text())  # raises if it isn't reviewable JSON


def test_total_requests(report):
    """instruction.md: "how many requests there were."
    total_requests must equal the number of requests in the log."""
    assert report["total_requests"] == EXPECTED_TOTAL


def test_unique_clients(report):
    """instruction.md: "how many distinct clients were involved."
    unique_ips must equal the number of distinct client IPs in the log."""
    assert report["unique_ips"] == EXPECTED_UNIQUE_IPS


def test_top_path(report):
    """instruction.md: "which page was most popular."
    top_path must be the most frequently requested path in the log."""
    assert report["top_path"] == EXPECTED_TOP_PATH
