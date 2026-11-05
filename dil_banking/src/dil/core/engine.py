from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple

from dil.core.loader import LoadedPack
from dil.core.models import ContextResult, RoleDefinition, RuleEvaluationResult
from dil.core.registry import DomainRegistry
from dil.intelligence.context_builder import ContextBuilder
from dil.intelligence.extractor import ConversationalParameterExtractor
from dil.intelligence.matcher import IntelligenceMatcher
from dil.roles.manager import RoleManager
from dil.rules.engine import RulesEngine
from dil.storage.engine import FTSStorageEngine


class Agent:
    """
    Role-configured DIL Agent.
    Combines domain intelligence, role boundaries, deterministic rules,
    and optional customer data to prepare grounded prompts or orchestrate responses.
    """

    def __init__(
        self,
        dil: "DIL",
        role: RoleDefinition,
        developer_rules: Optional[List[str]] = None,
        objective: Optional[str] = None,
    ):
        self.dil = dil
        self.role = role
        self.developer_rules = developer_rules or []
        self.objective = objective or role.objective

    def prepare(
        self,
        question: str,
        customer_data: Optional[Dict[str, Any]] = None,
        history: Optional[List[Dict[str, str]]] = None,
        top_k: int = 5,
    ) -> Tuple[ContextResult, List[Dict[str, str]]]:
        """Prepares domain context and provider-neutral chat messages."""
        return self.dil.build_messages(
            query=question,
            role=self.role,
            customer_data=customer_data,
            history=history,
            developer_rules=self.developer_rules,
            top_k=top_k,
        )

    def ask(
        self,
        question: str,
        llm_callable: Callable[..., Any],
        customer_data: Optional[Dict[str, Any]] = None,
        history: Optional[List[Dict[str, str]]] = None,
        top_k: int = 5,
        **kwargs: Any,
    ) -> Any:
        """
        Sends the prepared context and question to the provided LLM function.
        The llm_callable must accept a 'messages' keyword argument.
        """
        result, messages = self.prepare(
            question=question,
            customer_data=customer_data,
            history=history,
            top_k=top_k,
        )
        return llm_callable(messages=messages, **kwargs)


