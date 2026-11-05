"""
Quickstart Example: DIL Banking Loan Advisor
Demonstrates:
1. Initializing DIL with the Banking Knowledge Pack & India jurisdiction overlay.
2. Configuring a 'loan_advisor' agent with developer policy boundaries.
3. Supplying customer application data for automated ratio calculation and deterministic rule checks.
4. Inspecting the audit-ready context generated for the LLM.
"""

import sys
from pathlib import Path

# Ensure UTF-8 output on Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add src to path
SRC_PATH = Path(__file__).resolve().parent.parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from dil import DIL


def main():
    print("=================================================================")
    print("   Domain Intelligence Layer (DIL) - Banking Quickstart Demo     ")
    print("=================================================================\n")

    # 1. Initialize DIL
    dil = DIL(domain="banking", jurisdiction="india")
    print(f"Loaded Pack: {dil.pack.manifest.name} (v{dil.pack.manifest.version})")
    print(f"Jurisdictions supported: {dil.pack.manifest.jurisdictions}")
    print(f"Total concepts loaded: {len(dil.pack.concepts)}")
    print(f"Total deterministic rules loaded: {len(dil.pack.rules)}\n")

    # 2. Configure a Loan Advisor Agent
    loan_advisor = dil.create_agent(
        role="loan_advisor",
        developer_rules=[
            "Never guarantee loan approval.",
            "Never invent interest rates or proprietary discount margins.",
            "Always state that final sanction requires formal credit appraisal and physical verification.",
            "Ask for missing income documents when necessary.",
        ],
    )

    # 3. Customer Scenario: Home Loan Application in India
    # Loan requested: ₹40 Lakh on property valued at ₹48 Lakh -> LTV = 83.3%
    # For RBI Tier 2 (₹30L to ₹75L), max permitted LTV is 80%!
    # Therefore, DIL deterministic code will flag this breach before the LLM writes an answer.
    customer_data = {
        "applicant_name": "Rahul Sharma",
        "applicant_age": 31,
        "monthly_income": 95000,
        "existing_emi": 15000,
        "cibil_score": 745,
        "loan_amount": 4000000,     # ₹40 Lakh
        "property_value": 4800000,  # ₹48 Lakh
    }

    question = "Can I get a home loan of ₹40 lakh for this property, and what will my eligibility look like?"

    print(f"Question: \"{question}\"")
    print(f"Customer Data: {customer_data}\n")

    # 4. Prepare Context & Inspect Rule Evaluations
    context_result, messages = loan_advisor.prepare(
        question=question,
        customer_data=customer_data,
    )

    print("--- [1] DETECTED DOMAIN CONCEPTS ---")
    for concept in context_result.selected_concepts:
        print(f" • {concept.name} ({concept.id}) [score: {context_result.scores.get(concept.id, 'N/A')}]")

    print("\n--- [2] DETERMINISTIC RULE EVALUATION RESULTS ---")
    for er in context_result.evaluated_rules:
        status_icon = "✔ PASS" if er.passed else f"✖ {er.status}"
        print(f" • [{status_icon}] {er.rule_id} ({er.rule_title})")
        print(f"   Detail: {er.message}")

    print("\n--- [3] PREPARED LLM PROMPT (MESSAGES) ---")
    for msg in messages:
        print(f"\n[{msg['role'].upper()} PROMPT]")
        print(msg["content"][:600] + ("..." if len(msg["content"]) > 600 else ""))

    # 5. Simulated LLM call (or connect OpenAI / Claude)
    def demo_llm_callable(messages):
        return (
            "\n[Sample LLM Output Grounded in DIL Context]\n"
            "Based on your profile and RBI regulations:\n"
            "1. LTV Limit Breach: For a loan between ₹30 Lakh and ₹75 Lakh, RBI guidelines cap the Loan-to-Value (LTV) "
            "at 80%. Your requested loan of ₹40 Lakh on a ₹48 Lakh property results in an LTV of ~83.33%, which exceeds the 80% ceiling. "
            "The maximum loan permissible for this property value is ₹38.4 Lakh (80% of ₹48 Lakh), requiring an equity down payment of ₹9.6 Lakh.\n"
            "2. Credit Score: Your CIBIL score of 745 is above the 700 benchmark, qualifying you for prime rates.\n"
            "3. Affordability: Your DTI with existing EMI of ₹15,000 against ₹95,000 monthly income is ~15.8%, leaving strong room for home loan servicing.\n"
            "Disclaimer: Loan approval is subject to document verification and formal lender appraisal."
        )

    response = loan_advisor.ask(
        question=question,
        customer_data=customer_data,
        llm_callable=demo_llm_callable,
    )
    print("\n--- [4] FINAL RESPONSE ---")
    print(response)


if __name__ == "__main__":
    main()
