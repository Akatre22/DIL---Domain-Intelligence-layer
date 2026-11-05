# Domain Intelligence Layer (DIL) — End-to-End Production Implementation Plan
**Domain Vertical: Banking & Financial Services**  
*Document Version: 1.0.0 · Status: Approved Baseline Plan · Target Delivery: Enterprise-Ready Release*

---

## 1. Executive Summary & Production Objectives

The objective of this plan is to transition the **Domain Intelligence Layer (DIL)** from a local in-memory prototype (`dil_banking`) into a battle-tested, high-performance, and easily installable enterprise software library.

The final deliverable of this roadmap is:
> Any developer or bank can open their terminal, run:
> ```bash
> pip install dil
> ```
> and instantly give any AI application (chatbot, credit origination tool, or underwriting agent) grounded banking intelligence, exact deterministic financial math, and strict regulatory compliance without extra configuration.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 THE PRODUCTION LIFECYCLE                                        │
│                                                                                                 │
│  [ Phase 1 ] ──> [ Phase 2 ] ──> [ Phase 3 ] ──> [ Phase 4 ] ──> [ Phase 5 ] ──> [ Phase 6 ]    │
│   Domain Data      Ontology &       "Training"      High-Speed       Packaging &      pip install   │
│   Collection       Codification     & Evaluation    Storage Engine   Distribution     Integration   │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Phase 1: Complete Banking Domain Data Collection

A production DIL requires comprehensive coverage of retail, SME, corporate lending, compliance, and deposit operations. Data collection will be structured into three distinct tiers:

### 2.1 Tier 1: Regulatory & Statutory Corpus (Public & Legally Binding)
- **Primary Source Bodies:**
  - **India:** Reserve Bank of India (RBI Master Directions on Housing Finance, Priority Sector Lending, Fair Practices Code, KYC Directions 2016, IT Rules 114B).
  - **International:** Basel III / BCBS Standards, FATF 40 Recommendations on AML/CFT, Wolfsberg Principles.
- **Ingestion Pipeline:**
  - Automated weekly scrapers targeting central bank notification feeds and official gazettes.
  - Document conversion using high-precision parsers (Docling / Unstructured) capable of preserving complex tables, circular footnotes, and effective notification dates.

### 2.2 Tier 2: Institutional Credit Policies & Product Catalogs (Semi-Public / Industry Standard)
- Model retail credit policies from major national and private banks (e.g., SBI, HDFC, ICICI model underwriting guidelines).
- Loan product sheets: LTV caps, interest rate calculation conventions (daily reducing vs monthly rest), prepayment penalties, and processing charges.
- Indian Banks' Association (IBA) operational guidelines and debt recovery standards.

### 2.3 Tier 3: Tacit SME Know-How & Operational Workflows (Expert Elicitation)
- Structured interviews with senior credit underwriters, compliance officers, and branch managers.
- Extraction of unwritten heuristic checklists:
  - How an analyst detects circular cash movements in 6-month bank statements.
  - Common rejection flags for income verification (e.g., cash salary without tax filing).
  - Escalation paths when applicant age exceeds 60 years at loan maturity.

---

## 3. Phase 2: Data Arrangement, Ontology Mapping & Rule Codification

Raw text cannot be dumped directly into an LLM. All collected knowledge must be transformed into structured, machine-executable assets.

```
                      Raw Regulatory Documents & Credit Policies
                                          │
                                          ▼
                      +---------------------------------------+
                      |     Automated Parsing & Chunking      |
                      +---------------------------------------+
                                          │
        ┌───────────────────┬─────────────┴───────┬───────────────────┐
        ▼                   ▼                     ▼                   ▼
+---------------+   +---------------+     +---------------+   +---------------+
| Terminology   |   | Concepts &    |     | Deterministic |   | Provenance    |
| & Glossary    |   | Relationships |     | Rules Engine  |   | Source Store  |
+---------------+   +---------------+     +---------------+   +---------------+
```

### 3.1 The 6 Structured Asset Types

1. **Terminology (`terminology.parquet`):**
   - 500+ standardized banking acronyms and industry phrases (e.g., EMI, LTV, DTI, FOIR, DSCR, SMA-0/1/2, NPA, CASA, PCR, ALM).
   - Multi-lingual & vernacular aliases (e.g., "Kist", "Hafta", "Bandhak" in Indian regional banking).

2. **Concept & Entity Graph (`concepts.parquet`):**
   - 2,000+ domain entities organized by category (`lending`, `deposits`, `wealth`, `trade_finance`, `compliance`).
   - Defined attributes: canonical definitions, key product points, common misconceptions, and mandatory caveats.

3. **Relationship Graph (`ontology.parquet`):**
   - Directed knowledge graph mapping dependencies and impact chains:
     - `Home Loan` $\xrightarrow{\text{governed\_by}}$ `LTV Ratio`
     - `LTV Ratio` $\xrightarrow{\text{statutory\_cap}}$ `RBI Master Direction Tier 1/2/3`
     - `Customer Application` $\xrightarrow{\text{mandatory\_check}}$ `CIBIL Bureau Report`

