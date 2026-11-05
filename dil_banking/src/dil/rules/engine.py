from __future__ import annotations

import operator
from typing import Any, Dict, List, Optional

from dil.core.models import RuleEvaluationResult, RuleItem

OPERATORS = {
    "<=": operator.le,
    ">=": operator.ge,
    "<": operator.lt,
    ">": operator.gt,
    "==": operator.eq,
    "!=": operator.ne,
}


class RulesEngine:
    """
    High-performance indexed deterministic rules engine.
    Ensures mathematical and policy constraints are computed and verified in code,
    never entrusted to LLM approximation.
    Uses O(1) parameter-indexed trees to evaluate only applicable rules.
    """

    def __init__(self, rules: Optional[List[RuleItem]] = None):
        self._rules: List[RuleItem] = []
        self._by_param: Dict[str, List[RuleItem]] = {}
        if rules:
            for r in rules:
                self.add_rule(r)

    def add_rule(self, rule: RuleItem) -> None:
        self._rules.append(rule)
        self._by_param.setdefault(rule.parameter, []).append(rule)

    @property
    def rules(self) -> List[RuleItem]:
        return self._rules

    def evaluate_all(
        self,
        parameters: Dict[str, Any],
        jurisdiction: str = "global",
    ) -> List[RuleEvaluationResult]:
        """
        Evaluates applicable rules against supplied customer/applicant parameters.
        Leverages O(1) parameter index to evaluate only rules whose parameter is present.
        """
        results: List[RuleEvaluationResult] = []
        jur_normalized = jurisdiction.lower()

        # O(1) Candidate rule selection based on input parameters
        candidate_rules: List[RuleItem] = []
        for param_key in parameters.keys():
            matching_rules = self._by_param.get(param_key)
            if matching_rules:
                candidate_rules.extend(matching_rules)

        for rule in candidate_rules:
            # Check jurisdiction applicability
            if rule.jurisdiction not in ("global", jur_normalized):
                continue

            # Check dynamic activation condition if defined (e.g. "loan_amount > 3000000")
            if rule.applies_when and not self._check_applies_when(rule.applies_when, parameters):
                continue

            # Check if required parameter is provided
            if rule.parameter not in parameters:
                continue

            actual_val = parameters[rule.parameter]
            op_fn = OPERATORS.get(rule.operator)
            if not op_fn:
                continue

            try:
                passed = bool(op_fn(actual_val, rule.threshold))
            except Exception:
                passed = False

            if passed:
                status = "PASS"
                msg = f"Complies with {rule.title}: actual {actual_val} {rule.operator} threshold {rule.threshold} {rule.unit or ''}".strip()
            else:
                status = "FAIL" if rule.on_fail == "reject" else "REFER"
                msg = f"Breached {rule.title}: actual {actual_val} not {rule.operator} threshold {rule.threshold} {rule.unit or ''}. Action: {rule.on_fail}.".strip()

            results.append(
                RuleEvaluationResult(
                    rule_id=rule.id,
                    rule_title=rule.title,
                    passed=passed,
                    status=status,
                    parameter=rule.parameter,
                    actual_value=actual_val,
                    threshold=rule.threshold,
                    operator=rule.operator,
                    message=msg,
                    source_id=rule.source_id,
                )
            )

        return results

    def _check_applies_when(self, condition_expr: str, params: Dict[str, Any]) -> bool:
        """Safely evaluates simple python expressions over numeric parameter keys."""
        try:
            # Restrict scope to known parameters with numbers/booleans
            safe_scope = {k: v for k, v in params.items() if isinstance(v, (int, float, bool, str))}
            return bool(eval(condition_expr, {"__builtins__": {}}, safe_scope))
        except Exception:
            return False
