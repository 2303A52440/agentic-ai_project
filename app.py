"""
Medical AI Chatbot — Clinical Decision Support & Medical Intelligence
Built with Streamlit + Groq LPU Inference (Qwen 3.8 27B)
"""

import streamlit as st
from datetime import datetime
import json

from config import (
    APP_TITLE,
    APP_SUBTITLE,
    APP_VERSION,
    MODEL_NAME,
    SPECIALTIES,
    CONSULTATION_MODES,
    CLINICAL_CATEGORIES,
    MEDICAL_DISCLAIMER,
    DEFAULT_TEMPERATURE,
)
from llm_client import MedicalLLMClient
from styles import get_custom_css

# ── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Medical AI Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply Clinical Custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)


# ── State Initialization ─────────────────────────────────────────────────────
def init_session_state():
    defaults = {
        "messages": [],
        "specialty": "general_medicine",
        "consultation_mode": "patient",
        "temperature": DEFAULT_TEMPERATURE,
        "client": None,
        "client_error": None,
        "chat_started": False,
        "session_start": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "soap_note": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.client is None and st.session_state.client_error is None:
        try:
            st.session_state.client = MedicalLLMClient()
        except Exception as e:
            st.session_state.client_error = str(e)


init_session_state()


# ── Sidebar: Clinical Controls & Telemetry ───────────────────────────────────
with st.sidebar:
    st.markdown(
        f"""
        <div class="sidebar-brand">🏥 Medical AI Chatbot</div>
        <div class="sidebar-version">RELEASE {APP_VERSION}</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🔬 Specialty Department")
    selected_spec_label = st.selectbox(
        "Department:",
        list(SPECIALTIES.keys()),
        index=0,
        label_visibility="collapsed",
    )
    st.session_state.specialty = SPECIALTIES[selected_spec_label]

    st.markdown("### 🎭 Persona / Protocol")
    selected_mode_label = st.selectbox(
        "Consultation Output Persona:",
        list(CONSULTATION_MODES.keys()),
        index=0,
        label_visibility="collapsed",
    )
    st.session_state.consultation_mode = CONSULTATION_MODES[selected_mode_label]

    st.markdown("---")

    # Developer LLM Parameters
    st.markdown("### ⚙️ Inference Telemetry")
    temp_val = st.slider(
        "Temperature (Clinical Rigor):",
        min_value=0.0,
        max_value=0.7,
        value=st.session_state.temperature,
        step=0.05,
        help="Lower values yield strict adherence to clinical guidelines. Higher values allow broader descriptive analogies.",
    )
    st.session_state.temperature = temp_val

    st.markdown(
        f"""
        <div class="sidebar-card">
            <h4>Engine Telemetry</h4>
            <div style="font-size: 0.8rem; line-height: 1.6; color: #E2E8F0;">
                • <strong>Model:</strong> {MODEL_NAME}<br>
                • <strong>Hardware:</strong> Groq LPU Accelerator<br>
                • <strong>Inference:</strong> ~350 tokens/sec<br>
                • <strong>Messages:</strong> {len(st.session_state.messages)}<br>
                • <strong>Session:</strong> {st.session_state.session_start}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Session Management
    col_clear, col_export = st.columns(2)
    with col_clear:
        if st.button("🗑️ Reset Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat_started = False
            st.session_state.soap_note = None
            st.rerun()

    with col_export:
        if st.session_state.messages:
            transcript = f"# Medical AI Chatbot Consultation Transcript\nSession Date: {st.session_state.session_start}\nSpecialty: {selected_spec_label}\nMode: {selected_mode_label}\n\n"
            for msg in st.session_state.messages:
                transcript += f"### {msg['role'].upper()}:\n{msg['content']}\n\n"
            transcript += f"\n---\n{MEDICAL_DISCLAIMER}"

            st.download_button(
                label="📥 Export",
                data=transcript,
                file_name=f"clinical_consultation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True,
            )

    st.markdown("---")
    st.markdown(
        """
        <div class="sidebar-card" style="border-left: 3px solid #EF4444;">
            <h4 style="color: #F87171 !important;">🚨 Crisis Contacts</h4>
            <div style="font-size: 0.775rem; color: #CBD5E1;">
                • Emergency Services: <strong>911 / 112</strong><br>
                • Suicide &amp; Crisis Lifeline: <strong>988</strong><br>
                • Poison Control Center: <strong>1-800-222-1222</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Top Clinical Header Banner ───────────────────────────────────────────────
st.markdown(
    f"""
    <div class="clinical-banner">
        <div class="clinical-banner-left">
            <h1>{APP_TITLE}</h1>
            <p>{APP_SUBTITLE} • Department: <strong>{selected_spec_label}</strong></p>
        </div>
        <div class="clinical-banner-right">
            <div class="telemetry-chip telemetry-chip-live">
                <span class="chip-dot"></span> GROQ LPU ONLINE
            </div>
            <div class="telemetry-chip">
                <span>MODEL:</span> {MODEL_NAME}
            </div>
            <div class="telemetry-chip">
                <span>TEMP:</span> {st.session_state.temperature}
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)



# API Configuration Error Guard
if st.session_state.client_error:
    st.error(f"**Configuration Notice:** {st.session_state.client_error}")
    st.stop()


# ── Main Application Tabs ────────────────────────────────────────────────────
tab_consult, tab_soap, tab_calc, tab_triage = st.tabs([
    "💬 Clinical Consultation",
    "📋 SOAP Note Generator",
    "⚖️ Clinical Calculators",
    "🚨 Emergency Triage Protocol",
])


# ═════════════════════════════════════════════════════════════════════════════
# TAB 1: Clinical Consultation & Streaming Dialogue
# ═════════════════════════════════════════════════════════════════════════════
with tab_consult:
    # Quick Case Exploration chips (shown when conversation is fresh)
    if not st.session_state.chat_started:
        st.markdown("#### ⚡ Clinical Inquiries & Case Starters")
        cat_cols = st.columns(len(CLINICAL_CATEGORIES))

        for col_idx, (cat_name, questions) in enumerate(CLINICAL_CATEGORIES.items()):
            with cat_cols[col_idx]:
                st.markdown(f"**{cat_name}**")
                for q_idx, question in enumerate(questions):
                    if st.button(question, key=f"q_{col_idx}_{q_idx}", use_container_width=True):
                        st.session_state.messages.append({"role": "user", "content": question})
                        st.session_state.chat_started = True
                        st.rerun()

        st.markdown("---")

    # Display Existing Message History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🧑‍⚕️" if msg["role"] == "user" else "🏥"):
            st.markdown(msg["content"])

    # Chat Input Box
    if prompt := st.chat_input("Enter clinical symptoms, lab findings, or pharmacotherapy query..."):
        st.session_state.chat_started = True
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user", avatar="🧑‍⚕️"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🏥"):
            with st.spinner("Synthesizing clinical response via Groq LPU..."):
                response_stream = st.session_state.client.get_response(
                    user_message=prompt,
                    chat_history=st.session_state.messages[:-1],
                    specialty=st.session_state.specialty,
                    mode=st.session_state.consultation_mode,
                    temperature=st.session_state.temperature,
                )

                if isinstance(response_stream, str):
                    st.error(response_stream)
                    full_response = response_stream
                else:
                    full_response = st.write_stream(
                        (
                            chunk.choices[0].delta.content or ""
                            for chunk in response_stream
                            if chunk.choices[0].delta.content
                        )
                    )

        st.session_state.messages.append({"role": "assistant", "content": full_response})


# ═════════════════════════════════════════════════════════════════════════════
# TAB 2: Automated SOAP Note Synthesis
# ═════════════════════════════════════════════════════════════════════════════
with tab_soap:
    st.markdown("### 📋 Automated Clinical Encounter Synthesizer (SOAP)")
    st.markdown(
        "Compile the ongoing dialogue into an organized, physician-grade **SOAP Note** "
        "(Subjective, Objective, Assessment, Plan) for clinical documentation."
    )

    if not st.session_state.messages:
        st.info("Start a consultation in the **Clinical Consultation** tab to generate a SOAP note from the dialogue.")
    else:
        if st.button("⚡ Generate Clinical SOAP Note from Current Encounter", type="primary"):
            with st.spinner("Compiling structured SOAP note..."):
                st.session_state.soap_note = st.session_state.client.generate_soap_note(
                    st.session_state.messages
                )

        if st.session_state.soap_note:
            st.markdown("---")
            st.markdown(st.session_state.soap_note)
            st.download_button(
                label="📥 Download SOAP Note (.md)",
                data=st.session_state.soap_note,
                file_name=f"SOAP_Note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
            )


# ═════════════════════════════════════════════════════════════════════════════
# TAB 3: Clinical Calculators & Decision Tools
# ═════════════════════════════════════════════════════════════════════════════
with tab_calc:
    st.markdown("### ⚖️ Clinical Formulas & Physiological Estimators")
    calc_col1, calc_col2 = st.columns(2)

    with calc_col1:
        st.markdown("#### 1. Body Mass Index (BMI) & Classification")
        weight_kg = st.number_input("Weight (kg):", min_value=10.0, max_value=300.0, value=70.0, step=0.5)
        height_cm = st.number_input("Height (cm):", min_value=50.0, max_value=250.0, value=175.0, step=1.0)

        height_m = height_cm / 100.0
        bmi = round(weight_kg / (height_m ** 2), 1)

        if bmi < 18.5:
            bmi_cat = "Underweight (< 18.5)"
            cat_color = "#3B82F6"
        elif 18.5 <= bmi < 25.0:
            bmi_cat = "Normal Weight (18.5 - 24.9)"
            cat_color = "#10B981"
        elif 25.0 <= bmi < 30.0:
            bmi_cat = "Overweight (25.0 - 29.9)"
            cat_color = "#F59E0B"
        else:
            bmi_cat = "Obese Class (≥ 30.0)"
            cat_color = "#EF4444"

        st.markdown(
            f"""
            <div class="calc-result-box" style="border-color: {cat_color};">
                <div class="calc-result-val" style="color: {cat_color};">{bmi} kg/m²</div>
                <div class="calc-result-lbl" style="color: {cat_color};">WHO Classification: {bmi_cat}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with calc_col2:
        st.markdown("#### 2. Mean Arterial Pressure (MAP)")
        st.caption("Hemodynamic organ perfusion indicator. Normal resting MAP is typically 70–100 mmHg.")
        sbp = st.number_input("Systolic Blood Pressure (mmHg):", min_value=60, max_value=250, value=120)
        dbp = st.number_input("Diastolic Blood Pressure (mmHg):", min_value=40, max_value=150, value=80)

        map_val = round((2 * dbp + sbp) / 3, 1)

        if map_val < 65:
            map_status = "⚠️ Risk of Low Organ Perfusion (< 65 mmHg)"
            map_color = "#EF4444"
        elif 65 <= map_val <= 100:
            map_status = "✅ Normal Physiological Range (65 - 100 mmHg)"
            map_color = "#10B981"
        else:
            map_status = "⚠️ Elevated Vascular Resistance (> 100 mmHg)"
            map_color = "#F59E0B"

        st.markdown(
            f"""
            <div class="calc-result-box" style="border-color: {map_color};">
                <div class="calc-result-val" style="color: {map_color};">{map_val} mmHg</div>
                <div class="calc-result-lbl" style="color: {map_color};">{map_status}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ═════════════════════════════════════════════════════════════════════════════
# TAB 4: Emergency Triage Protocol & Red Flag Matrix
# ═════════════════════════════════════════════════════════════════════════════
with tab_triage:
    st.markdown("### 🚨 Emergency Medical Red Flags Matrix")
    st.markdown(
        "Immediate clinical indicators that demand **urgent / emergent evaluation** via emergency department or ambulance service."
    )

    triage_col1, triage_col2 = st.columns(2)

    with triage_col1:
        st.markdown(
            """
            <div class="triage-red-box">
                <h4>🫀 Acute Coronary Syndrome (Heart Attack)</h4>
                <ul>
                    <li>Crushing, squeezing retrosternal chest pain or pressure</li>
                    <li>Radiation of discomfort to jaw, neck, back, or left arm</li>
                    <li>Associated diaphoresis (cold sweats), nausea, or shortness of breath</li>
                </ul>
            </div>

            <div class="triage-red-box">
                <h4>🧠 Acute Stroke (BE-FAST Protocol)</h4>
                <ul>
                    <li><strong>B</strong>alance: Sudden loss of balance or coordination</li>
                    <li><strong>E</strong>yes: Sudden vision loss or diplopia (double vision)</li>
                    <li><strong>F</strong>ace: Unilateral facial droop</li>
                    <li><strong>A</strong>rm: Unilateral arm or leg weakness / numbness</li>
                    <li><strong>S</strong>peech: Slurred speech or aphasia</li>
                    <li><strong>T</strong>ime: Immediate emergency activation</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with triage_col2:
        st.markdown(
            """
            <div class="triage-red-box">
                <h4>🫁 Severe Respiratory Compromise</h4>
                <ul>
                    <li>Inability to speak in full sentences due to dyspnea</li>
                    <li>Cyanosis (bluish tint) around lips, nailbeds, or tongue</li>
                    <li>Stridor or audible wheezing with retractions</li>
                </ul>
            </div>

            <div class="triage-red-box">
                <h4>🦠 Sepsis &amp; Severe Infection Warning Signs</h4>
                <ul>
                    <li>Extreme shivering or severe muscle pain</li>
                    <li>Altered mental status, confusion, or extreme lethargy</li>
                    <li>Mottled or discolored skin with severe tachycardia</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Global Footer ────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="clinical-footer">
        <strong>{APP_TITLE}</strong> — Enterprise Decision Support System v{APP_VERSION}<br>
        Powered by Groq LPUs &amp; Qwen 3.8 27B • Strictly for Educational &amp; Clinical Information Architecture<br>
        Confidential Session • Client Data Stored Strictly in Volatile Memory
    </div>
    """,
    unsafe_allow_html=True,
)
