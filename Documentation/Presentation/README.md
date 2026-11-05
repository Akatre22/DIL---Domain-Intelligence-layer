# Domain Intelligence Layer (DIL) — Technical & Business Presentation

An interactive, 12-slide React-based web presentation engineered for bank executives (CROs, Chief Risk Officers, Heads of Digital Lending) and technical leaders (CTOs, Lead AI Architects, Credit Risk Engineers).

---

## 🎨 Design System & UI Architecture

- **Visual Style**: Clean, bright, minimalist corporate palette (pure white `#FFFFFF`, soft slate `#F8FAFC`, slate-900 `#0F172A` typography).
- **Zero Emojis & Clutter**: All concepts expressed through typographic hierarchy, subtle status pills (`[PASS]`, `[BREACH]`), and structural cards.
- **Collapsible Sidebar Index**:
  - Located on the left with one-click **Expand / Collapse** toggle (`« Hide Index` / `» Slide Index`).
  - Lists all 12 slides with numeric indicators (`01` to `12`), titles, and domain category tags.
- **Dynamic & Fully Responsive Across All Resolutions**:
  - **Mobile (< 768px)**: Auto-collapses into a slide-over off-canvas drawer with a blurred backdrop. Tap any slide to auto-close and view.
  - **Tablets (768px - 1024px)**: Touch-optimized drawer with quick toggle.
  - **Laptops (1024px - 1440px)**: Smooth side-by-side workspace with collapsible toggle to give full-width breathing room to slides.
  - **Desktops & 4K (1440px - 3840px)**: Centered `max-w-5xl` slide canvas with optimal typographic line lengths.

---

## 🚀 How to Open and Present

The presentation is 100% self-contained. No Node.js, `npm`, or build steps are required.

### Option 1: Direct File Open (Recommended)
Double-click [`index.html`](./index.html) in Windows File Explorer or open it in any modern browser (Chrome, Edge, Firefox, Safari).

### Option 2: Local HTTP Server (Optional)
```bash
python -m http.server 8000 --directory "Documentation/Presentation"
```
Then navigate to: `http://localhost:8000`

---

## ⌨️ Keyboard Shortcuts & Controls

| Shortcut / Button | Action |
| :--- | :--- |
| **`I` or `M`** | **Toggle Slide Index Sidebar (Expand / Collapse)** |
| **`→` (Right Arrow) / `Space` / `PageDown`** | Advance to Next Slide |
| **`←` (Left Arrow) / `PageUp`** | Return to Previous Slide |
| **`Home` / `End`** | Jump to First / Last Slide |
| **`Esc`** | Close Sidebar Drawer / Close Technical Report Modal |
| **Top Left `[« / »]` Button** | Click to Expand or Collapse Sidebar |
| **Footer `Navigate: [←] [→]`** | Tactile Clickable Navigation Keycaps |
| **Footer `DIL Technical Report`** | Opens Executive Architectural Metadata Modal |

---

## 📑 Detailed 12-Slide Content & Interactive Features

1. **Slide 1: Executive Overview**
   - The DIL Thesis: *"Code calculates and decides; LLMs explain."*
   - Decoupling domain intelligence from probabilistic generative models.

2. **Slide 2: The Enterprise LLM Problem**
   - Comparative risk matrix: Why conventional RAG fails at arithmetic, ignores statutory ceilings, and is vulnerable to prompt injections.

3. **Slide 3: What is DIL & Strategic Value**
   - 4 Architectural Pillars: Deterministic Precision, Regulatory Enforcement, Sub-4ms Latency, Zero Cloud Lock-in.

4. **Slide 4: Technical Architecture Pipeline**
   - **Interactive Layer Inspector**: Click on any of the 5 pipeline stages (Ingestion ➔ Extractor ➔ Rules Engine ➔ Context Assembler ➔ Target LLM) to inspect its inputs, outputs, and execution speed.