4. **Deterministic Rule Trees (`rules/`):**
   - Written in a strict, declarative schema with unit tests per rule:
     ```yaml
     id: RULE-IN-RBI-LTV-002
     title: RBI Housing Loan LTV Ceiling (30L to 75L)
     jurisdiction: india
     category: regulatory_cap
     condition: "loan_amount > 3000000 and loan_amount <= 7500000"
     test_expression: "ltv_ratio <= 0.80"
     on_fail: reject
     source_id: SRC-RBI-DOR-HOUSING-2020
     ```

5. **Operational Workflows (`processes.parquet`):**
   - Step-by-step state graphs for multi-step workflows (e.g., Credit Appraisal, KYC Verification, AML Alert Remediation).

6. **Source Provenance Registry (`sources.parquet`):**
   - Immutable audit references tracking the exact legal circular number, clause, publication date, and review date.

---

## 4. Phase 3: "Training", Model Alignment & Quality Verification

In DIL, "training" does not mean training an uncontrollable 70B parameter text generator. It means **fine-tuning specialized lightweight micro-models** and **building an unbending quality evaluation suite**.

### 4.1 Lightweight Specialized Micro-Models (Zero-Latency Local Models)
To ensure instant, low-cost operations, DIL trains small, specialized components that run locally without remote API calls:
- **Domain & Intent Classifier:** A lightweight 20MB model (e.g., fine-tuned `ModernBERT` or quantized embedding classifier) that categorizes queries (Banking vs. General vs. Adversarial) in `< 2 milliseconds`.
- **Financial Entity & Number Extractor:** A fine-tuned token classifier trained to extract unstructured numbers (e.g., *"paying 15k per month towards my swift car"*, *"flat worth 45 lakhs"*) with > 99% precision.

### 4.2 The Golden Evaluation Suite (Gate 2 Make-or-Break Benchmark)
A curated benchmark of **500 real-world banking test cases** reviewed and signed off by senior credit analysts:
- **150 Factual Definition & Concept Cases:** Verifying correct terminology and lack of hallucinated product features.
- **150 Deterministic Math & Underwriting Cases:** Testing boundary conditions (e.g., exactly ₹30,00,000 vs. ₹30,00,01 for RBI LTV tier shift).
- **100 Adversarial & Security Cases:**
  - Prompt injection attempting to force the bot to approve a loan.
  - Questions referencing superseded regulations (e.g., old demonetization circulars).
  - Attempts to extract confidential credit policy formulas.
- **100 Out-of-Domain General Queries:** Ensuring the bot answers normal conversational queries without awkward banking jargon.

**Continuous Regression Gate:** No code or rule pack is merged into production unless it achieves:
- **100%** on deterministic math and rule pass/fail logic.
- **Zero** unauthorized loan guarantees.
- Measurable superiority over a standard plain RAG baseline.

---

## 5. Phase 4: Production Engine & Storage Architecture

To avoid the performance degradation of flat JSON scans, production DIL transitions to an **embedded high-speed columnar/FTS storage engine**.

```
┌────────────────────────────────────────────────────────────────────────┐
│                      DIL RUNTIME CONTAINER / WORKER                    │
│                                                                        │
│   Fast Ingress Router  ──>  Regex & Token Parameter Extractor          │
│                                           │                            │
│                                           ▼                            │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │           EMBEDDED DUCKDB / SQLITE FTS5 ENGINE                 │   │
│   │   • Sub-millisecond BM25 keyword + alias indexing (< 1.5ms)    │   │
│   │   • Pre-filtered concept slices by product category            │   │
│   │   • O(1) Rule Tree lookup (Only rules matching active tags)    │   │
│   └────────────────────────────────────────────────────────────────┘   │
│                                           │                            │
│                                           ▼                            │
│   Deterministic Rules Engine  ──>  Context & Role Assembler            │
│   (Pure Python calculations)       (Appends citations & caveats)       │
└────────────────────────────────────────────────────────────────────────┘
```

### Key Production Engineering Standards
1. **Sub-millisecond Retrieval:** Replacing linear Python loops with **SQLite FTS5** or **DuckDB Parquet readers**. Query matching takes under **2 ms** even over 50,000 entries.
2. **Tag-Indexed Rule Execution:** Rules are indexed by product (`mortgage`, `auto_loan`) and borrower type (`salaried`, `self_employed`). Only the 6–10 applicable rules are executed, not the entire library.
3. **Memory-Mapped Sharing:** Multiple gunicorn/uvicorn web workers share a single read-only memory-mapped database cache, keeping total RAM overhead under **150 MB**.

---

## 6. Phase 5: Packaging, Versioning & Knowledge Registry

