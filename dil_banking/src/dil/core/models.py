from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PackManifest:
    pack_id: str
    name: str
    version: str
    domain: str
    publisher: str
    description: str
    jurisdictions: List[str]
    compatibility: Dict[str, str]
    assets: Dict[str, Any]
    release: Dict[str, str]


@dataclass
class TerminologyItem:
    term: str
    expansion: str
    category: str
    definition: str
    synonyms: List[str] = field(default_factory=list)


@dataclass
class ConceptItem:
    id: str
    name: str
    category: str
    definition: str
    key_points: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    related: List[str] = field(default_factory=list)
    caveat: Optional[str] = None
    jurisdiction: str = "global"


@dataclass
class RelationshipItem:
    source: str
    relation: str
    target: str
    description: str


@dataclass
class ProcessStep:
    step_number: int
    name: str
    description: str


@dataclass
class ProcessItem:
    id: str
    name: str
    category: str
    description: str
    steps: List[ProcessStep] = field(default_factory=list)


@dataclass
class RuleItem:
    id: str
    title: str
    category: str
    jurisdiction: str
    parameter: str
    operator: str
    threshold: Any
    on_fail: str
    description: str
    source_id: str
    unit: Optional[str] = None
    applies_when: Optional[str] = None


@dataclass
class SourceItem:
    source_id: str
    name: str
    publisher: str
    jurisdiction: str
    document_ref: str
    last_reviewed_date: str
    status: str = "active"


@dataclass
class RoleDefinition:
    role_id: str
    name: str
    description: str
    objective: str
    tone: str
    system_instructions: str
    rules: List[str] = field(default_factory=list)
    disclaimers: List[str] = field(default_factory=list)


@dataclass
class RuleEvaluationResult:
    rule_id: str
    rule_title: str
    passed: bool
    status: str  # "PASS", "FAIL", "REFER", "NOT_APPLICABLE"
    parameter: str
    actual_value: Any
    threshold: Any
    operator: str
    message: str
    source_id: str


@dataclass
class ContextResult:
    query: str
    detected_concepts: List[str]
    selected_concepts: List[ConceptItem]
    detected_terms: List[TerminologyItem]
    evaluated_rules: List[RuleEvaluationResult]
    relevant_processes: List[ProcessItem]
    context_text: str
    scores: Dict[str, float]
    domain_active: bool = False
    extracted_parameters: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "domain_active": self.domain_active,
            "detected_concepts": self.detected_concepts,
            "extracted_parameters": self.extracted_parameters,
            "selected_concepts": [c.__dict__ for c in self.selected_concepts],
            "detected_terms": [t.__dict__ for t in self.detected_terms],
            "evaluated_rules": [r.__dict__ for r in self.evaluated_rules],
            "relevant_processes": [p.__dict__ for p in self.relevant_processes],
            "context_text": self.context_text,
            "scores": self.scores,
        }

