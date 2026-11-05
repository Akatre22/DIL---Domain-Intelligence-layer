from __future__ import annotations

from typing import Any, Dict, List, Optional

from dil.core.models import (
    ConceptItem,
    ProcessItem,
    RoleDefinition,
    RuleEvaluationResult,
    TerminologyItem,
)


class ContextBuilder:
    """
    Assembles domain knowledge, evaluated deterministic rules, role instructions,
    and verified customer data into audit-ready context for the LLM.
    """

    @staticmethod
    def build(
        query: str,
        domain: str,
        jurisdiction: str,
        role: Optional[RoleDefinition],
        concepts: List[ConceptItem],
        terms: List[TerminologyItem],
        evaluated_rules: List[RuleEvaluationResult],
        processes: List[ProcessItem],
        customer_data: Optional[Dict[str, Any]] = None,
        developer_rules: Optional[List[str]] = None,
    ) -> str:
        # If no domain entities, rules, or data apply, don't force domain context
        if not concepts and not terms and not evaluated_rules and not customer_data:
            return ""

        lines: List[str] = [
            f"=== DOMAIN INTELLIGENCE LAYER (DIL) ===",
            f"DOMAIN: {domain.upper()} | JURISDICTION: {jurisdiction.upper()}",
            f"USER QUERY: {query}",
            "",
        ]

        # 1. Role Intelligence & Operational Boundaries
        if role:
            lines.append(f"--- OPERATING ROLE: {role.name} ---")
            lines.append(f"OBJECTIVE: {role.objective}")
            lines.append(f"TONE: {role.tone}")
            if role.rules:
                lines.append("ROLE BOUNDARIES:")
                for r in role.rules:
                    lines.append(f"  • {r}")
            if developer_rules:
                lines.append("DEVELOPER-DEFINED POLICIES:")
                for dr in developer_rules:
                    lines.append(f"  • {dr}")
            lines.append("")

        # 2. Deterministic Rule Evaluations (Code checks)
        if evaluated_rules:
            lines.append("--- DETERMINISTIC RULE CHECK RESULTS ---")
            lines.append("(Note: These results were computed by deterministic code/rules engine, not by LLM.)")
            for er in evaluated_rules:
                status_symbol = "✔" if er.passed else "✖"
                lines.append(
                    f"  [{status_symbol} {er.status}] Rule {er.rule_id} ({er.rule_title}): {er.message} [Source: {er.source_id}]"
                )
            lines.append("")

        # 3. Authorized Customer / Request Data
        if customer_data:
            lines.append("--- AUTHORIZED CUSTOMER DATA ---")
            for k, v in customer_data.items():
                lines.append(f"  • {k}: {v}")
            lines.append("")

        # 4. Domain Concepts & Ontology
        if concepts:
            lines.append("--- RELEVANT BANKING CONCEPTS & ONTOLOGY ---")
            for c in concepts:
                lines.append(f"- {c.name} [{c.id}]: {c.definition}")
                for kp in c.key_points:
                    lines.append(f"    • {kp}")
                if c.caveat:
                    lines.append(f"    CAVEAT: {c.caveat}")
            lines.append("")

        # 5. Detected Terminology
        if terms:
            lines.append("--- DOMAIN TERMINOLOGY ---")
            for t in terms:
                lines.append(f"  • {t.term} ({t.expansion}): {t.definition}")
            lines.append("")

        # 6. Guardrail Directives
        lines.append("--- MANDATORY DIL GOVERNANCE INSTRUCTIONS ---")
        lines.append("1. Ground your explanation strictly on the domain knowledge and evaluated rule results above.")
        lines.append("2. Do not hallucinate or invent interest rates, bank-specific approval criteria, or regulatory limits.")
        lines.append("3. If deterministic rules breached or returned REFER/FAIL, explain the exact criteria and action required.")
        lines.append("4. Clearly state when specific numbers or conditions depend on lender discretion or official documentation.")

        if role and role.disclaimers:
            lines.append("MANDATORY DISCLAIMERS:")
            for d in role.disclaimers:
                lines.append(f"  • {d}")

        return "\n".join(lines)

