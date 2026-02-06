"""Tests for generate_queries module.

Verifies that:
- The generated CSV has the correct header columns
- The number of query rows is between 25 and 40
- Query IDs are unique and sequential starting at 1
- Diverse domains are represented
- Every field in every row is non-empty
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
        assert 25 <= len(queries) <= 40, (
            f"Expected 25-40 queries, got {len(queries)}"
        )

    def test_unique_ids(self):
        queries = _build_queries()
        ids = [q["Query Id"] for q in queries]
        assert len(ids) == len(set(ids)), "Query IDs must be unique"

    def test_sequential_ids_starting_at_one(self):
        queries = _build_queries()
        expected = [str(i) for i in range(1, len(queries) + 1)]
        actual = [q["Query Id"] for q in queries]
        assert actual == expected, "IDs must be sequential starting at 1"

    def test_required_keys_present(self):
        required = {"Query Id", "Query", "Query Category", "System Output", "Remarks"}
        for q in _build_queries():
            assert required.issubset(q.keys()), f"Missing keys in row {q.get('Query Id')}"

    def test_no_empty_fields(self):
        for q in _build_queries():
            for key, value in q.items():
                assert value.strip(), f"Empty field '{key}' in row {q['Query Id']}"

    def test_diverse_categories(self):
        categories = {q["Query Category"] for q in _build_queries()}
        assert len(categories) >= 8, (
            f"Expected at least 8 distinct categories, got {len(categories)}: {categories}"
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
            assert 25 <= len(data_rows) <= 40
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
