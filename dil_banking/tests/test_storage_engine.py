"""
Unit tests for Phase 4: High-Speed Storage Engine & Columnar Parquet Architecture.
Tests:
- SQLite FTS5 BM25 search performance
- O(1) parameter-indexed rule lookup
- Parquet export and import with cryptographic SHA-256 verification (dil.lock)
"""

import tempfile
import time
import unittest
from pathlib import Path

from dil.core.loader import PackLoader
from dil.rules.engine import RulesEngine
from dil.storage.engine import FTSStorageEngine
from dil.storage.parquet_exporter import ParquetPackExporter


class TestStorageEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pack = PackLoader.load_pack(Path("dil_banking/src/dil/domains/banking/1.0.0"))

    def test_fts_engine_indexing_and_search(self):
        engine = FTSStorageEngine()
        engine.index_pack(self.pack)

        # Warmup
        engine.search_concepts_fts("housing loan", jurisdiction="india")

        # Benchmark search speed across iterations to avoid single-tick Windows timer jitter
        latencies = []
        for _ in range(5):
            start_t = time.perf_counter()
            results = engine.search_concepts_fts("housing loan LTV ratio", jurisdiction="india")
            latencies.append((time.perf_counter() - start_t) * 1000.0)

        latency_ms = min(latencies)

        self.assertTrue(len(results) > 0)
        top_concept_id = results[0][0]
        self.assertIn("loan", top_concept_id)
        # Verify sub-5ms lookup budget
        self.assertLess(latency_ms, 5.0, f"FTS search latency {latency_ms} ms exceeded 5ms budget.")
        engine.close()

    def test_rules_engine_o1_lookup(self):
        engine = RulesEngine(self.pack.rules)

        # Parameter index should exist
        self.assertTrue(hasattr(engine, "_by_param"))
        self.assertIn("ltv_ratio", engine._by_param)
        self.assertIn("cibil_score", engine._by_param)

        # Evaluating with only cibil_score should only evaluate CIBIL rules
        res = engine.evaluate_all({"cibil_score": 750}, jurisdiction="india")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].rule_id, "RULE-IN-CIBIL-SCORE-001")
        self.assertTrue(res[0].passed)

    def test_fts_rules_parameter_indexing(self):
        engine = FTSStorageEngine()
        engine.index_pack(self.pack)

        # Test indexed rule retrieval
        rules = engine.get_rules_for_parameters(["days_past_due"], jurisdiction="india")
        rule_ids = [r.id for r in rules]
        self.assertIn("RULE-IN-IRACP-NPA-001", rule_ids)
        self.assertIn("RULE-IN-IRACP-SMA2-001", rule_ids)
        # Should NOT contain housing LTV rules
        self.assertNotIn("RULE-IN-RBI-LTV-001", rule_ids)
        engine.close()

    def test_parquet_export_and_load_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            hashes = ParquetPackExporter.export_pack(self.pack, tmp_path)

            self.assertIn("terminology.parquet", hashes)
            self.assertIn("concepts.parquet", hashes)
            self.assertIn("rules.parquet", hashes)
            self.assertTrue(hashes["concepts.parquet"].startswith("sha256:"))

            # Verify dil.lock file
            lock_file = tmp_path / "dil.lock"
            self.assertTrue(lock_file.exists())

            # Read back from Parquet
            loaded = ParquetPackExporter.load_from_parquet(tmp_path)
            self.assertEqual(len(loaded["terminology"]), len(self.pack.terminology))
            self.assertEqual(len(loaded["concepts"]), len(self.pack.concepts))
            self.assertEqual(len(loaded["rules"]), len(self.pack.rules))


if __name__ == "__main__":
    unittest.main()

