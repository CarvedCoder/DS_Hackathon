"""Generate a diverse CSV of multi-step queries for hackathon submission."""

import csv
import io
import os
from typing import List, Dict


def _build_queries() -> List[Dict[str, str]]:
    """Return a list of query dictionaries spanning multiple domains."""
    return [
        {
            "Query Id": "1",
            "Query": "A 55-year-old diabetic patient presents with chest pain and an elevated troponin level. What differential diagnoses should be considered, and what immediate workup is required?",
            "Query Category": "Healthcare",
            "System Output": "Consider acute myocardial infarction, unstable angina, and pulmonary embolism. Order a 12-lead ECG, serial troponins, chest X-ray, and a CBC with metabolic panel.",
            "Remarks": "Multi-step clinical reasoning; follow-up needed on ECG interpretation and risk stratification."
        },
        {
            "Query Id": "2",
            "Query": "Our SaaS startup burned through 60% of its Series A in 8 months. How should we restructure our financial plan to extend runway to 18 months?",
            "Query Category": "Finance",
            "System Output": "Reduce non-essential SG&A by 25%, renegotiate cloud-hosting contracts, defer non-critical hires, and explore bridge financing or revenue-based lending.",
            "Remarks": "Requires follow-up cash-flow projection and scenario analysis under different revenue assumptions."
        },
        {
            "Query Id": "3",
            "Query": "An employee was terminated after reporting safety violations. Under OSHA's whistleblower protection statutes, what legal remedies are available?",
            "Query Category": "Legal",
            "System Output": "The employee may file a complaint with OSHA within 30 days, seek reinstatement, back pay, and compensatory damages under Section 11(c) of the OSH Act.",
            "Remarks": "Follow-up needed on state-specific anti-retaliation statutes and burden-of-proof requirements."
        },
        {
            "Query Id": "4",
            "Query": "Design a blended-learning curriculum for a graduate-level data-science programme that balances theory and hands-on projects across two semesters.",
            "Query Category": "Education",
            "System Output": "Semester 1 covers statistics, linear algebra, and Python programming with weekly labs. Semester 2 introduces ML, deep learning, and a capstone project with industry partners.",
            "Remarks": "Complexity in aligning learning outcomes with industry needs; follow-up on assessment rubrics and accreditation requirements."
        },
        {
            "Query Id": "5",
            "Query": "Plan a 14-day multi-city itinerary across Japan for a family of four with a moderate budget, including cultural experiences and kid-friendly activities.",
            "Query Category": "Travel",
            "System Output": "Days 1-4 Tokyo (Akihabara, Ueno Zoo, teamLab), Days 5-7 Hakone (hot springs, Open-Air Museum), Days 8-10 Kyoto (temples, bamboo grove), Days 11-14 Osaka (Universal Studios, street food tour).",
            "Remarks": "Follow-up needed on JR Pass cost-benefit, hotel bookings, and seasonal weather considerations."
        },
        {
            "Query Id": "6",
            "Query": "Evaluate the effectiveness of carbon-capture-and-storage (CCS) technology in reducing industrial CO2 emissions by 2035.",
            "Query Category": "Climate",
            "System Output": "Current CCS projects capture ~40 Mt CO2/year. Scaling to 1 Gt/year by 2035 requires $100B+ investment, improved sorbent efficiency, and supportive carbon-pricing policies.",
            "Remarks": "Assumes continued policy support; follow-up on lifecycle energy penalty and long-term geological storage risks."
        },
        {
            "Query Id": "7",
            "Query": "Our network logs show lateral movement from a compromised endpoint. Outline an incident-response plan to contain and remediate the breach.",
            "Query Category": "Cybersecurity",
            "System Output": "Isolate the affected subnet, revoke compromised credentials, deploy EDR scans across all endpoints, collect forensic images, and notify the CISO for regulatory-disclosure assessment.",
            "Remarks": "Multi-step IR process; follow-up needed on root-cause analysis and post-incident hardening measures."
        },
        {
            "Query Id": "8",
            "Query": "We are launching a B2B project-management tool. Define a go-to-market strategy that prioritises product-led growth with a freemium tier.",
            "Query Category": "Product Management",
            "System Output": "Offer a free tier for up to 5 users, gate advanced analytics and integrations behind a paid plan, invest in self-serve onboarding, and leverage in-app referral loops.",
            "Remarks": "Follow-up on pricing experiments, conversion-funnel metrics, and competitive positioning against Asana/Monday."
        },
        {
            "Query Id": "9",
            "Query": "Our warehouse fulfillment error rate has risen from 0.5% to 2.3% over the past quarter. Diagnose likely root causes and recommend corrective actions.",
            "Query Category": "Operations",
            "System Output": "Likely causes include pick-path changes after layout reorganisation, new temporary staff without adequate training, and barcode-scanner firmware issues. Recommend retraining, scanner audits, and a revised QC checkpoint.",
            "Remarks": "Requires follow-up Pareto analysis on error types and shift-level performance data."
        },
        {
            "Query Id": "10",
            "Query": "Design a competency-based performance-review framework for a 200-person engineering organisation transitioning from annual to quarterly reviews.",
            "Query Category": "HR",
            "System Output": "Define 5 core competencies (technical depth, collaboration, delivery, mentorship, innovation), use a 1-5 rubric, pair with quarterly OKRs, and include 360-degree peer feedback.",
            "Remarks": "Follow-up needed on calibration sessions, manager training, and HRIS tool integration."
        },
        {
            "Query Id": "11",
            "Query": "Given a dataset of 10M e-commerce transactions, outline a pipeline to detect fraudulent orders in near real-time.",
            "Query Category": "Data Analysis",
            "System Output": "Ingest events via Kafka, compute velocity features in Flink, score with an XGBoost model, and route high-risk orders to a manual-review queue with an SLA of < 5 minutes.",
            "Remarks": "Assumes existing feature store; follow-up on model retraining cadence and false-positive rate targets."
        },
        {
            "Query Id": "12",
            "Query": "A customer reports being double-charged for a subscription renewal. Walk through the resolution steps and root-cause investigation.",
            "Query Category": "Customer Support",
            "System Output": "Verify the duplicate charge in the billing system, issue an immediate refund for the extra charge, check the payment-gateway logs for retry storms, and escalate to engineering if a systemic bug is found.",
            "Remarks": "Follow-up needed on customer communication template and billing-system idempotency fix."
        },
        {
            "Query Id": "13",
            "Query": "A patient on warfarin therapy presents with an INR of 8.5 and minor gum bleeding. What is the appropriate management protocol?",
            "Query Category": "Healthcare",
            "System Output": "Hold warfarin, administer oral vitamin K 2.5 mg, recheck INR in 24 hours, and evaluate for occult bleeding. Resume warfarin at a reduced dose once INR is in range.",
            "Remarks": "Requires consideration of patient's indication for anticoagulation; follow-up on bridging therapy decisions."
        },
        {
            "Query Id": "14",
            "Query": "Compare the risk-adjusted returns of a 60/40 equity-bond portfolio versus a risk-parity strategy over the last 20 years.",
            "Query Category": "Finance",
            "System Output": "Risk-parity delivered a higher Sharpe ratio (0.85 vs 0.62) with lower max drawdown, but required leverage and had higher turnover costs.",
            "Remarks": "Assumptions include constant rebalancing and ignoring tax drag; follow-up on tail-risk analysis."
        },
        {
            "Query Id": "15",
            "Query": "Draft a GDPR-compliant data-processing agreement (DPA) checklist for onboarding a new third-party analytics vendor.",
            "Query Category": "Legal",
            "System Output": "Checklist items: purpose limitation clause, sub-processor disclosure, data-breach notification SLA (72 hours), data-subject rights facilitation, cross-border transfer safeguards (SCCs), and audit rights.",
            "Remarks": "Follow-up on vendor's specific processing activities and DPO review sign-off."
        },
        {
            "Query Id": "16",
            "Query": "Propose an adaptive-learning system that personalises math instruction for K-8 students based on real-time formative assessments.",
            "Query Category": "Education",
            "System Output": "Use item-response theory to estimate mastery, adjust problem difficulty dynamically, provide scaffolded hints after two incorrect attempts, and surface teacher dashboards with learning-gap heatmaps.",
            "Remarks": "Requires pilot study data; follow-up on content alignment with Common Core standards."
        },
        {
            "Query Id": "17",
            "Query": "Assess the infrastructure resilience of a coastal city to a Category 4 hurricane under current and projected 2050 sea-level-rise scenarios.",
            "Query Category": "Climate",
            "System Output": "Current flood defences protect against 3 m storm surge; a Category 4 event generates 5-6 m surge. Under 2050 projections (+0.5 m SLR), inundation area increases by 35%. Recommend upgrading levees and adopting managed-retreat zoning.",
            "Remarks": "Depends on RCP scenario chosen; follow-up on evacuation logistics and insurance-cost modelling."
        },
        {
            "Query Id": "18",
            "Query": "A zero-day vulnerability in our API gateway has been publicly disclosed. What immediate and medium-term actions should the security team take?",
            "Query Category": "Cybersecurity",
            "System Output": "Immediately apply the vendor's emergency patch or deploy a WAF virtual-patch rule, rotate API keys, audit access logs for exploitation evidence, and communicate status to affected customers.",
            "Remarks": "Follow-up on CVE scoring, penetration re-test, and long-term vendor-risk reassessment."
        },
        {
            "Query Id": "19",
            "Query": "Prioritise the next quarter's feature backlog for a mobile banking app using the RICE framework, given five candidate features.",
            "Query Category": "Product Management",
            "System Output": "Ranked: (1) biometric login (Reach=90%, Impact=High), (2) instant P2P transfers, (3) spending-insights dashboard, (4) virtual card issuance, (5) crypto-wallet integration.",
            "Remarks": "Scores assume current user-research data; follow-up on effort estimates and engineering capacity."
        },
        {
            "Query Id": "20",
            "Query": "Design a demand-forecasting model for a grocery chain with 150 stores to optimise perishable-goods inventory.",
            "Query Category": "Operations",
            "System Output": "Use a hierarchical time-series model (e.g., LightGBM with store-SKU granularity), incorporate weather and promotional calendars, and set dynamic safety-stock levels per category.",
            "Remarks": "Assumes 3 years of POS history; follow-up on cold-start handling for new SKUs and shrinkage metrics."
        },
        {
            "Query Id": "21",
            "Query": "Develop a diversity-hiring strategy to increase underrepresented-group representation in engineering roles from 18% to 30% within two years.",
            "Query Category": "HR",
            "System Output": "Partner with HBCUs and coding bootcamps, implement blind resume screening, set diverse-slate requirements for final-round interviews, and track quarterly cohort-retention data.",
            "Remarks": "Follow-up on bias-audit of existing ATS, mentorship programme design, and legal compliance with affirmative-action guidelines."
        },
        {
            "Query Id": "22",
            "Query": "Analyse churn patterns in a telecom dataset with 5M subscribers. Identify the top predictive features and recommend a retention campaign.",
            "Query Category": "Data Analysis",
            "System Output": "Top features: contract type, monthly charges, tenure, tech-support calls, and data overages. A gradient-boosted model achieves AUC 0.89. Target at-risk users with personalised discount offers 30 days before contract end.",
            "Remarks": "Follow-up on A/B testing the retention offers and measuring incremental lift."
        },
        {
            "Query Id": "23",
            "Query": "A high-value enterprise client threatens to churn due to repeated SLA breaches. Outline a recovery playbook.",
            "Query Category": "Customer Support",
            "System Output": "Assign a dedicated account manager, conduct a root-cause review of SLA breaches, offer a service-credit package, co-create an improvement plan with defined milestones, and schedule weekly check-ins for 90 days.",
            "Remarks": "Follow-up on contractual SLA renegotiation and executive-sponsor involvement."
        },
        {
            "Query Id": "24",
            "Query": "Design a microservices architecture for a real-time ride-sharing platform that handles 50K concurrent ride requests.",
            "Query Category": "Software Engineering",
            "System Output": "Decompose into services: ride-matching, pricing, driver-location (using geospatial indexing), payments, and notifications. Use Kafka for event streaming, Redis for caching, and Kubernetes for auto-scaling.",
            "Remarks": "Follow-up on service-mesh configuration, circuit-breaker policies, and disaster-recovery strategy."
        },
        {
            "Query Id": "25",
            "Query": "Evaluate the ROI of deploying IoT sensors across a 500-acre precision-agriculture farm for yield optimisation.",
            "Query Category": "Agriculture",
            "System Output": "Deploying soil-moisture, temperature, and NDVI sensors costs ~$120K. Expected yield increase of 12-18% in the first season translates to $200K+ additional revenue, yielding a payback period under 12 months.",
            "Remarks": "Assumptions include reliable connectivity; follow-up on sensor maintenance costs and data-integration with existing farm-management software."
        },
        {
            "Query Id": "26",
            "Query": "A manufacturing plant experiences a 15% increase in defect rate after switching raw-material suppliers. Perform a root-cause analysis.",
            "Query Category": "Operations",
            "System Output": "Conduct incoming-material inspection, compare tensile-strength and impurity specs, run a designed experiment (DOE) on the production line, and evaluate whether retooling is needed for the new material.",
            "Remarks": "Follow-up on supplier audit, corrective-action request, and lot-traceability for affected batches."
        },
        {
            "Query Id": "27",
            "Query": "Develop a compliance monitoring framework for anti-money-laundering (AML) regulations in a digital payments company.",
            "Query Category": "Finance",
            "System Output": "Implement transaction-monitoring rules (velocity checks, structuring detection), KYC/KYB verification at onboarding, suspicious-activity report (SAR) workflows, and quarterly independent audits.",
            "Remarks": "Follow-up on jurisdiction-specific thresholds and integration with FinCEN/FCA reporting systems."
        },
        {
            "Query Id": "28",
            "Query": "A school district wants to reduce chronic absenteeism by 20%. Propose a data-driven intervention programme.",
            "Query Category": "Education",
            "System Output": "Build an early-warning model using attendance, grades, and demographic data. Deploy tiered interventions: automated parent notifications (Tier 1), mentorship assignments (Tier 2), and home visits with social-worker support (Tier 3).",
            "Remarks": "Follow-up on FERPA compliance for student data use and programme effectiveness measurement."
        },
        {
            "Query Id": "29",
            "Query": "Assess the cybersecurity posture of a mid-size hospital network and recommend a 12-month hardening roadmap.",
            "Query Category": "Cybersecurity",
            "System Output": "Current gaps: unpatched medical devices, flat network architecture, no MFA on EHR access. Roadmap: Q1 network segmentation, Q2 MFA rollout, Q3 endpoint detection, Q4 tabletop exercises and staff training.",
            "Remarks": "HIPAA compliance constraints; follow-up on medical-device vendor coordination and budget approval."
        },
        {
            "Query Id": "30",
            "Query": "Analyse sentiment trends across 1M customer reviews for a consumer electronics brand and recommend product improvements.",
            "Query Category": "Data Analysis",
            "System Output": "Negative sentiment clusters around battery life (32%) and software bugs (28%). Positive sentiment highlights camera quality and design. Recommend prioritising battery optimisation and a dedicated QA sprint for the next firmware release.",
            "Remarks": "Follow-up on aspect-level sentiment model accuracy and competitive benchmarking."
        },
    ]


def generate_queries_csv(output_path: str = "queries.csv") -> str:
    """Generate the hackathon-submission CSV and return its content as a string.

    Parameters
    ----------
    output_path : str, optional
        File path where the CSV will be written.  Defaults to ``"queries.csv"``.

    Returns
    -------
    str
        The full CSV content that was written to *output_path*.
    """
    fieldnames = [
        "Query Id",
        "Query",
        "Query Category",
        "System Output",
        "Remarks",
    ]

    queries = _build_queries()

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(queries)
    content = buf.getvalue()

    with open(output_path, "w", newline="", encoding="utf-8") as fh:
        fh.write(content)

    return content


if __name__ == "__main__":
    csv_text = generate_queries_csv()
    print(csv_text)
