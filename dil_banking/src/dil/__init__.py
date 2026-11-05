"""
Domain Intelligence Layer (DIL) - Banking
A reusable intelligence infrastructure for AI applications in banking.
"""

from dil.core.engine import DIL, Agent
from dil.core.loader import LoadedPack, PackLoader
from dil.core.models import (
    ConceptItem,
    ContextResult,
    PackManifest,
    ProcessItem,
    RelationshipItem,
    RoleDefinition,
    RuleEvaluationResult,
    RuleItem,
    SourceItem,
    TerminologyItem,
)
from dil.core.registry import DomainRegistry
from dil.llm.providers import (
    create_gemini_callable,
    create_generic_callable,
    create_ollama_callable,
    create_openai_callable,
)
from dil.roles.manager import RoleManager
from dil.rules.engine import RulesEngine
from dil.storage.engine import FTSStorageEngine
from dil.storage.parquet_exporter import ParquetPackExporter

__version__ = "1.0.0"

__all__ = [
    "DIL",
    "Agent",
    "DomainRegistry",
    "PackLoader",
    "LoadedPack",
    "RulesEngine",
    "RoleManager",
    "FTSStorageEngine",
    "ParquetPackExporter",
    "ContextResult",
    "PackManifest",
    "ConceptItem",
    "TerminologyItem",
    "RelationshipItem",
    "ProcessItem",
    "RuleItem",
    "SourceItem",
    "RoleDefinition",
    "RuleEvaluationResult",
    "create_openai_callable",
    "create_gemini_callable",
    "create_ollama_callable",
    "create_generic_callable",
]
