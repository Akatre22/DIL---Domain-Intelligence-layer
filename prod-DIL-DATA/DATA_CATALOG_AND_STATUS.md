# 🏦 Production DIL Banking Knowledge Master Catalog & Ingestion Tracker
**Objective:** 100% Comprehensive Coverage of Banking Domain Data (Regulatory, Retail, SME, Corporate, NPA, Deposits, Forex, Digital Lending & Compliance)

---

## 📊 Ingestion Progress & Codification Tracker

| Domain Category | Downloaded Official Artifacts & PDFs | Extracted Full Text | Phase 2 Codified Status in `dil_banking` |
| :--- | :--- | :--- | :--- |
| **01. Regulatory Master Directions** | • `Reserve-Bank-of-India-Housing-Finance-Companies-Directions-2025.pdf` (108 Pages, 760 KB)<br>• `RBI_Master_Directions_Priority_Sector_Lending_2025.html` (458 KB)<br>• `RBI_Master_Directions_Index.html` (797 KB)<br>• `RBI_Data_Portal_Home.html` | • `...Directions-2025_FULL_TEXT.md` (201 KB)<br>• `...Priority_Sector_Lending_2025_CLEAN.md` (90 KB)<br>• `RBI_Master_Directions_Directory.md` (133 Master Directions Indexed) | 🟢 **CODIFIED**: Tier 1/2/3 LTV caps, CRAR 9% (Banks) & 15% (HFCs), PSL 40% ANBC, 18% Agri, 7.5% Micro |
| **02. Retail Lending** | • `Retail_Credit_Underwriting_Policy_Comprehensive.md`<br>• (Covered under 108-page Housing Finance Directions above) | Full LTV, FOIR, CIBIL, Gold Loan 75% cap rules | 🟢 **CODIFIED**: LTV tiers, DTI <= 50%, Gold loan 75% LTV, CIBIL 700 prime cutoff |
| **03. SME & Commercial Credit** | • `SME_Working_Capital_Assessment_and_Schemes.md`<br>• (Covered under Priority Sector Lending Master Direction) | MSME criteria, Nayak 20% turnover method, Tandon MPBF | 🟢 **CODIFIED**: Nayak 20% MPBF, Nayak 5% margin equity, Term debt DSCR >= 1.20 |
| **04. Corporate & Consortium** | • `Corporate_Credit_Consortium_and_Project_Finance.md`<br>• `SEBI_Portal_Home.html` (Capital Markets & Debenture Norms) | Consortium, TRA waterfall, DSCR covenants, Project Finance | 🟢 **CODIFIED**: DSCR formula & thresholds, corporate loan underwriting concepts |
| **05. Deposits & NRI Banking** | • `Deposit_Accounts_NRI_Banking_and_TDS_Regulations.md` | DICGC ₹5L cover, Section 194A TDS, NRE/NRO/FCNR(B) | 🟢 **CODIFIED**: DICGC ₹5L statutory ceiling, Section 194A TDS rules, CASA concepts |
| **06. NPA, Recovery & Resolution** | • `Prudential_Norms_on_Income_Recognition...IRACP.md` | SMA-0/1/2 DPD triggers, 90-day NPA, Provisioning tables | 🟢 **CODIFIED**: SMA-2 (61-90 DPD), 90-day NPA trigger, 15% Substandard provision |
| **07. Digital Lending & Payments** | • `RBI_Guidelines_on_Digital_Lending_and_Customer_Protection.md` | Direct disbursals, KFS/APR mandate, cooling-off period | 🟢 **CODIFIED**: Direct account disbursal, mandatory KFS, min 3-day cooling-off |
| **08. Trade Finance & Forex** | • `RBI_Master_Direction_ECB_Trade_Credit.html` (280 KB)<br>• `Trade_Finance_LC_BG_and_Incoterms.md` | • `...ECB_Trade_Credit_CLEAN.md` (64 KB)<br>• UCP 600 rules, BG types, FEMA realization | 🟢 **CODIFIED**: LC & UCP 600 framework, Bank Guarantees (Financial & Performance) |
| **09. KYC, AML & Financial Crime** | • `RBI_Master_Direction_KYC_and_AML_Norms.md` | 6 OVDs, Risk refresh (2/8/10 yrs), Section 114B PAN, STR | 🟢 **CODIFIED**: Rule 114B PAN, 6 OVDs, CKYC registry, CTR & STR reporting |
| **10. Customer Protection & Ombudsman**| • `RBI_Integrated_Ombudsman_Scheme_and_Fair_Practices.md` | RB-IOS 2021, ₹20L compensation, ₹5,000/day delay penalty | 🟢 **CODIFIED**: RB-IOS 2021 terminology, customer protection dispute pathways |

---

## 📁 Repository File Tree (Total Ingested Data: ~2.8 MB of Verified Banking Text)

```
prod-DIL-Data/
├── DATA_CATALOG_AND_STATUS.md
├── download_data.py
├── 01_regulatory_master_directions/
│   ├── Reserve-Bank-of-India-Housing-Finance-Companies-Directions-2025.pdf    [108 Pages, 760 KB]
│   ├── Reserve-Bank-of-India-Housing-Finance-Companies-Directions-2025_FULL_TEXT.md [201 KB]
│   ├── RBI_Master_Directions_Priority_Sector_Lending_2025.html               [458 KB]
│   ├── RBI_Master_Directions_Priority_Sector_Lending_2025_CLEAN.md           [90 KB]
│   ├── RBI_Master_Directions_Index.html                                      [797 KB]
│   ├── RBI_Master_Directions_Directory.md                                    [133 Links]
│   ├── RBI_Data_Portal_Home.html                                             [51 KB]
│   └── RBI_Prudential_Norms_and_Capital_Adequacy.md                          [4.2 KB]
├── 02_retail_lending/
│   └── Retail_Credit_Underwriting_Policy_Comprehensive.md                    [4.8 KB]
├── 03_sme_and_commercial_credit/
│   └── SME_Working_Capital_Assessment_and_Schemes.md                         [3.4 KB]
├── 04_corporate_and_syndicated_lending/
│   ├── Corporate_Credit_Consortium_and_Project_Finance.md                    [3.0 KB]
│   └── SEBI_Portal_Home.html                                                 [55 KB]
├── 05_deposits_and_nri_banking/
│   └── Deposit_Accounts_NRI_Banking_and_TDS_Regulations.md                  [4.2 KB]
├── 06_npa_recovery_and_insolvency/
│   └── Prudential_Norms_on_Income_Recognition_Asset_Classification_and_Provisioning_IRACP.md [4.9 KB]
├── 07_digital_lending_and_payments/
│   └── RBI_Guidelines_on_Digital_Lending_and_Customer_Protection.md         [5.7 KB]
├── 08_trade_finance_and_forex/
│   ├── RBI_Master_Direction_ECB_Trade_Credit.html                            [280 KB]
│   ├── RBI_Master_Direction_ECB_Trade_Credit_CLEAN.md                       [64 KB]
│   └── Trade_Finance_LC_BG_and_Incoterms.md                                 [3.5 KB]
├── 09_kyc_aml_and_financial_crime/
│   └── RBI_Master_Direction_KYC_and_AML_Norms.md                            [4.7 KB]
└── 10_customer_protection_and_grievance/
    └── RBI_Integrated_Ombudsman_Scheme_and_Fair_Practices.md                [2.9 KB]
```
