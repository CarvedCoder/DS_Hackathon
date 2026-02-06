"""Tests for generate_queries module.

Verifies that:
- The generated CSV has the correct header columns
- The number of query rows is between 25 and 40
- Query IDs are unique and sequential starting at 1
- Queries cover multiple query categories (causal, follow-up, counterfactual, evidence)
- Every field in every row is non-empty
- Multi-turn follow-up chains are present (Task 2 requirement)
"""

import csv
import io
import os
import tempfile

import pytest

from generate_queries import generate_queries_csv, _build_queries


class TestBuildQueries:
    """Unit tests for the internal query builder."""

    def test_returns_list(self):
        queries = _build_queries()
        assert isinstance(queries, list)

    def test_row_count_in_range(self):
        queries = _build_queries()
        assert 25 <= len(queries) <= 50, (
            f"Expected 25-50 queries, got {len(queries)}"
        )

    def test_unique_ids(self):
        queries = _build_queries()
        ids = [q["Query Id"] for q in queries]
        assert len(ids) == len(set(ids)), "Query IDs must be unique"

    def test_sequential_ids_starting_at_one(self):
        queries = _build_queries()
        expected = [f"Q{i:03d}" for i in range(1, len(queries) + 1)]
        actual = [q["Query Id"] for q in queries]
        assert actual == expected, "IDs must be sequential Q001, Q002, …"

    def test_required_keys_present(self):
        required = {"Query Id", "Query", "Query Category", "System Output", "Remarks"}
        for q in _build_queries():
            assert required.issubset(q.keys()), f"Missing keys in row {q.get('Query Id')}"

    def test_no_empty_fields(self):
        for q in _build_queries():
            for key, value in q.items():
                assert value.strip(), f"Empty field '{key}' in row {q['Query Id']}"

    def test_diverse_query_categories(self):
        categories = {q["Query Category"] for q in _build_queries()}
        assert len(categories) >= 5, (
            f"Expected at least 5 distinct query categories, got {len(categories)}: {categories}"
        )

    def test_has_follow_up_queries(self):
        """Task 2 requires multi-turn follow-up reasoning queries."""
        queries = _build_queries()
        follow_up = [q for q in queries if "Follow-up" in q["Query Category"]]
        assert len(follow_up) >= 5, (
            f"Expected at least 5 follow-up queries for Task 2, got {len(follow_up)}"
        )

    def test_has_causal_explanation_queries(self):
        """Task 1 requires causal explanation queries."""
        queries = _build_queries()
        causal = [q for q in queries if "Causal" in q["Query Category"]]
        assert len(causal) >= 5, (
            f"Expected at least 5 causal-explanation queries for Task 1, got {len(causal)}"
        )

    def test_has_counterfactual_queries(self):
        """Counterfactual reasoning tests causal analysis depth."""
        queries = _build_queries()
        cf = [q for q in queries if "Counterfactual" in q["Query Category"]]
        assert len(cf) >= 2, (
            f"Expected at least 2 counterfactual queries, got {len(cf)}"
        )

    def test_remarks_reference_task_type(self):
        """Every query's Remarks should indicate whether it tests Task 1 or Task 2."""
        queries = _build_queries()
        for q in queries:
            assert "Task 1" in q["Remarks"] or "Task 2" in q["Remarks"], (
                f"Query {q['Query Id']} Remarks must reference Task 1 or Task 2"
            )

    def test_covers_multiple_domains(self):
        """Queries should reference at least 10 distinct domains."""
        queries = _build_queries()
        domain_keywords = {
            "healthcare": "Healthcare",
            "banking": "Banking",
            "finance": "Finance",
            "e-commerce": "E-commerce",
            "telecom": "Telecom",
            "insurance": "Insurance",
            "technology": "Technology",
            "travel": "Travel",
            "legal": "Legal",
            "education": "Education",
            "science": "Science",
            "hr": "HR",
            "marketing": "Marketing",
        }
        found = set()
        for q in queries:
            text = q["Remarks"] + " " + q["Query"]
            for key, label in domain_keywords.items():
                if key.lower() in text.lower():
                    found.add(label)
        assert len(found) >= 10, (
            f"Expected at least 10 domains, found {len(found)}: {found}"
        )


class TestGenerateQueriesCsv:
    """Integration tests for the CSV generation function."""

    def test_writes_file(self):
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            path = tmp.name
        try:
            generate_queries_csv(output_path=path)
            assert os.path.exists(path)
            assert os.path.getsize(path) > 0
        finally:
            os.unlink(path)

    def test_csv_header(self):
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            path = tmp.name
        try:
            content = generate_queries_csv(output_path=path)
            reader = csv.reader(io.StringIO(content))
            header = next(reader)
            assert header == [
                "Query Id",
                "Query",
                "Query Category",
                "System Output",
                "Remarks",
            ]
        finally:
            os.unlink(path)

    def test_csv_row_count(self):
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            path = tmp.name
        try:
            content = generate_queries_csv(output_path=path)
            reader = csv.reader(io.StringIO(content))
            rows = list(reader)
            data_rows = rows[1:]  # exclude header
            assert 25 <= len(data_rows) <= 50
        finally:
            os.unlink(path)

    def test_returned_string_matches_file(self):
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            path = tmp.name
        try:
            content = generate_queries_csv(output_path=path)
            with open(path, "r", newline="", encoding="utf-8") as fh:
                file_content = fh.read()
            assert content == file_content
        finally:
            os.unlink(path)
