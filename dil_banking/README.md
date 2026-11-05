# Domain Intelligence Layer (DIL) — Banking

**DIL** is a reusable intelligence infrastructure for enterprise AI applications in banking. It ensures LLMs reason like accredited banking specialists by decoupling **domain knowledge, role boundaries, and deterministic rules** from application data and the underlying model.

---

## 🏛 Architecture Overview

```
                      +---------------------------------------+
                      |         Application / Chatbot         |
                      +---------------------------------------+
                                          │
                                          ▼
                      +---------------------------------------+
                      |       DIL Interface Layer (SDK)       |
                      |   • Agent configuration (Role, Rules) |
                      |   • Query & customer data intake      |
                      +---------------------------------------+
                                          │
       ┌──────────────────────────────────┼──────────────────────────────────┐
       ▼                                  ▼                                  ▼
+-----------------------+     +-----------------------+     +-----------------------+
|  Domain Intelligence  |     |   Role Intelligence   |     |  Deterministic Rules  |
|  • Terminology        |     |  • Objectives         |     |  • Code computations  |
|  • Concepts & aliases |     |  • Persona tone       |     |  • Regulatory caps    |
|  • 1-hop ontology     |     |  • Disclaimers        |     |  • RBI / Global rules |
+-----------------------+     +-----------------------+     +-----------------------+
       └──────────────────────────────────┬──────────────────────────────────┘
                                          │
                                          ▼
                      +---------------------------------------+
                      |       Audit-Ready Context Engine      |
                      |   Structures facts, rule verdicts,    |
                      |   and mandatory governance directives |
                      +---------------------------------------+
                                          │
                                          ▼
                      +---------------------------------------+
                      |   Any LLM (OpenAI, Claude, Local)     |
                      |   "Code decides; LLM explains"        |
                      +---------------------------------------+
```

---

## 📂 Project Structure

```
dil_banking/
├── pyproject.toml                         # Packaging configuration
├── README.md                              # Documentation
├── src/
│   └── dil/
│       ├── __init__.py                    # Public API exports
│       ├── core/
│       │   ├── engine.py                  # DIL and Agent classes
│       │   ├── loader.py                  # PackLoader and LoadedPack
│       │   ├── models.py                  # Dataclasses (Manifest, Concepts, Rules, Context)
│       │   └── registry.py                # DomainRegistry & pack version manager
│       ├── domains/
│       │   └── banking/
│       │       └── 1.0.0/                 # Versioned Banking Knowledge Pack
│       │           ├── manifest.json      # Pack identity, dependencies, and asset maps
│       │           ├── terminology.json   # Industry acronyms & definitions (EMI, LTV, CASA, etc.)
│       │           ├── concepts.json      # 17 core banking entities with aliases & caveats
│       │           ├── relationships.json # Semantic graph & dependency linkages
│       │           ├── processes.json     # Standard workflows (Credit Appraisal, KYC)
│       │           ├── rules/
│       │           │   ├── general.json   # Global lending & affordability rules
│       │           │   └── india.json     # RBI LTV caps, CIBIL thresholds, PAN rules
│       │           └── sources/
│       │               └── source_registry.json # Regulatory provenance & citations
│       ├── intelligence/
│       │   ├── matcher.py                 # Query tokenization, alias matching & 1-hop expansion
│       │   └── context_builder.py         # Structured context assembler with guardrails
│       ├── roles/
│       │   ├── manager.py                 # Predefined & custom role manager
│       │   └── predefined/
│       │       ├── loan_advisor.json      # Retail loan advisor persona & limits
│       │       ├── credit_analyst.json    # Underwriting risk analyst persona
│       │       └── compliance_officer.json# KYC / AML compliance officer persona
│       ├── rules/
│       │   └── engine.py                  # Deterministic rule evaluator (code-driven checks)
│       └── llm/
│           ├── base.py                    # LLM callable protocol
│           └── providers.py               # OpenAI provider adapter
├── tests/
│   └── test_dil_banking.py                # Unit test suite
└── examples/
    └── quickstart_loan_advisor.py         # End-to-end quickstart script
```

---

## 🚀 Quickstart Guide

### 1. Installation

From the project root:

```powershell
pip install -e dil_banking
```

### 2. Run the Unit Tests

```powershell
python -m unittest discover -s dil_banking/tests -v
```

### 3. Run the Loan Advisor Demo

```powershell
python dil_banking/examples/quickstart_loan_advisor.py
```

---

## 💡 Developer Usage Example

```python
from dil import DIL

# 1. Initialize DIL for Banking with India jurisdiction overlay
dil = DIL(domain="banking", jurisdiction="india")

# 2. Configure a Role Agent with developer boundaries
advisor = dil.create_agent(
    role="loan_advisor",
    developer_rules=[
        "Never guarantee loan approval.",
        "Never invent interest rates.",
        "State that sanction requires formal verification.",
    ],
)

# 3. Supply customer data for automated calculation & rule evaluation
customer_data = {
    "applicant_age": 31,
    "loan_amount": 4000000,     # ₹40 Lakh
    "property_value": 4800000,  # ₹48 Lakh (Calculated LTV: 83.33% -> Breaches RBI 80% cap!)
    "monthly_income": 95000,
    "existing_emi": 15000,      # (Calculated DTI: 15.79% -> Complies with <= 50% limit)
    "cibil_score": 745,         # (Complies with >= 700 prime cutoff)
}

question = "Can I get a home loan of 40 lakh for this property?"

# 4. Prepare context or ask an LLM
result, messages = advisor.prepare(
    question=question,
    customer_data=customer_data,
)

# Deterministic rule verdicts are already computed:
for er in result.evaluated_rules:
    print(f"[{er.status}] {er.rule_title}: {er.message}")

# 5. Call LLM (OpenAI, Claude, or local model)
# response = advisor.ask(question=question, customer_data=customer_data, llm_callable=my_llm_fn)
```

---

## 🛡 Key Guarantees
1. **Mathematical Accuracy**: Calculations (LTV, DTI, debt servicing) are executed in pure Python code.
2. **Regulatory Provenance**: Every rule breach or pass carries its `rule_id`, jurisdiction, and source citation (e.g., RBI Master Directions).
3. **No Hallucinated Policies**: Explicit system and developer boundaries instruct the model to state missing requirements instead of guessing bank criteria.

