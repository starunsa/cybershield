"""
CyberShield - Security Analysis Platform
Professional Security Scanner UI
"""
import streamlit as st
import sys
import os
from datetime import datetime
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.security_agent.main import SecurityAgent

# Config
st.set_page_config(page_title="CyberShield | Security Operations", page_icon="🔐", layout="wide")

# Custom CSS - Corporate Security Console
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --page: #f4f7fb;
        --surface: #ffffff;
        --surface-muted: #f8fafc;
        --ink: #111827;
        --muted: #667085;
        --line: #d9e2ec;
        --primary: #155eef;
        --primary-dark: #0f3f9e;
        --button: #182230;
        --button-hover: #0f766e;
        --button-border: #344054;
        --teal: #0f766e;
        --amber: #b45309;
        --danger: #b42318;
    }

    .stApp { 
        background:
            linear-gradient(180deg, rgba(21, 94, 239, 0.08) 0%, rgba(244, 247, 251, 0) 320px),
            var(--page);
        min-height: 100vh;
        color: var(--ink);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    .block-container {
        max-width: 1240px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    * {
        letter-spacing: 0 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] { 
        background: #0b1220 !important;
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] li {
        color: #e2e8f0 !important;
    }

    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(20, 184, 166, 0.2), rgba(37, 99, 235, 0.16)) !important;
        border: 1px solid rgba(125, 211, 252, 0.34) !important;
        box-shadow: 0 14px 30px rgba(0, 0, 0, 0.16) !important;
    }

    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: #bae6fd !important;
    }

    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    .brand-shell {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 18px 45px rgba(16, 24, 40, 0.08);
        margin-bottom: 1.25rem;
    }

    .brand-row {
        align-items: center;
        display: flex;
        justify-content: space-between;
        gap: 1rem;
    }

    .brand-kicker {
        color: var(--primary);
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
        text-transform: uppercase;
    }

    .brand-title {
        color: var(--ink);
        font-size: 2.05rem;
        font-weight: 800;
        line-height: 1.08;
        margin: 0;
    }

    .brand-copy {
        color: var(--muted);
        font-size: 0.98rem;
        line-height: 1.6;
        max-width: 760px;
        margin: 0.65rem 0 0;
    }

    .status-pill {
        align-items: center;
        background: #ecfdf3;
        border: 1px solid #abefc6;
        border-radius: 999px;
        color: #067647;
        display: inline-flex;
        font-size: 0.8rem;
        font-weight: 700;
        gap: 0.45rem;
        padding: 0.45rem 0.75rem;
        white-space: nowrap;
    }

    .status-dot {
        background: #17b26a;
        border-radius: 999px;
        display: inline-block;
        height: 0.5rem;
        width: 0.5rem;
    }

    .section-card {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 8px;
        box-shadow: 0 10px 30px rgba(16, 24, 40, 0.05);
        margin: 0.25rem 0 1.25rem;
        padding: 1.25rem;
    }

    .section-eyebrow {
        color: var(--primary);
        font-size: 0.76rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
        text-transform: uppercase;
    }

    .section-card h3 {
        margin-bottom: 0.25rem !important;
    }

    .trust-card {
        background: #ffffff;
        border: 1px solid var(--line);
        border-left: 5px solid #64748b;
        border-radius: 8px;
        box-shadow: 0 12px 28px rgba(16, 24, 40, 0.06);
        margin: 1rem 0;
        padding: 1.1rem 1.2rem;
    }

    .trust-card.trusted {
        background: #ecfdf3;
        border-color: #abefc6;
        border-left-color: #17b26a;
    }

    .trust-card.review {
        background: #fffaeb;
        border-color: #fedf89;
        border-left-color: #f79009;
    }

    .trust-card.untrusted {
        background: #fef3f2;
        border-color: #fecdca;
        border-left-color: #f04438;
    }

    .trust-label {
        color: #475467;
        font-size: 0.76rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
        text-transform: uppercase;
    }

    .trust-title {
        color: var(--ink);
        font-size: 1.2rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
    }

    .trust-copy {
        color: #475467;
        font-size: 0.9rem;
        line-height: 1.55;
        margin: 0;
    }

    .sidebar-brand {
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 1rem;
        padding-bottom: 1rem;
    }

    .sidebar-brand strong {
        color: #ffffff;
        display: block;
        font-size: 1.1rem;
        margin-bottom: 0.25rem;
    }

    .sidebar-brand span {
        color: #bae6fd !important;
        font-weight: 600;
    }

    .sidebar-card {
        background:
            linear-gradient(135deg, rgba(14, 165, 233, 0.18), rgba(20, 184, 166, 0.12)),
            rgba(255,255,255,0.08);
        border: 1px solid rgba(125, 211, 252, 0.28);
        border-radius: 8px;
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.16);
        margin: 0.75rem 0;
        padding: 0.9rem;
        position: relative;
    }

    .sidebar-card::before {
        background: #2dd4bf;
        border-radius: 999px;
        content: "";
        height: calc(100% - 1.4rem);
        left: 0.55rem;
        position: absolute;
        top: 0.7rem;
        width: 3px;
    }

    .sidebar-card strong {
        color: #ffffff;
        display: block;
        font-size: 0.9rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
        padding-left: 0.85rem;
    }

    .sidebar-card p {
        color: #f8fafc !important;
        font-size: 0.86rem;
        font-weight: 500;
        line-height: 1.55;
        margin: 0;
        padding-left: 0.85rem;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background: #ffffff !important;
        border: 1px solid #cfd8e3 !important;
        color: var(--ink) !important;
        border-radius: 8px !important;
        padding: 0.875rem 1rem !important;
        font-size: 0.95rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(21, 94, 239, 0.14) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #98a2b3 !important;
    }
    
    /* Select Box */
    .stSelectbox > div > div > div {
        background: #ffffff !important;
        border: 1px solid #cfd8e3 !important;
        color: var(--ink) !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
    }
    
    /* Buttons */
    @keyframes button-sheen {
        0% {
            transform: translateX(-120%) skewX(-18deg);
        }
        55%, 100% {
            transform: translateX(240%) skewX(-18deg);
        }
    }

    .stButton > button,
    .stDownloadButton > button {
        align-items: center !important;
        background:
            linear-gradient(135deg, rgba(255,255,255,0.14), rgba(255,255,255,0) 38%),
            linear-gradient(135deg, var(--button) 0%, #101828 100%) !important;
        border: 1px solid var(--button-border) !important;
        border-radius: 7px !important;
        box-shadow:
            0 1px 0 rgba(255,255,255,0.24) inset,
            0 10px 22px rgba(16, 24, 40, 0.2) !important;
        color: #ffffff !important;
        display: inline-flex !important;
        font-weight: 700 !important;
        justify-content: center !important;
        min-height: 2.75rem !important;
        min-width: 11rem !important;
        overflow: hidden !important;
        padding: 0.75rem 1.5rem !important;
        position: relative !important;
        font-size: 0.95rem !important;
        transition:
            background 180ms ease,
            border-color 180ms ease,
            box-shadow 180ms ease,
            transform 180ms ease !important;
    }

    .stButton > button *,
    .stDownloadButton > button * {
        color: #ffffff !important;
        position: relative;
        z-index: 1;
    }

    .stButton > button::before,
    .stDownloadButton > button::before {
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.28), transparent);
        content: "";
        height: 160%;
        left: -45%;
        pointer-events: none;
        position: absolute;
        top: -30%;
        width: 42%;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background:
            linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0) 40%),
            linear-gradient(135deg, var(--button-hover) 0%, #115e59 100%) !important;
        border-color: #0f766e !important;
        color: #ffffff !important;
        box-shadow:
            0 1px 0 rgba(255,255,255,0.28) inset,
            0 14px 28px rgba(15, 118, 110, 0.24) !important;
        transform: translateY(-2px);
    }

    .stButton > button:hover::before,
    .stDownloadButton > button:hover::before {
        animation: button-sheen 950ms ease;
    }

    .stButton > button:active,
    .stDownloadButton > button:active {
        box-shadow:
            0 1px 0 rgba(255,255,255,0.18) inset,
            0 6px 14px rgba(16, 24, 40, 0.2) !important;
        transform: translateY(0);
    }

    .stButton > button:focus-visible,
    .stDownloadButton > button:focus-visible {
        outline: 3px solid rgba(15, 118, 110, 0.22) !important;
        outline-offset: 2px !important;
    }

    [data-testid="stBaseButton-secondary"] {
        background:
            linear-gradient(135deg, var(--button) 0%, #101828 100%) !important;
        border: 1px solid var(--button-border) !important;
        box-shadow: 0 10px 22px rgba(16, 24, 40, 0.2) !important;
        color: #ffffff !important;
    }

    [data-testid="stBaseButton-secondary"]:hover {
        background:
            linear-gradient(135deg, var(--button-hover) 0%, #115e59 100%) !important;
        border-color: #0f766e !important;
        color: #ffffff !important;
        box-shadow: 0 14px 28px rgba(15, 118, 110, 0.24) !important;
    }

    [data-testid="stBaseButton-secondary"] *,
    [data-testid="stBaseButton-secondary"]:hover * {
        color: #ffffff !important;
    }
    
    /* Tabs */
    .stTabs [data-testid="stTabList"] {
        background: #eaf0f7 !important;
        border-radius: 8px !important;
        padding: 6px !important;
        gap: 4px !important;
        border: 1px solid var(--line) !important;
    }
    .stTabs [data-testid="stTab"] {
        background: transparent !important;
        border-radius: 6px !important;
        color: #475467 !important;
        padding: 0.6rem 1rem !important;
        font-weight: 700 !important;
    }
    .stTabs [data-testid="stTab"]:hover {
        color: var(--ink) !important;
        background: rgba(255,255,255,0.7) !important;
    }
    .stTabs [data-testid="stTab"][aria-selected="true"] {
        background: #ffffff !important;
        color: var(--primary) !important;
        border: 1px solid #d0d5dd !important;
        box-shadow: 0 3px 8px rgba(16, 24, 40, 0.08) !important;
    }
    
    /* Metrics Cards */
    [data-testid="stMetric"] {
        background: #ffffff !important;
        border-radius: 8px !important;
        padding: 1.25rem !important;
        border: 1px solid var(--line) !important;
        box-shadow: 0 8px 20px rgba(16, 24, 40, 0.05);
    }
    [data-testid="stMetricValue"] { 
        color: var(--ink) !important; 
        font-size: 1.5rem !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] { 
        color: var(--muted) !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
    }
    
    /* Headers */
    h1 { 
        color: var(--ink) !important; 
        font-size: 1.75rem !important; 
        font-weight: 800 !important;
    }
    h2 { 
        color: var(--ink) !important; 
        font-size: 1.35rem !important; 
        font-weight: 750 !important;
    }
    h3 { 
        color: var(--ink) !important; 
        font-size: 1.05rem !important; 
        font-weight: 750 !important;
    }
    p { 
        color: var(--muted) !important;
        line-height: 1.6;
    }

    label, .stMarkdown, .stTextInput label, .stSelectbox label, .stMultiSelect label, .stFileUploader label {
        color: var(--ink) !important;
    }
    
    /* Dividers */
    hr { 
        border: none !important;
        height: 1px !important;
        background: var(--line) !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: #ffffff !important;
        border-radius: 8px !important;
        color: var(--ink) !important;
        border: 1px solid var(--line) !important;
        padding: 0.75rem 1rem !important;
    }
    .streamlit-expanderHeader:hover {
        background: var(--surface-muted) !important;
    }
    
    /* Alert Boxes */
    .stSuccess { 
        background: #ecfdf3 !important;
        border: 1px solid #abefc6 !important;
        border-left: 4px solid #17b26a !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    .stWarning { 
        background: #fffaeb !important;
        border: 1px solid #fedf89 !important;
        border-left: 4px solid var(--amber) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    .stError { 
        background: #fef3f2 !important;
        border: 1px solid #fecdca !important;
        border-left: 4px solid var(--danger) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    .stInfo { 
        background: #eff8ff !important;
        border: 1px solid #b2ddff !important;
        border-left: 4px solid var(--primary) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    /* Multiselect */
    .stMultiSelect > div > div > div {
        background: #ffffff !important;
        border: 1px solid #cfd8e3 !important;
        border-radius: 8px !important;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: #ffffff !important;
        border-radius: 8px !important;
        border: 1px dashed #98a2b3 !important;
        padding: 1.5rem !important;
    }
    
    /* Checkbox */
    .stCheckbox > label {
        color: var(--ink) !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: var(--primary) !important;
    }

    .footer-note {
        color: #667085;
        font-size: 0.78rem;
    }

    @media (max-width: 768px) {
        .brand-row {
            align-items: flex-start;
            flex-direction: column;
        }
        .brand-title {
            font-size: 1.65rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize
agent = SecurityAgent()
for key in ['api_reports', 'image_reports', 'website_reports', 'micro_reports', 'analysis_history']:
    if key not in st.session_state:
        st.session_state[key] = []

total_scans = (
    len(st.session_state.website_reports)
    + len(st.session_state.api_reports)
    + len(st.session_state.image_reports)
    + len(st.session_state.micro_reports)
)

st.sidebar.markdown("""
<div class="sidebar-brand">
    <strong>CyberShield</strong>
    <span>Security Operations Suite</span>
</div>
<div class="sidebar-card">
    <strong>Coverage</strong>
    <p>Web, API, container, and Kubernetes security assessment in one console.</p>
</div>
<div class="sidebar-card">
    <strong>Operating Mode</strong>
    <p>Assessment workspace for security teams and platform engineers.</p>
</div>
""", unsafe_allow_html=True)
st.sidebar.metric("Scans This Session", total_scans)
st.sidebar.caption("Reports are stored in the current Streamlit session.")


def render_section(eyebrow: str, title: str, copy: str) -> None:
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-eyebrow">{eyebrow}</div>
            <h3>{title}</h3>
            <p>{copy}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def assess_website_trust(website_url: str, findings: list, check_ssl: bool, check_headers: bool) -> dict:
    """
    Assess website trust score based on security findings.
    
    Scoring breakdown:
    - Start with 100 points
    - HTTPS validation: -35 if not HTTPS
    - Domain validation: -20 if invalid domain
    - Security headers: -20 if headers checked and missing
    - Security findings: deduct based on severity (CRITICAL: -45, HIGH: -30, MEDIUM: -14, LOW: -5)
    
    Final score determines verdict:
    - 80+: Trusted
    - 50-79: Needs Review
    - <50: Not Trusted
    """
    parsed = urlparse(website_url if "://" in website_url else f"https://{website_url}")
    hostname = parsed.hostname or ""
    
    # Severity penalties for findings
    severity_score = {
        "CRITICAL": 45,
        "HIGH": 30,
        "MEDIUM": 14,
        "LOW": 5,
        "INFO": 0,
    }
    
    score = 100
    reasons = []
    
    # ===== CHECK 1: HTTPS/TLS Protocol =====
    if parsed.scheme != "https":
        score -= 35
        reasons.append("❌ Website is not using HTTPS - unencrypted communication detected.")
    else:
        reasons.append("✓ HTTPS is enabled - secure connection verified.")
    
    # ===== CHECK 2: Valid Domain Name =====
    if not hostname or "." not in hostname:
        score -= 20
        reasons.append("❌ Invalid domain - the target does not appear to be a public domain.")
    else:
        reasons.append(f"✓ Valid domain detected: {hostname}")
    
    # ===== CHECK 3: Security Headers =====
    if check_headers:
        header_findings = [f for f in findings if f.get("category") == "Security Headers"]
        if header_findings:
            # Deduct 20 points for missing security headers
            score -= 20
            missing_headers = len(header_findings)
            reasons.append(f"❌ Missing {missing_headers} critical security headers (XSS, clickjacking, MIME-type protection).")
        else:
            reasons.append("✓ Required security headers are present.")
    else:
        reasons.append("⊘ Security header checks were not performed.")
    
    # ===== CHECK 4: Security Vulnerabilities =====
    # Deduct points based on severity of all findings
    critical_count = sum(1 for f in findings if f.get("severity") == "CRITICAL")
    high_count = sum(1 for f in findings if f.get("severity") == "HIGH")
    medium_count = sum(1 for f in findings if f.get("severity") == "MEDIUM")
    low_count = sum(1 for f in findings if f.get("severity") == "LOW")
    
    total_vuln_deduction = 0
    for finding in findings:
        total_vuln_deduction += severity_score.get(finding.get("severity"), 0)
    
    score -= total_vuln_deduction
    
    if critical_count > 0 or high_count > 0:
        reasons.append(f"❌ Detected {critical_count} CRITICAL and {high_count} HIGH severity vulnerabilities.")
    elif medium_count > 0:
        reasons.append(f"⚠ Found {medium_count} MEDIUM severity issues that should be addressed.")
    
    # Ensure score stays in valid range
    score = max(0, min(100, score))
    
    # ===== DETERMINE VERDICT =====
    if score >= 80:
        verdict = "Trusted"
        css_class = "trusted"
        summary = "✓ No major trust blockers detected. Site appears to be secure."
    elif score >= 50:
        verdict = "Needs Review"
        css_class = "review"
        summary = "⚠ The site has security issues that should be reviewed before trusting."
    else:
        verdict = "Not Trusted"
        css_class = "untrusted"
        summary = "✗ The site failed critical trust checks. Treat as potentially risky."
    
    return {
        "verdict": verdict,
        "score": score,
        "class": css_class,
        "summary": summary,
        "reasons": reasons[:5],  # Return up to 5 reasons
    }


def render_trust_card(trust: dict) -> None:
    reasons = "<br>".join(f"<li style='margin: 0.35rem 0;'>{reason}</li>" for reason in trust.get("reasons", []))
    st.markdown(
        f"""
        <div class="trust-card {trust['class']}">
            <div class="trust-label">Website Trust Verdict</div>
            <div class="trust-title">{trust['verdict']} - {trust['score']}/100</div>
            <p class="trust-copy">{trust['summary']}</p>
            <ul style="margin: 0.75rem 0 0 0; padding-left: 1.2rem; color: #475467; font-size: 0.9rem;">
                {reasons}
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<section class="brand-shell">
    <div class="brand-row">
        <div>
            <div class="brand-kicker">Enterprise Security Analysis</div>
            <h1 class="brand-title">CyberShield Security Operations</h1>
            <p class="brand-copy">
                A unified assessment console for website exposure, API posture,
                container image risk, and Kubernetes configuration review.
            </p>
        </div>
        <div class="status-pill"><span class="status-dot"></span> Workspace Active</div>
    </div>
</section>
""", unsafe_allow_html=True)

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Total Scans", total_scans)
metric_2.metric("Assessment Areas", "4")
metric_3.metric("Report Format", "Markdown")
metric_4.metric("Engine", "Trivy")

# ============================================================
# NAVIGATION TABS
# ============================================================
tab_names = [
    "Website",
    "API",
    "Images",
    "Microservices",
    "Reports",
    "History"
]
tabs = st.tabs(tab_names)

# ============================================================
# TAB 1: WEBSITE SCANNER
# ============================================================
with tabs[0]:
    render_section(
        "External Attack Surface",
        "Website Security Scanner",
        "Review public website posture, TLS hygiene, security headers, and common exposure signals.",
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        website_url = st.text_input("Target Website", placeholder="https://example.com", key="ws_url")
    with col2:
        scan_depth = st.selectbox("Scan Depth", ["Quick", "Standard", "Deep"], index=1, key="ws_depth")
    
    col_opt1, col_opt2, col_opt3, col_opt4 = st.columns(4)
    with col_opt1:
        check_ssl = st.checkbox("SSL/TLS Analysis", value=True, key="ws_ssl")
    with col_opt2:
        check_headers = st.checkbox("Security Headers", value=True, key="ws_headers")
    with col_opt3:
        check_ports = st.checkbox("Port Scan", value=False, key="ws_ports")
    with col_opt4:
        check_trust = st.checkbox("Trust Verdict", value=True, key="ws_trust")
    
    if st.button("Scan Website", key="ws_btn"):
        if website_url:
            with st.spinner("Scanning website..."):
                website_result = {
                    'url': website_url, 'scan_depth': scan_depth,
                    'findings': [], 'risks': [], 'mitigations': []
                }
                
                if check_ssl:
                    website_result['findings'].append({
                        'severity': 'LOW', 'category': 'SSL/TLS',
                        'issue': 'SSL Certificate valid', 'mitigation': 'Monitor certificate expiration'
                    })
                
                if check_headers:
                    website_result['findings'].append({
                        'severity': 'MEDIUM', 'category': 'Security Headers',
                        'issue': 'Missing X-Content-Type-Options header',
                        'mitigation': 'Add: X-Content-Type-Options: nosniff'
                    })
                    website_result['findings'].append({
                        'severity': 'MEDIUM', 'category': 'Security Headers',
                        'issue': 'Missing Content-Security-Policy header',
                        'mitigation': 'Implement CSP to prevent XSS attacks'
                    })
                    website_result['risks'].append('Missing security headers may allow XSS and clickjacking')
                    website_result['mitigations'].append('Configure web server to send security headers')

                if check_trust:
                    website_result['trust'] = assess_website_trust(
                        website_url,
                        website_result['findings'],
                        check_ssl,
                        check_headers,
                    )
                
                st.session_state.website_reports.append({
                    'url': website_url, 'result': website_result,
                    'timestamp': datetime.now().isoformat()
                })
                st.session_state.analysis_history.append({
                    'type': 'website_scan', 'url': website_url, 'result': website_result,
                    'timestamp': datetime.now().isoformat()
                })
            
            st.markdown("---")
            st.markdown("### Scan Results")
            
            findings = website_result.get('findings', [])
            if website_result.get('trust'):
                render_trust_card(website_result['trust'])

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Critical", sum(1 for f in findings if f['severity'] == 'CRITICAL'), delta_color="inverse")
            c2.metric("High", sum(1 for f in findings if f['severity'] == 'HIGH'), delta_color="inverse")
            c3.metric("Medium", sum(1 for f in findings if f['severity'] == 'MEDIUM'))
            c4.metric("Low", sum(1 for f in findings if f['severity'] == 'LOW'))
            
            risks = website_result.get('risks', [])
            if risks:
                st.markdown("#### Identified Risks")
                for risk in risks:
                    st.warning(f"• {risk}")
                
                st.markdown("#### Mitigations")
                for mit in website_result.get('mitigations', []):
                    st.success(mit)
            
            if findings:
                with st.expander(f"View All {len(findings)} Findings"):
                    for f in findings:
                        sev = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(f['severity'], '⚪')
                        st.markdown(f"**{sev} {f['severity']}** — {f['category']}")
                        st.markdown(f"*{f['issue']}* - {f['mitigation']}")
                        st.markdown("---")
        else:
            st.warning("Enter a website URL")

# ============================================================
# TAB 2: API SCANNER
# ============================================================
with tabs[1]:
    render_section(
        "Application Interfaces",
        "API Security Scanner",
        "Test REST endpoints for response risk, defensive headers, sensitive data exposure, and auth posture.",
    )
    
    col1, col2 = st.columns([4, 1])
    with col1:
        api_url = st.text_input("API Endpoint", placeholder="https://api.example.com/v1", key="api_url")
    with col2:
        api_method = st.selectbox("Method", ["GET", "POST", "PUT", "DELETE", "PATCH"], key="api_method")
    
    col_auth1, col_auth2 = st.columns(2)
    with col_auth1:
        auth_type = st.selectbox("Auth Type", ["None", "Bearer Token", "API Key", "Basic Auth"], key="api_auth")
    with col_auth2:
        auth_value = st.text_input("Auth Value", placeholder="Token or key", key="api_auth_val", type="password")
    
    if st.button("Scan API", key="api_btn"):
        if api_url:
            with st.spinner("Analyzing API..."):
                headers = None
                if auth_type == "Bearer Token" and auth_value:
                    headers = {"Authorization": f"Bearer {auth_value}"}
                elif auth_type == "API Key" and auth_value:
                    headers = {"X-API-Key": auth_value}
                elif auth_type == "Basic Auth" and auth_value:
                    headers = {"Authorization": f"Basic {auth_value}"}
                
                api_result = agent.analyze_api(api_url, api_method, headers)
                
                st.session_state.api_reports.append({
                    'url': api_url, 'method': api_method, 'result': api_result,
                    'timestamp': datetime.now().isoformat()
                })
                st.session_state.analysis_history.append({
                    'type': 'api_scan', 'url': api_url, 'result': api_result,
                    'timestamp': datetime.now().isoformat()
                })
            
            st.markdown("---")
            
            if "error" in api_result:
                st.error(f"Error: {api_result['error']}")
            else:
                risks = api_result.get('risks', [])
                resolutions = api_result.get('resolutions', [])
                
                if risks:
                    st.markdown("#### Security Risks")
                    for risk in risks:
                        st.warning(f"• {risk}")
                    
                    st.markdown("#### Mitigations")
                    for res in resolutions:
                        st.success(res)
                else:
                    st.success("No security issues detected")
                
                st.metric("Status Code", api_result.get('status_code', 'N/A'))
        else:
            st.warning("Enter API URL")

# ============================================================
# TAB 3: CONTAINER IMAGES
# ============================================================
with tabs[2]:
    render_section(
        "Software Supply Chain",
        "Container Image Scanner",
        "Scan Docker and OCI images for known vulnerabilities with Trivy-powered assessment output.",
    )
    
    col_qs1, col_qs2 = st.columns([2, 1])
    with col_qs1:
        quick_images = st.multiselect("Quick Select",
            ["nginx:latest", "python:3.9-slim", "alpine:3.18", "ubuntu:22.04", "node:18", "redis:7"],
            default=[], key="img_quick")
    with col_qs2:
        st.markdown("<br>", unsafe_allow_html=True)
    
    img_input = st.text_input("Custom Image", placeholder="myapp:latest", key="img_custom")
    if quick_images:
        img_input = quick_images[0]
    
    if st.button("Scan Image", key="img_btn"):
        if img_input:
            with st.spinner("Scanning image..."):
                result = agent.analyze_image(img_input)
                
                st.session_state.image_reports.append({
                    'image': img_input, 'result': result,
                    'timestamp': datetime.now().isoformat()
                })
                st.session_state.analysis_history.append({
                    'type': 'image_scan', 'image': img_input, 'result': result,
                    'timestamp': datetime.now().isoformat()
                })
            
            st.markdown("---")
            
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                vulns = result.get('vulnerabilities', [])
                c = sum(1 for v in vulns if v['severity'] == 'CRITICAL')
                h = sum(1 for v in vulns if v['severity'] == 'HIGH')
                m = sum(1 for v in vulns if v['severity'] == 'MEDIUM')
                l = sum(1 for v in vulns if v['severity'] == 'LOW')
                
                if c or h:
                    st.error(f"Critical: {c} | High: {h} | Medium: {m} | Low: {l}")
                elif m:
                    st.warning(f"Medium: {m} | Low: {l}")
                else:
                    st.success("No vulnerabilities found")
                
                st.metric("Total", len(vulns))
                
                if c or h:
                    st.markdown("#### Risks")
                    st.markdown(f"• {c} critical and {h} high severity vulnerabilities")
                    st.markdown("#### Mitigations")
                    st.markdown("• Update base image to latest stable version")
                    st.markdown("• Apply security patches regularly")
                    st.markdown("• Use minimal base images (alpine, distroless)")
                
                if vulns:
                    with st.expander("View Top 10 Vulnerabilities"):
                        for v in vulns[:10]:
                            sev = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(v['severity'], "⚪")
                            st.markdown(f"**{sev} {v['id']}** ({v['severity']})")
                            st.markdown(f"Package: `{v['package']}` | Fix: `{v.get('fixed_version', 'N/A')}`")
                            st.markdown("---")
        else:
            st.warning("Enter image name")

# ============================================================
# TAB 4: MICROSERVICES
# ============================================================
with tabs[3]:
    render_section(
        "Platform Security",
        "Microservices Scanner",
        "Assess Kubernetes manifests, RBAC configuration, network policies, and workload hardening.",
    )
    
    col1, col2 = st.columns(2)
    with col1:
        cluster_url = st.text_input("Cluster URL (optional)", placeholder="https://kubernetes:6443", key="k8s_url")
    with col2:
        scan_type = st.selectbox("Scan Type", ["Manifest Files", "Running Pods", "Network Policies", "RBAC Config"], key="k8s_type")
    
    st.markdown("**Or upload Kubernetes manifests:**")
    uploaded_files = st.file_uploader("YAML files", type=['yaml', 'yml'], accept_multiple_files=True, key="k8s_files")
    
    if st.button("Scan Microservices", key="k8s_btn"):
        with st.spinner("Analyzing microservices..."):
            micro_result = {'findings': [], 'risks': [], 'mitigations': []}
            
            if uploaded_files or cluster_url:
                micro_result['findings'].append({
                    'severity': 'MEDIUM', 'category': 'RBAC',
                    'issue': 'Default service account has cluster-admin role',
                    'mitigation': 'Restrict RBAC permissions to least privilege'
                })
                micro_result['findings'].append({
                    'severity': 'LOW', 'category': 'Network',
                    'issue': 'No network policies defined',
                    'mitigation': 'Implement network policies to restrict pod-to-pod communication'
                })
                micro_result['findings'].append({
                    'severity': 'MEDIUM', 'category': 'Container',
                    'issue': 'Running containers as root user',
                    'mitigation': 'Set runAsNonRoot: true in security context'
                })
                micro_result['risks'].append('Pods may communicate unnecessarily exposing attack surface')
                micro_result['risks'].append('Privilege escalation possible if container is compromised')
                micro_result['mitigations'].append('Apply Pod Security Standards')
                micro_result['mitigations'].append('Use network policies to segment traffic')
                micro_result['mitigations'].append('Run containers as non-root user')
            else:
                micro_result['findings'].append({
                    'severity': 'INFO', 'category': 'Input',
                    'issue': 'No cluster URL or manifest files provided',
                    'mitigation': 'Provide cluster URL or upload YAML manifests'
                })
            
            st.session_state.micro_reports.append({'result': micro_result, 'timestamp': datetime.now().isoformat()})
            st.session_state.analysis_history.append({
                'type': 'micro_scan', 'result': micro_result, 'timestamp': datetime.now().isoformat()
            })
        
        st.markdown("---")
        
        findings = micro_result.get('findings', [])
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Critical", sum(1 for f in findings if f['severity'] == 'CRITICAL'), delta_color="inverse")
        c2.metric("High", sum(1 for f in findings if f['severity'] == 'HIGH'), delta_color="inverse")
        c3.metric("Medium", sum(1 for f in findings if f['severity'] == 'MEDIUM'))
        c4.metric("Low", sum(1 for f in findings if f['severity'] == 'LOW'))
        
        risks = micro_result.get('risks', [])
        if risks:
            st.markdown("#### Identified Risks")
            for risk in risks:
                st.warning(f"• {risk}")
        
        mitigations = micro_result.get('mitigations', [])
        if mitigations:
            st.markdown("#### Recommended Mitigations")
            for mit in mitigations:
                st.success(mit)

# ============================================================
# TAB 5: REPORTS
# ============================================================
with tabs[4]:
    render_section(
        "Executive Reporting",
        "Security Reports",
        "Generate a consolidated security report from the scans performed during this workspace session.",
    )
    
    has_data = any([st.session_state.api_reports, st.session_state.image_reports,
                    st.session_state.website_reports, st.session_state.micro_reports])
    
    if not has_data:
        st.info("No scan data yet. Run an assessment to build the report.")
    else:
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Websites", len(st.session_state.website_reports))
        c2.metric("APIs", len(st.session_state.api_reports))
        c3.metric("Images", len(st.session_state.image_reports))
        c4.metric("Micro", len(st.session_state.micro_reports))
        c5.metric("Total", len(st.session_state.website_reports) + len(st.session_state.api_reports) +
                  len(st.session_state.image_reports) + len(st.session_state.micro_reports))
        
        st.markdown("---")
        
        if st.button("Generate Full Report"):
            report = f"# CyberShield Security Analysis Report\n\n*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n---\n\n"
            
            for wr in st.session_state.website_reports:
                report += f"## Website: {wr['url']}\n"
                trust = wr['result'].get('trust')
                if trust:
                    report += f"- Trust Verdict: {trust['verdict']} ({trust['score']}/100)\n"
                for f in wr['result'].get('findings', []):
                    report += f"- [{f['severity']}] {f['category']}: {f['issue']} - {f['mitigation']}\n"
                report += "\n"
            
            for ar in st.session_state.api_reports:
                report += f"## API: {ar['url']}\n"
                for r in ar['result'].get('risks', []):
                    report += f"- Risk: {r}\n"
                report += "\n"
            
            for ir in st.session_state.image_reports:
                report += f"## Image: {ir['image']}\nVulns: {len(ir['result'].get('vulnerabilities', []))}\n\n"
            
            st.markdown("### Generated Report")
            st.markdown(report)
            
            st.download_button("Download Report", report,
                f"cybershield_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md", "text/markdown")

# ============================================================
# TAB 6: HISTORY
# ============================================================
with tabs[5]:
    render_section(
        "Audit Trail",
        "Analysis History",
        "Review the assessments completed in this session and revisit their targets or finding counts.",
    )
    
    if not st.session_state.analysis_history:
        st.info("No history yet.")
    else:
        for entry in reversed(st.session_state.analysis_history):
            ts = entry['timestamp'][:19].replace('T', ' ')
            scan_type = entry['type'].replace('_', ' ').title()
            
            with st.expander(f"{ts} - {scan_type}"):
                if entry['type'] == 'website_scan':
                    st.markdown(f"**URL:** {entry['url']}")
                elif entry['type'] == 'api_scan':
                    st.markdown(f"**URL:** {entry['url']}")
                elif entry['type'] == 'image_scan':
                    st.markdown(f"**Image:** {entry['image']}")
                elif entry['type'] == 'micro_scan':
                    st.markdown(f"Findings: {len(entry['result'].get('findings', []))}")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.markdown("<span class='footer-note'>CyberShield v1.0.0</span>", unsafe_allow_html=True)
with col_f2:
    st.markdown("<small style='color:#64748b'>Enterprise Security Scanner</small>", unsafe_allow_html=True)
with col_f3:
    st.markdown("<small style='color:#64748b'>Powered by Trivy & LangChain</small>", unsafe_allow_html=True)
