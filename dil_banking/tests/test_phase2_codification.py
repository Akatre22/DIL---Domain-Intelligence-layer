"""
Unit tests for DIL Phase 2 Knowledge Codification:
Tests deterministic evaluation of newly codified rules across:
1. IRACP Delinquency & NPA Classification (SMA-2, 90-day NPA)
2. SME Working Capital (Nayak 20% MPBF, 5% Margin, 1.20 DSCR)
3. Priority Sector Lending (40% ANBC, 18% Agri, 7.5% Micro)
4. Digital Lending Guidelines (Direct Disbursal, Mandatory KFS, Cooling-off)
5. Deposits & Customer Protection (DICGC 5 Lakh limit, Gold Loan 75% LTV)
6. Capital Adequacy (Bank 9% CRAR, HFC 15% CRAR)
"""

import unittest
from dil import DIL


class TestPhase2Codification(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dil = DIL(domain="banking", jurisdiction="india")

    def test_iracp_npa_classification(self):
        # 1. 45 DPD should pass <= 90 days NPA threshold
        res_standard = self.dil.rules_engine.evaluate_all({"days_past_due": 45}, jurisdiction="india")
        npa_rules = [r for r in res_standard if r.rule_id == "RULE-IN-IRACP-NPA-001"]
        self.assertEqual(len(npa_rules), 1)
        self.assertTrue(npa_rules[0].passed)
        self.assertEqual(npa_rules[0].status, "PASS")

        # 2. 75 DPD triggers SMA-2 (breaches <= 60 threshold)
        res_sma2 = self.dil.rules_engine.evaluate_all({"days_past_due": 75}, jurisdiction="india")
        sma2_rule = next(r for r in res_sma2 if r.rule_id == "RULE-IN-IRACP-SMA2-001")
        self.assertFalse(sma2_rule.passed)
        self.assertEqual(sma2_rule.status, "REFER")

        # 3. 95 DPD breaches 90-day NPA rule
        res_npa = self.dil.rules_engine.evaluate_all({"days_past_due": 95}, jurisdiction="india")
        npa_rule = next(r for r in res_npa if r.rule_id == "RULE-IN-IRACP-NPA-001")
        self.assertFalse(npa_rule.passed)
        self.assertEqual(npa_rule.status, "REFER")

    def test_sme_nayak_working_capital(self):
        # Compliant SME scenario: 18% finance ratio, 6% margin equity, 1.40 DSCR
        compliant_params = {
            "bank_finance_turnover_ratio": 0.18,
            "margin_equity_ratio": 0.06,
            "dscr": 1.40,
        }
        res = self.dil.rules_engine.evaluate_all(compliant_params, jurisdiction="india")
        for r in res:
            self.assertTrue(r.passed, f"Rule {r.rule_id} should pass")

        # Non-compliant scenario: Over-leveraged working capital (25% bank finance, 3% margin, 1.05 DSCR)
        breach_params = {
            "bank_finance_turnover_ratio": 0.25,
            "margin_equity_ratio": 0.03,
            "dscr": 1.05,
        }
        res_breach = self.dil.rules_engine.evaluate_all(breach_params, jurisdiction="india")
        nayak_finance = next(r for r in res_breach if r.rule_id == "RULE-IN-NAYAK-MAX-BANK-FINANCE-001")
        nayak_margin = next(r for r in res_breach if r.rule_id == "RULE-IN-NAYAK-MIN-MARGIN-001")
        dscr_rule = next(r for r in res_breach if r.rule_id == "RULE-IN-COMMERCIAL-DSCR-001")

        self.assertFalse(nayak_finance.passed)
        self.assertEqual(nayak_finance.status, "FAIL")
        self.assertFalse(nayak_margin.passed)
        self.assertEqual(nayak_margin.status, "FAIL")
        self.assertFalse(dscr_rule.passed)
        self.assertEqual(dscr_rule.status, "REFER")

    def test_priority_sector_lending(self):
        # Bank with 42% PSL, 19% Agri, 8% Micro
        pass_res = self.dil.rules_engine.evaluate_all({
            "psl_advances_ratio": 0.42,
            "psl_agri_ratio": 0.19,
            "psl_micro_ratio": 0.08,
        }, jurisdiction="india")
        self.assertEqual(len(pass_res), 3)
        self.assertTrue(all(r.passed for r in pass_res))

        # Bank with PSL shortfall (36% PSL, 14% Agri)
        shortfall_res = self.dil.rules_engine.evaluate_all({
            "psl_advances_ratio": 0.36,
            "psl_agri_ratio": 0.14,
        }, jurisdiction="india")
        psl_overall = next(r for r in shortfall_res if r.rule_id == "RULE-IN-PSL-OVERALL-001")
        psl_agri = next(r for r in shortfall_res if r.rule_id == "RULE-IN-PSL-AGRI-001")
        self.assertFalse(psl_overall.passed)
        self.assertFalse(psl_agri.passed)

    def test_digital_lending_guidelines(self):
        # Uncompliant digital loan: disburse via pool account (False), no KFS (False), 1-day cooling off for 15-day loan
        res_fail = self.dil.rules_engine.evaluate_all({
            "direct_disbursal_to_borrower": False,
            "kfs_provided": False,
            "loan_tenure_days": 15,
            "cooling_off_days": 1,
        }, jurisdiction="india")
        self.assertEqual(len(res_fail), 3)
        self.assertTrue(all(not r.passed for r in res_fail))

    def test_deposits_and_gold_loan(self):
        # Gold loan exceeding 75% LTV cap
        res_gold = self.dil.rules_engine.evaluate_all({"gold_loan_ltv": 0.82}, jurisdiction="india")
        gold_rule = next(r for r in res_gold if r.rule_id == "RULE-IN-RBI-GOLD-LTV-001")
        self.assertFalse(gold_rule.passed)
        self.assertEqual(gold_rule.status, "FAIL")

        # Deposit under DICGC 5 Lakh limit
        res_dicgc = self.dil.rules_engine.evaluate_all({"insured_deposit_cap": 450000}, jurisdiction="india")
        dicgc_rule = next(r for r in res_dicgc if r.rule_id == "RULE-IN-DEPOSITS-DICGC-001")
        self.assertTrue(dicgc_rule.passed)

    def test_capital_adequacy(self):
        # Bank CRAR 11.5% passes 9%
        res_bank = self.dil.rules_engine.evaluate_all({"crar_ratio": 0.115}, jurisdiction="india")
        bank_rule = next(r for r in res_bank if r.rule_id == "RULE-IN-BANK-CRAR-001")
        self.assertTrue(bank_rule.passed)

        # HFC CRAR 13.0% fails 15% statutory threshold
        res_hfc = self.dil.rules_engine.evaluate_all({"hfc_crar_ratio": 0.13}, jurisdiction="india")
        hfc_rule = next(r for r in res_hfc if r.rule_id == "RULE-IN-HFC-CRAR-001")
        self.assertFalse(hfc_rule.passed)


if __name__ == "__main__":
    unittest.main()

