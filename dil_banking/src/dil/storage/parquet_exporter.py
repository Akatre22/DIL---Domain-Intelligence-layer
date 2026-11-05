"""
Parquet Columnar Storage Exporter and Loader for DIL (Phase 4 & Phase 5 Standards).
Provides high-performance columnar serialization for DIL knowledge packs using pyarrow.
Generates SHA-256 cryptographic hashes for enterprise dil.lock reproducibility.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
    PYARROW_AVAILABLE = True
except ImportError:
    PYARROW_AVAILABLE = False

from dil.core.loader import LoadedPack
from dil.core.models import ConceptItem, RuleItem, TerminologyItem


class ParquetPackExporter:
    """Exports and loads DIL Knowledge Packs to and from compressed Parquet files."""

    @staticmethod
    def is_available() -> bool:
        return PYARROW_AVAILABLE

    @staticmethod
    def export_pack(pack: LoadedPack, output_dir: Path | str) -> Dict[str, str]:
        """
        Exports concepts, terminology, and rules to columnar Parquet files.
        Returns a dictionary mapping asset names to their SHA-256 content hashes.
        """
        if not PYARROW_AVAILABLE:
            raise RuntimeError("pyarrow is required to export knowledge packs to Parquet format.")

        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        hashes: Dict[str, str] = {}

        # 1. Export Terminology
        term_data = {
            "term": [t.term for t in pack.terminology],
            "expansion": [t.expansion for t in pack.terminology],
            "category": [t.category for t in pack.terminology],
            "definition": [t.definition for t in pack.terminology],
            "synonyms": [json.dumps(t.synonyms) for t in pack.terminology],
        }
        term_table = pa.Table.from_pydict(term_data)
        term_file = out_path / "terminology.parquet"
        pq.write_table(term_table, term_file, compression="snappy")
        hashes["terminology.parquet"] = ParquetPackExporter._compute_sha256(term_file)

        # 2. Export Concepts
        concept_data = {
            "id": [c.id for c in pack.concepts],
            "name": [c.name for c in pack.concepts],
            "category": [c.category for c in pack.concepts],
            "definition": [c.definition for c in pack.concepts],
            "key_points": [json.dumps(c.key_points) for c in pack.concepts],
            "aliases": [json.dumps(c.aliases) for c in pack.concepts],
            "related": [json.dumps(c.related) for c in pack.concepts],
            "caveat": [c.caveat or "" for c in pack.concepts],
            "jurisdiction": [c.jurisdiction for c in pack.concepts],
        }
        concept_table = pa.Table.from_pydict(concept_data)
        concept_file = out_path / "concepts.parquet"
        pq.write_table(concept_table, concept_file, compression="snappy")
        hashes["concepts.parquet"] = ParquetPackExporter._compute_sha256(concept_file)

        # 3. Export Rules
        rules_data = {
            "id": [r.id for r in pack.rules],
            "title": [r.title for r in pack.rules],
            "category": [r.category for r in pack.rules],
            "jurisdiction": [r.jurisdiction for r in pack.rules],
            "parameter": [r.parameter for r in pack.rules],
            "operator": [r.operator for r in pack.rules],
            "threshold": [json.dumps(r.threshold) for r in pack.rules],
            "unit": [r.unit or "" for r in pack.rules],
            "on_fail": [r.on_fail for r in pack.rules],
            "description": [r.description for r in pack.rules],
            "source_id": [r.source_id for r in pack.rules],
            "applies_when": [r.applies_when or "" for r in pack.rules],
        }
        rules_table = pa.Table.from_pydict(rules_data)
        rules_file = out_path / "rules.parquet"
        pq.write_table(rules_table, rules_file, compression="snappy")
        hashes["rules.parquet"] = ParquetPackExporter._compute_sha256(rules_file)

        # 4. Write manifest lockfile (dil.lock)
        lockfile_data = {
            "pack_id": pack.manifest.pack_id,
            "version": pack.manifest.version,
            "format": "parquet",
            "compression": "snappy",
            "content_hashes": hashes,
        }
        lock_file = out_path / "dil.lock"
        with open(lock_file, "w", encoding="utf-8") as f:
            json.dump(lockfile_data, f, indent=2)

        return hashes

    @staticmethod
    def load_from_parquet(parquet_dir: Path | str) -> Dict[str, Any]:
        """Loads concepts, terms, and rules directly from Parquet files."""
        if not PYARROW_AVAILABLE:
            raise RuntimeError("pyarrow is required to load from Parquet format.")

        p_dir = Path(parquet_dir)
        results: Dict[str, Any] = {"terminology": [], "concepts": [], "rules": []}

        # 1. Read Terminology
        term_file = p_dir / "terminology.parquet"
        if term_file.exists():
            tbl = pq.read_table(term_file)
            pydict = tbl.to_pydict()
            for i in range(len(pydict["term"])):
                results["terminology"].append(
                    TerminologyItem(
                        term=pydict["term"][i],
                        expansion=pydict["expansion"][i],
                        category=pydict["category"][i],
                        definition=pydict["definition"][i],
                        synonyms=json.loads(pydict["synonyms"][i]),
                    )
                )

        # 2. Read Concepts
        concept_file = p_dir / "concepts.parquet"
        if concept_file.exists():
            tbl = pq.read_table(concept_file)
            pydict = tbl.to_pydict()
            for i in range(len(pydict["id"])):
                results["concepts"].append(
                    ConceptItem(
                        id=pydict["id"][i],
                        name=pydict["name"][i],
                        category=pydict["category"][i],
                        definition=pydict["definition"][i],
                        key_points=json.loads(pydict["key_points"][i]),
                        aliases=json.loads(pydict["aliases"][i]),
                        related=json.loads(pydict["related"][i]),
                        caveat=pydict["caveat"][i] or None,
                        jurisdiction=pydict["jurisdiction"][i],
                    )
                )

        # 3. Read Rules
        rules_file = p_dir / "rules.parquet"
        if rules_file.exists():
            tbl = pq.read_table(rules_file)
            pydict = tbl.to_pydict()
            for i in range(len(pydict["id"])):
                results["rules"].append(
                    RuleItem(
                        id=pydict["id"][i],
                        title=pydict["title"][i],
                        category=pydict["category"][i],
                        jurisdiction=pydict["jurisdiction"][i],
                        parameter=pydict["parameter"][i],
                        operator=pydict["operator"][i],
                        threshold=json.loads(pydict["threshold"][i]),
                        unit=pydict["unit"][i] or None,
                        on_fail=pydict["on_fail"][i],
                        description=pydict["description"][i],
                        source_id=pydict["source_id"][i],
                        applies_when=pydict["applies_when"][i] or None,
                    )
                )

        return results

    @staticmethod
    def _compute_sha256(file_path: Path) -> str:
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return f"sha256:{h.hexdigest()}"

