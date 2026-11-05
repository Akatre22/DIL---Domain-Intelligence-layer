# RBI Guidelines on Digital Lending & Customer Protection in Electronic Banking Transactions

**Regulatory References:**  
1. Digital Lending: RBI/2022-23/111 DOR.CRE.REC.66/21.07.001/2022-23  
2. Customer Protection (Unauthorized Electronic Transactions): RBI/2017-18/15 DBR.No.Leg.BC.78/09.07.005/2017-18  

---

## 1. Digital Lending Architecture & Mandatory Rules

These directions govern commercial banks and NBFCs partnering with Fintech Lending Service Providers (LSPs) operating Digital Lending Apps (DLAs).

### 1.1 Direct Disbursal & Repayment Rule (No Pass-Through Accounts)
- All loan disbursements and repayments **must be executed directly between the bank account of the regulated lender and the bank account of the borrower**.
- Under no circumstances can loan funds pass through any pool, nodal, or escrow account controlled by the Fintech LSP or third-party intermediary.

### 1.2 Key Fact Statement (KFS) & Annual Percentage Rate (APR)
- Every borrower must be provided a standardized, simple **Key Fact Statement (KFS)** before the loan contract is executed.
- The KFS must clearly disclose the **Annual Percentage Rate (APR)**—representing the true total cost of credit including the base interest rate, all upfront processing fees, documentation charges, and third-party recovery costs.
- *Rule:* Any fee, charge, or penalty not explicitly listed in the KFS **cannot be recovered** from the borrower under any pretext.

### 1.3 Mandatory Cooling-off / Look-up Period
- Borrowers must be provided a defined exit window (Cooling-off Period) within which they can cancel the loan facility without paying any prepayment penalty:
  - Loans with tenure $\ge 7\text{ days}$: Minimum **3 calendar days** look-up period.
  - Loans with tenure $\ge 1\text{ year}$: Minimum **1 calendar day** look-up period.
- The borrower only returns the principal disbursed plus proportionate interest for the elapsed days.

### 1.4 Prohibition on Automatic Credit Limit Hikes
- Regulated entities and apps are **strictly prohibited from automatically increasing credit limits** or pre-approving loan top-ups without obtaining explicit, affirmative consent from the borrower for each revision.

---

## 2. Customer Protection: Limiting Liability in Unauthorized Electronic Banking Transactions

When a customer falls victim to electronic fraud (phishing, unauthorized UPI, ATM skimming, fraudulent net-banking transfer), liability is distributed based on reporting timelines:

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│              CUSTOMER LIABILITY IN UNAUTHORIZED ELECTRONIC TRANSACTIONS           │
├─────────────────────────┬─────────────────────────────────────────────────────────┤
│ Notification Timeline   │ Maximum Customer Liability                              │
├─────────────────────────┼─────────────────────────────────────────────────────────┤
│ Contributory Fraud /    │ ZERO LIABILITY                                          │
│ Bank's Internal Negligence│ (Bank must reverse amount regardless of reporting time) │
├─────────────────────────┼─────────────────────────────────────────────────────────┤
│ Third-Party Breach      │ ZERO LIABILITY                                          │
│ (Reported within 3 days)│ Full refund credited to customer within 10 working days │
├─────────────────────────┼─────────────────────────────────────────────────────────┤
│ Reported within         │ CAPPED LIABILITY                                        │
│ 4 to 7 working days     │ • Basic Savings (BSBD): Max ₹5,000                      │
│                         │ • Savings / Cards limit < ₹5L: Max ₹10,000               │
│                         │ • Current / Credit Cards limit > ₹5L: Max ₹25,000       │
├─────────────────────────┼─────────────────────────────────────────────────────────┤
│ Reported beyond         │ As per the Bank's Board-approved customer policy        │
│ 7 working days          │                                                         │
└─────────────────────────┴─────────────────────────────────────────────────────────┘
```

### Shadow Reversal Mandate (10-Day Rule)
The bank must credit the disputed amount back to the customer's account (shadow credit) **within 10 working days** from the date of the customer reporting the unauthorized transaction, even while the forensic investigation remains underway.