5. **Slide 5: DIL Library & PyPI Release**
   - Official package: `pip install dil-banking`.
   - 3-line drop-in code integration with one-click copy buttons.

6. **Slide 6: The 51-Function Subsystem Catalog**
   - **Interactive Function Browser**: Filter callable methods by subsystem (`Core`, `Intelligence`, `Rules`, `Storage`, `LLM`).

7. **Slide 7: How DIL Was Developed (Methodology)**
   - 5-Phase SDLC: Regulatory Data Collection ➔ Semantic Codification ➔ Golden Evaluation Benchmark ➔ Columnar Storage Engine ➔ PyPI Release.

8. **Slide 8: Data-to-DIL Transformation Pipeline (Animated Suspense Journey)**
   - **Clickable Raw Document Intake**: Select from 3 authentic regulatory files:
     - `RBI_Housing_Finance_Directions_2025.pdf` (108 Pages · Individual Housing LTV Limits)
     - `RBI_Master_Directions_PSL_2025.html` (64 Sections · 40% ANBC PSL Mandates)
     - `RBI_Digital_Lending_Directions_2022.pdf` (42 Pages · KFS & Direct Disbursal Mandate)
   - **Progressive Mystery & Suspense Mechanics**:
     - Subsequent stages are initially locked (`[LOCKED]`), teasing the audience with critical questions (e.g. *"How do we extract quantitative ceilings without letting an LLM guess?"*).
     - Clicking **"Transform & Reveal Stage 0X ➔"** launches an **animated compiler scan** with real-time ticker logs and progress bar before unveiling the next layer.
   - **`[▶ Auto-Play Journey]` Presentation Mode**:
     - Automatically steps through the transformation flow with dramatic timing, executing each compilation step and concluding with a live simulated banking agent execution in Stage 07.
   - **7 Animated Compilation Layers**:
     - *Stage 01: Raw Intake* — Unstructured central bank circular ingestion & SHA-256 verification.
     - *Stage 02: Extraction* — Regex clause parsing, table extraction, and operative quantitative ceiling isolation.
     - *Stage 03: Terminology* — Canonical schemas in `terminology.json` with multi-alias synonym trees.
     - *Stage 04: Ontology* — 1-hop knowledge graph modeling in `concepts.json` with mandatory caveats.
     - *Stage 05: Rules AST* — Compiling machine-executable boolean condition logic in `rules/india.json`.
     - *Stage 06: Storage & Lock* — SQLite FTS5 BM25 index generation, Snappy Parquet tables, and `dil.lock` SHA-256 seal.
     - *Stage 07: Live DIL Runtime* — Production Python execution with an **interactive live agent simulation sandbox** delivering sub-4ms verified decisions.

9. **Slide 9: Case Study: Single Regulation Codification**
   - Step-by-step transformation of *RBI Housing Finance Master Directions 2025* (Raw Text ➔ Terminology ➔ Concepts ➔ Executable Rule).
   - **Live Interactive LTV Rule Simulator**: Move the loan slider from ₹10 Lakh to ₹100 Lakh to watch statutory RBI tiers (90%, 80%, 75%) and pass/breach verdicts trigger in real-time.

10. **Slide 10: Enterprise Database Pipeline**
    - Ingesting Core Banking System (CBS) or SQL database records directly into DIL.
    - **Interactive Database Customer Switcher**: Toggle between *Rahul Sharma* (LTV issue) and *Priya Verma* (CIBIL issue) to inspect real database evaluation results.

11. **Slide 11: Commercial Banking Use Cases**
    - High-stakes workflows: Retail Loan Advisor, Credit Underwriter CAM Generator, MSME Nayak Working Capital, and Digital Lending Compliance.

12. **Slide 12: Production Verification & Golden Benchmark**
    - Continuous validation metrics: 110/110 passed (100%), 3.3 ms mean latency, 100% prompt injection resistance, 0% out-of-domain false positives.
