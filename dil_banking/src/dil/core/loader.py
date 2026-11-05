from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from dil.core.models import (
    ConceptItem,
    PackManifest,
    ProcessItem,
    ProcessStep,
    RelationshipItem,
    RuleItem,
    SourceItem,
    TerminologyItem,
)


class PackLoader:
    """Loads and validates structured DIL Knowledge Packs from disk."""

    @staticmethod
    def load_pack(pack_dir: Path | str) -> "LoadedPack":
        pack_path = Path(pack_dir)
        manifest_file = pack_path / "manifest.json"
        if not manifest_file.exists():
            raise FileNotFoundError(f"Missing manifest.json in pack directory: {pack_path}")

        with open(manifest_file, "r", encoding="utf-8") as f:
            m_data = json.load(f)

        manifest = PackManifest(
            pack_id=m_data["pack_id"],
            name=m_data["name"],
            version=m_data["version"],
            domain=m_data["domain"],
            publisher=m_data["publisher"],
            description=m_data["description"],
            jurisdictions=m_data.get("jurisdictions", ["global"]),
            compatibility=m_data.get("compatibility", {}),
            assets=m_data.get("assets", {}),
            release=m_data.get("release", {}),
        )

        # 1. Terminology
        terms: List[TerminologyItem] = []
        term_rel = manifest.assets.get("terminology")
        if term_rel:
            term_file = pack_path / term_rel
            if term_file.exists():
                with open(term_file, "r", encoding="utf-8") as f:
                    for item in json.load(f):
                        terms.append(TerminologyItem(**item))

        # 2. Concepts
        concepts: List[ConceptItem] = []
        conc_rel = manifest.assets.get("concepts")
        if conc_rel:
            conc_file = pack_path / conc_rel
            if conc_file.exists():
                with open(conc_file, "r", encoding="utf-8") as f:
                    for item in json.load(f):
                        concepts.append(ConceptItem(**item))

        # 3. Relationships
        relationships: List[RelationshipItem] = []
        rel_rel = manifest.assets.get("relationships")
        if rel_rel:
            rel_file = pack_path / rel_rel
            if rel_file.exists():
                with open(rel_file, "r", encoding="utf-8") as f:
                    for item in json.load(f):
                        relationships.append(RelationshipItem(**item))

        # 4. Processes
        processes: List[ProcessItem] = []
        proc_rel = manifest.assets.get("processes")
        if proc_rel:
            proc_file = pack_path / proc_rel
            if proc_file.exists():
                with open(proc_file, "r", encoding="utf-8") as f:
                    for item in json.load(f):
                        steps = [ProcessStep(**s) for s in item.get("steps", [])]
                        proc_copy = dict(item)
                        proc_copy["steps"] = steps
                        processes.append(ProcessItem(**proc_copy))

        # 5. Rules
        rules: List[RuleItem] = []
        rules_asset = manifest.assets.get("rules", {})
        if isinstance(rules_asset, dict):
            for jur_key, rel_path in rules_asset.items():
                rule_file = pack_path / rel_path
                if rule_file.exists():
                    with open(rule_file, "r", encoding="utf-8") as f:
                        for item in json.load(f):
                            rules.append(RuleItem(**item))
        elif isinstance(rules_asset, str):
            rules_dir = pack_path / rules_asset
            if rules_dir.is_dir():
                for rule_file in rules_dir.glob("*.json"):
                    with open(rule_file, "r", encoding="utf-8") as f:
                        for item in json.load(f):
                            rules.append(RuleItem(**item))

        # 6. Sources
        sources: List[SourceItem] = []
        src_rel = manifest.assets.get("sources")
        if src_rel:
            src_file = pack_path / src_rel
            if src_file.exists():
                with open(src_file, "r", encoding="utf-8") as f:
                    for item in json.load(f):
                        sources.append(SourceItem(**item))

        return LoadedPack(
            manifest=manifest,
            terminology=terms,
            concepts=concepts,
            relationships=relationships,
            processes=processes,
            rules=rules,
            sources=sources,
        )


class LoadedPack:
    def __init__(
        self,
        manifest: PackManifest,
        terminology: List[TerminologyItem],
        concepts: List[ConceptItem],
        relationships: List[RelationshipItem],
        processes: List[ProcessItem],
        rules: List[RuleItem],
        sources: List[SourceItem],
    ):
        self.manifest = manifest
        self.terminology = terminology
        self.concepts = concepts
        self.relationships = relationships
        self.processes = processes
        self.rules = rules
        self.sources = sources

        self.concepts_by_id: Dict[str, ConceptItem] = {c.id: c for c in concepts}
        self.terms_by_name: Dict[str, TerminologyItem] = {t.term.lower(): t for t in terminology}
        self.rules_by_id: Dict[str, RuleItem] = {r.id: r for r in rules}
        self.sources_by_id: Dict[str, SourceItem] = {s.source_id: s for s in sources}

