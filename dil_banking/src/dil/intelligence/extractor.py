from __future__ import annotations

import re
from typing import Any, Dict


def parse_indian_amount(val_str: str, multiplier_str: str = "") -> float:
    """Parses numeric expressions like '40', '40.5', '85k', '1.5 lakh', '2 crore' into float."""
    try:
        clean_num = re.sub(r"[^\d.]", "", val_str)
        if not clean_num:
            return 0.0
        val = float(clean_num)
        mult = multiplier_str.lower().strip()
        if "crore" in mult or "cr" in mult:
            return val * 10000000
        elif "lakh" in mult or "lac" in mult or mult == "l":
            return val * 100000
        elif "k" in mult or "thousand" in mult:
            return val * 1000
        return val
    except Exception:
        return 0.0


class ConversationalParameterExtractor:
    """
    Extracts financial parameters from conversational queries so users
    do not have to fill out separate form fields.
    """

    @staticmethod
    def extract(text: str) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        t = text.lower()

        # 1. CIBIL / Credit Score: e.g. "cibil is 750", "credit score of 720", "cibil 680"
        cibil_match = re.search(r"(?:cibil|credit\s+score)(?:\s+is|\s+of|\s*:)?\s*([3-9]\d{2})", t)
        if cibil_match:
            params["cibil_score"] = int(cibil_match.group(1))

        # 2. Applicant Age: e.g. "age is 32", "i am 29 years old", "age 28"
        age_match = re.search(r"(?:i\s+am\s+|age\s*(?:is|\s*:)?\s*)(1[8-9]|[2-7]\d)\s*(?:years|yr)?", t)
        if age_match:
            params["applicant_age"] = int(age_match.group(1))

        # 3. Monthly Income / Salary: e.g. "income is 85000", "salary 95k", "earn 85000", "salary of 80k"
        income_match = (
            re.search(r"(?:income|salary|earn(?:ing)?)\s*(?:of|is|:)?\s*(?:rs\.?|inr|₹)?\s*([\d,]+(?:\.\d+)?)\s*(lakh|lakhs|lac|lacs|cr|crore|k|thousand)?", t)
            or re.search(r"(?:rs\.?|inr|₹)?\s*([\d,]+(?:\.\d+)?)\s*(lakh|lakhs|lac|lacs|cr|crore|k|thousand)?\s*(?:salary|income)", t)
        )
        if income_match:
            num = income_match.group(1)
            mult = income_match.group(2) or ""
            val = parse_indian_amount(num, mult)
            if val > 0:
                params["monthly_income"] = val

        # 4. Existing EMI: e.g. "existing emi is 15000", "15000 emi", "emi of 12k", "15k emi"
        emi_match = (
            re.search(r"(?:existing|current|car|personal|other)?\s*emi\s*(?:of|is|:)?\s*(?:rs\.?|inr|₹)?\s*([\d,]+(?:\.\d+)?)\s*(lakh|lakhs|lac|k|thousand)?", t)
            or re.search(r"(?:rs\.?|inr|₹)?\s*([\d,]+(?:\.\d+)?)\s*(lakh|lakhs|lac|k|thousand)?\s*(?:existing|current)?\s*emi", t)
        )
        if emi_match:
            num = emi_match.group(1)
            mult = emi_match.group(2) or ""
            val = parse_indian_amount(num, mult)
            if val > 0 and val != params.get("monthly_income"):
                params["existing_emi"] = val

        # 5. Loan Amount Requested: e.g. "loan of 40 lakh", "40 lakh loan", "borrow 50 lakhs", "home loan 35 lakh"
        loan_match = (
            re.search(r"(?:loan\s+(?:of|amount|for)?|borrow|need)\s*(?:rs\.?|inr|₹)?\s*([\d,]+(?:\.\d+)?)\s*(lakh|lakhs|lac|lacs|cr|crore|k)?", t)
            or re.search(r"(?:rs\.?|inr|₹)?\s*([\d,]+(?:\.\d+)?)\s*(lakh|lakhs|lac|lacs|cr|crore|k)?\s*(?:home\s+)?loan", t)
        )
        if loan_match:
            num = loan_match.group(1)
            mult = loan_match.group(2) or ""
            val = parse_indian_amount(num, mult)
            if val >= 10000:
                params["loan_amount"] = val

        # 6. Property / Collateral Value: e.g. "property valued at 50 lakh", "50 lakh flat", "flat worth 60 lakhs"
        prop_match = (
            re.search(r"(?:property|flat|house|apartment|home|collateral)\s*(?:worth|cost|value|valued\s+at|of)?\s*(?:is|:)?\s*(?:rs\.?|inr|₹)?\s*([\d,]+(?:\.\d+)?)\s*(lakh|lakhs|lac|lacs|cr|crore)?", t)
            or re.search(r"(?:rs\.?|inr|₹)?\s*([\d,]+(?:\.\d+)?)\s*(lakh|lakhs|lac|lacs|cr|crore)?\s*(?:worth|cost|valued)?\s*(?:property|flat|house|apartment|collateral)", t)
        )
        if prop_match:
            num = prop_match.group(1)
            mult = prop_match.group(2) or ""
            val = parse_indian_amount(num, mult)
            if val >= 50000 and val != params.get("loan_amount"):
                params["property_value"] = val

        return params
