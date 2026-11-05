# 🏦 Domain Intelligence Layer (DIL) — Banking

[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://python.org)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](dil_banking/pyproject.toml)
[![Evaluation Benchmark](https://img.shields.io/badge/gate%202%20benchmark-100%25%20pass-brightgreen)](dil_banking/benchmark/BENCHMARK_REPORT.md)
[![Storage Engine](https://img.shields.io/badge/storage-SQLite%20FTS5%20%2B%20Parquet-orange)](dil_banking/src/dil/storage/)

> **"Code calculates and decides; LLMs explain."**  
> DIL decouples domain knowledge, regulatory policies, and deterministic calculations from application data and the underlying language model.

---

## 🏛 What is DIL?

In conventional AI banking applications, general-purpose LLMs hallucinate interest calculations, misunderstand statutory lending caps (like RBI LTV tiers or MSME MPBF rules), and fail under prompt injection.

**DIL (Domain Intelligence Layer)** fixes this by sitting invisibly in the pipeline between the user and the LLM:
1. **Detects Domain Intent**: Identifies financial terminology and concepts in `< 3 milliseconds`.
2. **Performs Pure Python Calculations**: Extracts numbers and calculates financial ratios (LTV, DTI, DSCR, Nayak Working Capital) deterministically.
3. **Executes Statutory Policy Rules**: Evaluates non-negotiable regulatory constraints (RBI Housing LTV caps, CIBIL cutoffs, IRACP SMA/NPA triggers, Digital Lending KFS/cooling-off mandates).
4. **Assembles Audit-Ready Context**: Delivers exact pass/fail verdicts, legal citations, and role boundaries to the LLM so it explains the decision accurately without guessing.

---

## 📂 Repository File Directory & Job Role Guide

```
c:\Users\akatre\OneDrive - Nice Software Solutions\Desktop\DIL\
├── README.md                              # Master repository guide and architectural documentation
├── .env                                   # Local environment variables (API keys)
├── .gitignore                             # Git ignore rules for virtual environments and temporary builds
│
├── dil_banking/                           # 📦 OFFICIAL PRODUCTION LIBRARY (pip installable)
│   ├── pyproject.toml                     # PEP 517/621 build configuration & package metadata (v1.0.0)
│   ├── MANIFEST.in                        # Packaging manifest bundling domain assets, rules, and parquet files
│   ├── README.md                          # Dedicated library SDK documentation and developer quickstart
│   ├── dist/                              # Compiled distribution artifacts
│   │   ├── dil_banking-1.0.0-py3-none-any.whl  # Production Python Wheel (< 500 KB)
│   │   └── dil_banking-1.0.0.tar.gz            # Source distribution archive
│   ├── benchmark/                         # Gate 2 Quality & Regression Benchmark Suite
│   │   ├── golden_dataset.json            # 110 curated test scenarios (math, concepts, adversarial, OOD)
│   │   ├── runner.py                      # Automated benchmark evaluation harness
│   │   └── BENCHMARK_REPORT.md            # Benchmark execution report (100% pass rate, 3.3ms latency)
│   ├── src/dil/                           # Core SDK Source Code
│   │   ├── __init__.py                    # Public API exports (DIL, Agent, RulesEngine, Storage)
│   │   ├── core/                          # Engine Orchestration
│   │   │   ├── engine.py                  # DIL runtime coordinator & Agent persona abstraction
│   │   │   ├── loader.py                  # PackLoader for parsing manifests and JSON/Parquet assets
│   │   │   ├── models.py                  # Strongly typed dataclasses for concepts, rules, results
│   │   │   └── registry.py                # Domain pack registry & SemVer version selector
│   │   ├── storage/                       # Phase 4 High-Speed Columnar & FTS Storage
│   │   │   ├── engine.py                  # SQLite FTS5 BM25 search engine & O(1) rule indexer
│   │   │   └── parquet_exporter.py        # Columnar Parquet exporter & dil.lock SHA-256 validator
│   │   ├── rules/                         # Deterministic Rules Engine
│   │   │   └── engine.py                  # Constant-time parameter-indexed rule evaluation in code
│   │   ├── intelligence/                  # Natural Language & Parameter Processing
│   │   │   ├── matcher.py                 # Word-boundary regex tokenization & alias search
│   │   │   ├── extractor.py               # Conversational financial number & currency parser
│   │   │   └── context_builder.py         # Audit-grounded context assembler & governance formatter
│   │   ├── roles/                         # Persona & Tone Governance
│   │   │   ├── manager.py                 # RoleDefinition loader & custom role factory
│   │   │   └── predefined/                # Pre-configured banking specialist personas
│   │   │       ├── loan_advisor.json      # Retail lending advisor persona
│   │   │       ├── credit_analyst.json    # Underwriting risk analyst persona
│   │   │       └── compliance_officer.json# KYC / AML compliance persona
│   │   ├── llm/                           # Optional Provider Adapters (100% Model Agnostic)
│   │   │   ├── base.py                    # LLMCallable protocol definition
│   │   │   └── providers.py               # Optional adapters (OpenAI, Gemini, Ollama, Custom)
│   │   └── domains/banking/1.0.0/         # Standardized Banking Knowledge Pack
│   │       ├── manifest.json              # Pack metadata, jurisdiction tags, and schema map
│   │       ├── terminology.json           # 49 standard banking acronyms & regional aliases
│   │       ├── concepts.json              # 30 core banking entities with regulatory caveats
│   │       ├── relationships.json         # 18 semantic dependency links
│   │       ├── processes.json             # 5 end-to-end workflows (Credit Appraisal, IRACP, Nayak)
│   │       ├── rules/
│   │       │   ├── general.json           # Global mortgage & affordability rules
│   │       │   └── india.json             # 20 statutory RBI rules (LTV, CIBIL, IRACP, PSL, KFS, CRAR)
│   │       ├── sources/
│   │       │   └── source_registry.json   # 15 official statutory circular references & citations
│   │       └── dist/                      # Pre-compiled Snappy Parquet tables & dil.lock
│   ├── tests/                             # Automated Test Suites (24 Unit Tests)
│   │   ├── test_dil_banking.py            # SDK core engine & conversational tests
│   │   ├── test_phase2_codification.py    # Deterministic rule evaluation tests
│   │   ├── test_benchmark_gate.py         # Continuous regression gate for the 110-case benchmark
│   │   └── test_storage_engine.py         # SQLite FTS5 & Parquet roundtrip tests
│   └── examples/
│       ├── quickstart_loan_advisor.py     # Standalone terminal quickstart script
│       └── streamlit_chatbot_demo.py      # Production Streamlit Chatbot with invisible DIL integration
│
├── prod-DIL-DATA/                         # 📚 REGULATORY & STATUTORY REFERENCE CORPUS
│   ├── DATA_CATALOG_AND_STATUS.md         # Master data catalog, page counts, and codification status
│   ├── 01_regulatory_master_directions/   # Clean RBI Housing Finance Directions, PSL, IRACP
│   ├── 02_retail_lending/                 # Model retail credit underwriting policies
│   ├── 03_sme_and_commercial_credit/      # MSME Nayak Committee 20% turnover & Tandon MPBF
│   ├── 04_corporate_and_syndicated_lending/# Consortium, TRA waterfall, SEBI Debenture norms
│   ├── 05_deposits_and_nri_banking/       # DICGC ₹5L cover, Section 194A TDS, NRE/NRO/FCNR
│   ├── 06_npa_recovery_and_insolvency/    # IRACP 90-day NPA, SMA-0/1/2 DPD, SARFAESI, IBC
│   ├── 07_digital_lending_and_payments/   # Direct disbursals, KFS/APR mandate, cooling-off
│   ├── 08_trade_finance_and_forex/        # RBI ECB Directions, UCP 600, LC, Bank Guarantees
│   ├── 09_kyc_aml_and_financial_crime/    # RBI KYC Directions, 6 OVDs, PMLA, STR/CTR
│   └── 10_customer_protection_and_grievance/# RB-IOS 2021 Ombudsman scheme, compensation rules
│
└── Documentation/                         # 📄 ARCHITECTURE PAPERS, ROADMAPS & INFOGRAPHICS
    ├── Presentation/                      # 🖥️ Interactive 11-Slide React Web Presentation
    │   ├── index.html                     # Standalone interactive React web app (Zero setup required)
    │   └── README.md                      # Presentation navigation & keyboard shortcuts guide
    ├── DIL_Banking_Production_Implementation_Plan.md  # 8-Month production roadmap
    ├── Domain Intelligence Layer Concept, Architecture, Build Plan and Go-to-Market.pdf # 51-Page master paper
    ├── product_overview_1.md              # Foundation architecture summary
    ├── product_overview_2.md              # Modular pack and governance summary
    ├── DIL Banking Chatbot Comparison.png # Visual comparison infographic (With vs Without DIL)
    ├── Domain Intelligence Layer Architecture Comparison-2.png # Infographic artifact
    └── Mini DIL Banking Intelligence Workflow.png # Flowchart visualization
```

---

## ⚡ Installation Guide

### Option 1: Install from the Pre-Built Wheel (Recommended)
You can install the compiled wheel directly on any computer:
```bash
pip install dil_banking/dist/dil_banking-1.0.0-py3-none-any.whl
```

### Option 2: Install from Source (Editable Mode)
```bash
pip install -e ./dil_banking
```

### Option 3: Install Directly from Git
```bash
pip install "git+https://github.com/<your-org>/dil.git#subdirectory=dil_banking"
```

### 🌐 How to Make `pip install dil` Work Globally via PyPI
To allow anyone in the world to type `pip install dil-banking` without downloading files:
1. Create a free account at [PyPI.org](https://pypi.org).
2. Generate an API token from your PyPI account settings.
3. Upload the pre-built distribution files using `twine`:
   ```bash
   pip install twine
   twine upload dil_banking/dist/*
   ```
4. Once published, anyone can install it via:
   ```bash
   pip install dil-banking
   ```

---

## 🧠 Why DIL is 100% LLM-Agnostic

You might notice [`dil_banking/src/dil/llm/providers.py`](dil_banking/src/dil/llm/providers.py).  
**DIL does NOT depend on OpenAI, Gemini, or any external LLM service.**

- All calculations (LTV, DTI, DSCR, Nayak MPBF) and rule evaluations execute **locally in pure Python** in `< 4 milliseconds`.
- The `providers.py` file is **purely an optional convenience helper** providing one-line wrappers for popular providers:
  - `create_openai_callable(...)` (OpenAI GPT-4o)
  - `create_gemini_callable(...)` (Google Gemini 1.5 Flash/Pro)
  - `create_ollama_callable(...)` (Local offline Llama 3 / Mistral — zero cost, 100% private)
  - `create_generic_callable(...)` (Any custom internal bank function or private API)

You can use DIL without calling any LLM at all via `agent.prepare()`:
```python
import dil

engine = dil.DIL(domain="banking", jurisdiction="india")
advisor = engine.create_agent(role="loan_advisor")

# Returns structured domain context, evaluated rules, and formatted prompt
result, messages = advisor.prepare(
    question="Can I borrow 40L for a 46L flat with 85k salary?",
    customer_data={"cibil_score": 750}
)

print(result.extracted_parameters)
# {'monthly_income': 85000.0, 'loan_amount': 4000000.0, 'property_value': 4600000.0, 'ltv_ratio': 0.8696}

for rule in result.evaluated_rules:
    print(rule.rule_id, rule.status, rule.message)
# RULE-IN-RBI-LTV-002 FAIL Breached RBI Housing Loan LTV Cap - Tier 2 (₹30 Lakh to ₹75 Lakh): actual 0.8696 not <= threshold 0.8 ratio.
```

---

## 🖥 Running the Interactive Chatbot

Launch the production Streamlit application:
```bash
streamlit run app2.py
```
- **Invisible Domain Activation**: Normal non-financial queries receive friendly conversational answers.
- **Automatic Banking Intelligence**: When a user mentions loans, EMI, credit score, or working capital, DIL activates automatically, extracts numbers, executes RBI rules, and grounds the response.

---

## 🧪 Testing & Benchmark Suite

### Run All 24 Unit & Regression Tests:
```bash
python -m unittest discover -s dil_banking/tests -v
```

### Run the 110-Scenario Golden Evaluation Benchmark:
```bash
python dil_banking/benchmark/runner.py
```
*Current benchmark score:* **110/110 Passed (100.0%)** with **`3.3 ms`** average latency.