### 6.1 Decoupled Packaging Strategy
Production DIL cleanly separates **code engine** from **domain datasets**:
- **`dil` (Core SDK):** Pure Python engine containing orchestration, math evaluators, and LLM adapters. Packaged via `pyproject.toml` and hosted on PyPI. Size: **< 2 MB**.
- **Domain Packs (`dil.banking.india`):** Standalone data artifacts versioned independently with SemVer (`1.0.0`, `1.1.0`). Stored in an authenticated Central Knowledge Registry or local filesystem.

### 6.2 The `dil.lock` Enterprise Reproducibility Standard
Every enterprise deployment locks its exact verified versions:
```json
{
  "sdk_version": "1.0.0",
  "knowledge_packs": {
    "dil.banking": {
      "version": "1.2.0",
      "jurisdiction": "india",
      "content_hash": "sha256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069"
    }
  },
  "client_overlay": {
    "overlay_id": "hdfc_retail_v3",
    "hash": "sha256:9b12a84976cfc981..."
  }
}
```

---

## 7. Phase 6: Enterprise Deployment & Distribution

DIL will be distributed across multiple deployment modes depending on bank security requirements:

| Distribution Channel | Target Audience | How It Works |
| :--- | :--- | :--- |
| **Public PyPI (`pip install dil`)** | Individual developers, startups, fintechs | Installs the standard open SDK with bundled core banking knowledge. |
| **Private Enterprise Repository** (JFrog / AWS CodeArtifact) | Mid-size banks, NBFCs | Distributed as verified enterprise wheels within the bank's internal CI/CD pipeline. |
| **Air-Gapped Docker Container** | Tier-1 banks with strict data localization | Pre-packaged container with embedded local knowledge packs and local vLLM support (zero outbound internet access). |
| **Cloud Marketplace (AWS / GCP / Azure)** | Enterprise IT procurement | One-click deployment billed directly to the bank's committed enterprise cloud budget. |

---

## 8. Phase 7: The Final Developer Experience (End-to-End Walkthrough)

When the entire pipeline is complete, this is the exact experience for any developer in the world:

### Step 1: Install via Terminal
```bash
pip install dil
```

### Step 2: Use in Any Python Application (5 Lines of Code)
```python
import os
from dil import DIL, create_openai_callable

# 1. Initialize with domain and jurisdiction
dil = DIL(domain="banking", jurisdiction="india")

# 2. Configure a persona with your custom bank rules
advisor = dil.create_agent(
    role="loan_advisor",
    developer_rules=["Never guarantee loan approval."]
)

# 3. Ask any question — general or banking
llm = create_openai_callable(model="gpt-4o-mini")
response = advisor.ask(
    question="I make 90k/month with 12k EMI. Can I get a 40L loan on a 46L flat?",
    llm_callable=llm
)

print(response)
```

### What Happens Automatically Under the Hood:
1. DIL parses `₹90,000 income`, `₹12,000 EMI`, `₹40L loan`, `₹46L property`.
2. DIL calculates `LTV = 86.96%` and `DTI = 13.33%` in pure Python.
3. DIL checks RBI Tier-2 Housing Loan caps (maximum 80% LTV).
4. DIL detects that `86.96% > 80%` and flags a **statutory breach**.
5. DIL constructs the grounded prompt with `Rule RBI-LTV-002: FAIL`.
6. The LLM receives the exact numbers and delivers an accurate, audit-compliant answer without hallucination.

---

## 9. Master Roadmap & Milestone Schedule

```
Month 1-2: Data Ingestion & Ontology Codification
├── M1: Build regulatory web scrapers (RBI, Basel III, FATF)
├── M1: Ingest and parse 200+ circulars via Docling
└── M2: Codify Terminology (500 terms) & Ontology Graph (2,000 concepts)

Month 3-4: Deterministic Rules Engine & High-Speed Storage
├── M3: Codify 100+ standard lending rules with unit tests
├── M3: Implement DuckDB / SQLite FTS5 embedded storage engine (< 2ms lookups)
└── M4: Build conversational financial parameter extraction engine

Month 5-6: Golden Evaluation Benchmark & Engine Hardening
├── M5: Construct 500-question expert-verified evaluation dataset
├── M5: Implement automated regression test harness (Gate 2 benchmark)
└── M6: Adversarial red-teaming (jailbreaks, outdated circular traps)

Month 7-8: Packaging, Distribution & PyPI Release
├── M7: Implement SemVer Knowledge Registry and dil.lock engine
├── M7: Build client overlay cascade architecture (declarative YAML overrides)
└── M8: Publish `dil` v1.0.0 to PyPI and enterprise private repositories
```

---

## 10. Conclusion & Immediate Next Action

By following this implementation plan, DIL transitions from an interesting local experiment into an indispensable piece of enterprise fintech infrastructure.

**Immediate Next Step:**  
Begin **Sprint 1 of Phase 1**: Setting up the automated legal document parser and compiling the master list of 50 primary RBI circulars and Basel III guidelines into structured parquet schemas.

