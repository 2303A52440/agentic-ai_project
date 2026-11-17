"""
Clinical-grade custom CSS design for MediAssist AI Platform.
"""


def get_custom_css() -> str:
    """Return modern medical enterprise CSS."""
    return """
    <style>
    /* ── Import Clean Typography ────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    /* ── Header Clinical Banner ─────────────────────────────────────────── */
    .clinical-banner {
        background: linear-gradient(135deg, #091E3A 0%, #10375C 50%, #185A9D 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 10px 30px rgba(9, 30, 58, 0.35);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1.2rem;
    }

    .clinical-banner-left h1 {
        color: #FFFFFF;
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    .clinical-banner-left p {
        color: #B4D3E6;
        font-size: 0.95rem;
        margin: 0.4rem 0 0 0;
        font-weight: 400;
    }

    .clinical-banner-right {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
    }

    .telemetry-chip {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 8px;
        padding: 0.4rem 0.8rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #E2E8F0;
        display: flex;
        align-items: center;
        gap: 0.45rem;
    }

    .telemetry-chip-live {
        background: rgba(16, 185, 129, 0.15);
        border-color: rgba(16, 185, 129, 0.4);
        color: #34D399;
    }

    .chip-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 8px #10B981;
        animation: pulseLive 2s infinite ease-in-out;
    }

    @keyframes pulseLive {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.85); }
    }

    /* ── Medical Disclaimer Box ─────────────────────────────────────────── */
    .clinical-disclaimer {
        background: #FFFBEB;
        border: 1px solid #FCD34D;
        border-left: 5px solid #F59E0B;
        padding: 0.9rem 1.25rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        font-size: 0.84rem;
        color: #78350F;
        line-height: 1.55;
    }

    /* ── Streamlit Tabs Styling ─────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 4px;
        margin-bottom: 1.25rem;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 8px 18px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
        color: #475569;
        transition: all 0.2s;
    }

    .stTabs [aria-selected="true"] {
        background-color: #0F4C81 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(15, 76, 129, 0.2);
    }

    /* ── Sidebar Custom Styling ─────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: #0B192C !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #F8FAFC !important;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 1.2rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 0.2rem;
    }

    .sidebar-version {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.725rem;
        color: #38BDF8;
        background: rgba(56, 189, 248, 0.1);
        padding: 2px 6px;
        border-radius: 4px;
        display: inline-block;
        margin-bottom: 1.2rem;
    }

    .sidebar-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 0.9rem 1rem;
        margin-bottom: 1rem;
    }

    .sidebar-card h4 {
        margin: 0 0 0.4rem 0;
        font-size: 0.85rem;
        color: #38BDF8 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* ── Calculator Cards ────────────────────────────────────────────────── */
    .calc-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        margin-bottom: 1.2rem;
    }

    .calc-result-box {
        background: #F0FDF4;
        border: 1px solid #86EFAC;
        padding: 1.2rem;
        border-radius: 10px;
        text-align: center;
        margin-top: 1rem;
    }

    .calc-result-val {
        font-size: 2rem;
        font-weight: 800;
        color: #166534;
        font-family: 'JetBrains Mono', monospace;
    }

    .calc-result-lbl {
        font-size: 0.9rem;
        font-weight: 600;
        color: #15803D;
    }

    /* ── Triage Warning Badge ────────────────────────────────────────────── */
    .triage-red-box {
        background: #FEF2F2;
        border: 1px solid #FECACA;
        border-left: 5px solid #EF4444;
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin-bottom: 1.2rem;
        color: #991B1B;
    }

    .triage-red-box h4 {
        margin: 0 0 0.4rem 0;
        color: #B91C1C;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ── Quick Prompts Grid ──────────────────────────────────────────────── */
    .prompt-chip-btn {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 0.6rem 0.9rem;
        font-size: 0.85rem;
        color: #1E293B;
        text-align: left;
        transition: all 0.2s;
        cursor: pointer;
    }

    .prompt-chip-btn:hover {
        border-color: #0F4C81;
        background: #F1F5F9;
        transform: translateY(-1px);
    }

    /* ── Clean Footer ────────────────────────────────────────────────────── */
    .clinical-footer {
        text-align: center;
        padding: 2rem 0 1rem;
        margin-top: 3rem;
        border-top: 1px solid #E2E8F0;
        font-size: 0.8rem;
        color: #64748B;
        line-height: 1.6;
    }

    /* ── Buttons Customization ───────────────────────────────────────────── */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        transition: all 0.2s ease !important;
    }
    </style>
    """