class DIL:
    """
    Domain Intelligence Layer (DIL) Engine.
    Coordinates domain packs, ontology retrieval, role management, and deterministic rules.
    """

    def __init__(
        self,
        domain: str = "banking",
        jurisdiction: str = "global",
        version: Optional[str] = None,
        custom_packs_dir: Optional[str] = None,
    ):
        self.domain = domain.lower()
        self.jurisdiction = jurisdiction.lower()
        self.registry = DomainRegistry(custom_packs_dir=custom_packs_dir)
        self.pack: LoadedPack = self.registry.get_pack(domain=self.domain, version=version)
        self.storage = FTSStorageEngine()
        self.storage.index_pack(self.pack)
        self.matcher = IntelligenceMatcher(self.pack)
        self.rules_engine = RulesEngine(self.pack.rules)
        self.role_manager = RoleManager()

    def get_context(
        self,
        query: str,
        role: Optional[RoleDefinition | str] = None,
        customer_data: Optional[Dict[str, Any]] = None,
        developer_rules: Optional[List[str]] = None,
        top_k: int = 5,
    ) -> ContextResult:
        """
        Retrieves relevant domain concepts, extracts conversational parameters,
        evaluates deterministic rules, and generates structured context.
        """
        # Resolve role
        role_def: Optional[RoleDefinition] = None
        if isinstance(role, str):
            role_def = self.role_manager.get_role(role)
        elif isinstance(role, RoleDefinition):
            role_def = role

        # 1. Match concepts and terminology
        concepts, terms, scores = self.matcher.match(
            query=query,
            jurisdiction=self.jurisdiction,
            max_concepts=top_k,
        )

        # 2. Extract conversational financial parameters from query
        extracted_params = ConversationalParameterExtractor.extract(query)

        # 3. Derive helper parameters from customer data + extracted parameters
        eval_params: Dict[str, Any] = {}
        if customer_data:
            eval_params.update(customer_data)
        eval_params.update(extracted_params)

        # Automatic ratio computations (code does the math, not the LLM)
        if "loan_amount" in eval_params and "property_value" in eval_params:
            try:
                pv = float(eval_params["property_value"])
                if pv > 0:
                    eval_params["ltv_ratio"] = round(float(eval_params["loan_amount"]) / pv, 4)
            except (ValueError, ZeroDivisionError):
                pass

        if "monthly_income" in eval_params and "existing_emi" in eval_params:
            try:
                income = float(eval_params["monthly_income"])
                if income > 0:
                    eval_params["dti_ratio"] = round(float(eval_params["existing_emi"]) / income, 4)
            except (ValueError, ZeroDivisionError):
                pass

        if "credit_score" in eval_params and "cibil_score" not in eval_params:
            eval_params["cibil_score"] = eval_params["credit_score"]

        # 4. Evaluate deterministic rules
        evaluated_rules: List[RuleEvaluationResult] = []
        if eval_params:
            evaluated_rules = self.rules_engine.evaluate_all(
                parameters=eval_params,
                jurisdiction=self.jurisdiction,
            )

        # 5. Determine if domain is active
        # Activated if role is explicitly assigned, concepts matched, terms matched, rules were evaluated, or financial parameters found
        domain_active = bool(role_def or concepts or terms or evaluated_rules or extracted_params)

        # 6. Assemble context text
        effective_customer_data = eval_params if eval_params else None
        context_text = ContextBuilder.build(
            query=query,
            domain=self.domain,
            jurisdiction=self.jurisdiction,
            role=role_def if domain_active else None,
            concepts=concepts,
            terms=terms,
            evaluated_rules=evaluated_rules,
            processes=self.pack.processes if domain_active else [],
            customer_data=effective_customer_data,
            developer_rules=developer_rules if domain_active else None,
        )

        return ContextResult(
            query=query,
            domain_active=domain_active,
            extracted_parameters=extracted_params,
            detected_concepts=[c.id for c in concepts],
            selected_concepts=concepts,
            detected_terms=terms,
            evaluated_rules=evaluated_rules,
            relevant_processes=self.pack.processes if domain_active else [],
            context_text=context_text,
            scores=scores,
        )

    def build_messages(
        self,
        query: str,
        role: Optional[RoleDefinition | str] = None,
        customer_data: Optional[Dict[str, Any]] = None,
        history: Optional[List[Dict[str, str]]] = None,
        developer_rules: Optional[List[str]] = None,
        top_k: int = 5,
    ) -> Tuple[ContextResult, List[Dict[str, str]]]:
        """Constructs provider-agnostic system and user message payload with conversation history."""
        result = self.get_context(
            query=query,
            role=role,
            customer_data=customer_data,
            developer_rules=developer_rules,
            top_k=top_k,
        )

        if result.domain_active:
            if isinstance(role, str):
                role_instructions = self.role_manager.get_role(role).system_instructions
            elif isinstance(role, RoleDefinition):
                role_instructions = role.system_instructions
            else:
                role_instructions = (
                    "You are an AI assistant specialized in banking and financial services. "
                    "Provide factual, clear, and structured answers grounded strictly in banking "
                    "domain knowledge and evaluated rules. Distinguish general banking principles "
                    "from bank-specific policies, and enforce credit cautions."
                )
            user_content = (result.context_text + f"\n\nUSER QUESTION: {query}") if result.context_text else query
        else:
            role_instructions = (
                "You are a helpful, knowledgeable, and polite AI assistant. "
                "Respond naturally, accurately, and concisely to the user's questions."
            )
            user_content = query

        messages: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": role_instructions,
            }
        ]

        # Multi-turn history support
        if history:
            for h in history[-8:]:
                if h.get("role") in ("user", "assistant") and h.get("content"):
                    messages.append({"role": h["role"], "content": h["content"]})

        messages.append({
            "role": "user",
            "content": user_content,
        })

        return result, messages

    def create_agent(
        self,
        role: str | RoleDefinition,
        developer_rules: Optional[List[str]] = None,
        objective: Optional[str] = None,
    ) -> Agent:
        """Configures a reusable DIL Agent bound to a specific role."""
        if isinstance(role, str):
            role_def = self.role_manager.get_role(role)
        else:
            role_def = role

        return Agent(
            dil=self,
            role=role_def,
            developer_rules=developer_rules,
            objective=objective,
        )

    def answer(
        self,
        query: str,
        llm_callable: Callable[..., Any],
        role: Optional[str | RoleDefinition] = None,
        customer_data: Optional[Dict[str, Any]] = None,
        history: Optional[List[Dict[str, str]]] = None,
        top_k: int = 5,
        **kwargs: Any,
    ) -> Any:
        """Directly evaluates context and passes to llm_callable."""
        result, messages = self.build_messages(
            query=query,
            role=role,
            customer_data=customer_data,
            history=history,
            top_k=top_k,
        )
        return llm_callable(messages=messages, **kwargs)

