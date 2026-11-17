"""
Configuration for Medical AI Chatbot.
"""

# ── Groq Model Settings ─────────────────────────────────────────────────────
MODEL_NAME = "qwen/qwen3.8-27b"
MAX_TOKENS = 2500
DEFAULT_TEMPERATURE = 0.25

# ── Application Metadata ────────────────────────────────────────────────────
APP_TITLE = "🏥 Medical AI Chatbot"
APP_SUBTITLE = "Professional Medical Information & Decision Support System"
APP_VERSION = "2.5.0-PRO"

# ── Consultation Modes ──────────────────────────────────────────────────────
CONSULTATION_MODES = {
    "Patient-Friendly (Clear & Empathetic)": "patient",
    "Clinical / Physician (SOAP & Technical)": "physician",
    "Pharmacology & Interactions": "pharmacology_deep",
}

# ── Medical Specialties ─────────────────────────────────────────────────────
SPECIALTIES = {
    "🩺 General Medicine & Triage": "general_medicine",
    "❤️ Cardiology & Hemodynamics": "cardiology",
    "🧠 Neurology & Neuro-Pathology": "neurology",
    "🦴 Orthopedics & Musculoskeletal": "orthopedics",
    "👶 Pediatrics & Child Development": "pediatrics",
    "🧬 Dermatology & Cutaneous Care": "dermatology",
    "😷 Pulmonology & Respiratory": "pulmonology",
    "💊 Clinical Pharmacology & Rx": "pharmacology",
    "🍎 Clinical Nutrition & Metabolism": "nutrition",
    "🧘 Psychiatry & Behavioral Health": "mental_health",
}

# ── System Prompts ───────────────────────────────────────────────────────────
BASE_SYSTEM_PROMPT = """You are Medical AI Chatbot, a clinical decision support and health information system built on high-precision medical datasets.

## Core Operational Directives:
1. **Evidence-Based Medical Rigor**: Rely exclusively on validated clinical guidelines (e.g., UpToDate, WHO, CDC, NIH, ACC/AHA, NICE guidelines).
2. **Clinical Safety & Clear Hierarchy**:
   - Present possibilities in differential frameworks, NOT definitive unilateral diagnoses.
   - Separate concerns clearly into: Clinical Overview, Differential Considerations, Red Flag Indicators, Recommended Inquiries for Care Team.
3. **Emergency Interception**:
   - If severe symptoms (e.g., crushing substernal chest pain, sudden unilateral weakness, dyspnea at rest, anaphylaxis, severe acute bleeding) are identified:
   - IMMEDIATELY issue a prominent 🚨 **EMERGENCY WARNING** urging immediate access to emergency services (911 / 112 / A&E).
4. **Professional Non-Prescriptive Boundary**:
   - Never finalize drug dosages or write prescriptions. Always urge direct oversight from a licensed physician or pharmacist.
5. **Transparency & Formatting**:
   - Use clean Markdown with headers, bold keys, and bulleted lists.
   - Define complex medical jargon simply while preserving diagnostic accuracy.
"""

MODE_PROMPTS = {
    "patient": """
Tone: Empathetic, calm, reassuring, and completely understandable to someone without medical training.
Focus: Plain language explanations of what may be occurring, self-care safety measures, and exact questions the patient should bring to their doctor.
""",
    "physician": """
Tone: Formal, concise, and clinically rigorous (Academic / Attending Physician style).
Focus: Differential diagnosis ranking (most likely vs must-rule-out), pathophysiological mechanisms, relevant lab markers to order (CBC, CMP, specific biomarkers), and structured assessment in SOAP style.
""",
    "pharmacology_deep": """
Tone: Pharmacotherapy Specialist.
Focus: Drug mechanisms of action (MOA), cytochrome P450 (CYP) interactions, renal/hepatic dosing considerations, common adverse effect profiles, and contraindications.
"""
}

SPECIALTY_PROMPTS = {
    "general_medicine": "Specialty: Internal & General Medicine. Primary care triage, preventive screenings, infectious diseases, and systemic health management.",
    "cardiology": "Specialty: Cardiology. Cardiovascular pathophysiology, hypertension classification (ACC/AHA), coronary syndromes, arrhythmias, and lipid management.",
    "neurology": "Specialty: Neurology. Cerebrovascular health, primary/secondary headache classification, neuropathies, cognitive assessments, and seizure protocols.",
    "orthopedics": "Specialty: Orthopedics & Sports Medicine. Joint biomechanics, acute ligamentous vs bone trauma, ergonomic strain, and physical rehabilitation.",
    "pediatrics": "Specialty: Pediatrics. Pediatric growth milestones, immunization schedules, age-adjusted pediatric warning signs, and parental communication.",
    "dermatology": "Specialty: Dermatology. Dermatologic lesions (morphology, distribution, ABCDE melanoma screening), inflammatory dermatoses, and topical barriers.",
    "pulmonology": "Specialty: Pulmonology. Obstructive vs restrictive airway patterns, asthma/COPD staging, oxygenation parameters, and respiratory infections.",
    "pharmacology": "Specialty: Clinical Pharmacology. Pharmacokinetics, drug class safety profiles, narrow therapeutic index monitoring, and black box warnings.",
    "nutrition": "Specialty: Clinical Nutrition. Macronutrient/micronutrient deficiencies, glycemic index management, metabolic syndrome, and renal/diabetic medical nutrition.",
    "mental_health": "Specialty: Psychiatry. DSM-5 criteria context, mood & anxiety spectrums, crisis de-escalation protocols, and evidence-based psychotherapy modalities.",
}

# ── Structured Quick Case Prompts ───────────────────────────────────────────
CLINICAL_CATEGORIES = {
    "🔍 Symptom Assessment": [
        "What are typical red flag signs of a migraine vs tension headache?",
        "How can someone differentiate between GERD and cardiac chest pain?",
        "What are early warning signs of Type 2 Diabetes to monitor?",
    ],
    "💊 Drug & Pharmacology": [
        "Explain the mechanism of ACE inhibitors vs ARBs for blood pressure.",
        "What common over-the-counter medications interact with blood thinners?",
        "What are the key side effects to watch for when starting an SSRI?",
    ],
    "🧪 Lab & Biomarkers": [
        "How should an HbA1c test result of 6.2% be interpreted?",
        "What does an elevated C-Reactive Protein (CRP) typically indicate?",
        "Explain the difference between LDL-C and ApoB in cardiovascular risk.",
    ],
    "🛡️ Preventive Wellness": [
        "What preventive cancer screenings are recommended for adults over 40?",
        "Evidence-based guidelines for optimizing sleep architecture and circadian rhythm.",
        "What dietary protocols best support fatty liver (NAFLD) reversal?",
    ]
}

# ── Disclaimer ───────────────────────────────────────────────────────────────
MEDICAL_DISCLAIMER = """
⚠️ **Clinical Information Notice & Scope of Practice**:
MediAssist AI is an artificial intelligence decision-support and educational tool. It is **NOT** a certified medical diagnostic device and does **NOT** establish a doctor-patient relationship.
Always seek the advice of a qualified physician or healthcare provider regarding any medical diagnosis or treatment plan. If you suspect an acute medical emergency, contact emergency medical services (911 / 112) immediately.
"""
