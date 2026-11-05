import sys
from pathlib import Path
import unittest

# Ensure src is in sys.path for test discovery
SRC_PATH = Path(__file__).resolve().parent.parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from dil import DIL, DomainRegistry, PackLoader, RulesEngine, RoleManager


class TestDILBanking(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dil_global = DIL(domain="banking", jurisdiction="global")
        cls.dil_india = DIL(domain="banking", jurisdiction="india")

    def test_pack_manifest_and_assets(self):
        pack = self.dil_india.pack
        self.assertEqual(pack.manifest.domain, "banking")
        self.assertEqual(pack.manifest.version, "1.0.0")
        self.assertGreaterEqual(len(pack.concepts), 17)
        self.assertGreaterEqual(len(pack.terminology), 10)
        self.assertGreaterEqual(len(pack.relationships), 10)
        self.assertGreaterEqual(len(pack.processes), 2)
        self.assertGreaterEqual(len(pack.rules), 9)
        self.assertGreaterEqual(len(pack.sources), 5)

    def test_query_concept_detection(self):
        query = "What factors affect eligibility for a home loan?"
        result = self.dil_india.get_context(query)
        self.assertIn("loan.home", result.detected_concepts)
        self.assertIn("loan.eligibility", result.detected_concepts)
        self.assertTrue(len(result.context_text) > 100)

    def test_terminology_detection(self):
        query = "How is the EMI calculated on my mortgage?"
        result = self.dil_india.get_context(query)
        detected_term_names = [t.term for t in result.detected_terms]
        self.assertIn("EMI", detected_term_names)

    def test_deterministic_rule_pass(self):
        # Applicant in India with loan 25 Lakh, property 30 Lakh -> LTV = 25/30 = 83.3% <= 90%
        # CIBIL = 750 (>= 700)
        customer_data = {
            "applicant_age": 30,
            "loan_amount": 2500000,
            "property_value": 3000000,
            "monthly_income": 80000,
            "existing_emi": 10000,
            "cibil_score": 750,
        }
        result = self.dil_india.get_context(
            query="Check my loan affordability",
            customer_data=customer_data,
        )
        rule_dict = {r.rule_id: r for r in result.evaluated_rules}
        self.assertIn("RULE-IN-RBI-LTV-001", rule_dict)
        self.assertTrue(rule_dict["RULE-IN-RBI-LTV-001"].passed)
        self.assertEqual(rule_dict["RULE-IN-RBI-LTV-001"].status, "PASS")
        self.assertTrue(rule_dict["RULE-IN-CIBIL-SCORE-001"].passed)

    def test_deterministic_rule_breach(self):
        # Loan > 75 Lakh in India (Tier 3 max LTV = 75%)
        # Here: loan 80 Lakh on 90 Lakh property -> LTV = 88.8% > 75% -> FAIL
        # CIBIL 650 < 700 -> REFER
        customer_data = {
            "applicant_age": 32,
            "loan_amount": 8000000,
            "property_value": 9000000,
            "cibil_score": 650,
        }
        result = self.dil_india.get_context(
            query="Check my eligibility for 80 lakh home loan",
            customer_data=customer_data,
        )
        rule_dict = {r.rule_id: r for r in result.evaluated_rules}
        self.assertIn("RULE-IN-RBI-LTV-003", rule_dict)
        self.assertFalse(rule_dict["RULE-IN-RBI-LTV-003"].passed)
        self.assertEqual(rule_dict["RULE-IN-RBI-LTV-003"].status, "FAIL")
        self.assertEqual(rule_dict["RULE-IN-CIBIL-SCORE-001"].status, "REFER")

    def test_role_agent_workflow(self):
        agent = self.dil_india.create_agent(
            role="loan_advisor",
            developer_rules=["Never guarantee loan approval"],
        )
        result, messages = agent.prepare(
            question="Can I afford a 40 Lakh home loan?",
            customer_data={"monthly_income": 90000, "existing_emi": 12000, "cibil_score": 780},
        )
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[1]["role"], "user")
        self.assertIn("Retail Loan Advisor", messages[1]["content"])
        self.assertIn("Never guarantee loan approval", messages[1]["content"])

    def test_custom_role(self):
        custom_role = self.dil_india.role_manager.create_custom_role(
            role_id="audit_agent",
            name="Regulatory Audit Assistant",
            objective="Ensure loan files comply with RBI housing finance master directions.",
            rules=["Always flag unverified income sources."],
            system_instructions="You are an internal audit assistant checking credit compliance.",
        )
        agent = self.dil_india.create_agent(role=custom_role)
        result, messages = agent.prepare(question="Audit this loan proposal")
        self.assertIn("Regulatory Audit Assistant", messages[1]["content"])
        self.assertIn("Always flag unverified income sources", messages[1]["content"])

    def test_general_question_domain_inactive(self):
        result, messages = self.dil_india.build_messages("What is the capital of France?")
        self.assertFalse(result.domain_active)
        self.assertEqual(len(result.selected_concepts), 0)
        self.assertIn("helpful, knowledgeable", messages[0]["content"])

    def test_conversational_financial_extraction(self):
        query = "I earn 85000 with 15000 emi. Can I get a 40 lakh home loan on a 48 lakh flat with cibil 750?"
        result, messages = self.dil_india.build_messages(query)
        self.assertTrue(result.domain_active)
        self.assertEqual(result.extracted_parameters.get("cibil_score"), 750)
        self.assertEqual(result.extracted_parameters.get("loan_amount"), 4000000.0)
        self.assertTrue(len(result.evaluated_rules) > 0)
        self.assertIn("DOMAIN INTELLIGENCE LAYER", messages[1]["content"])


if __name__ == "__main__":
    unittest.main()

