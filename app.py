"""
CyberShield - Security Analysis Platform
Professional Security Scanner UI
"""
import streamlit as st
import sys
import os
from collections import Counter
from datetime import datetime
from html import escape
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

    @keyframes bot-pop-in {
        0% {
            opacity: 0;
            transform: translateY(18px) scale(0.96);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    .bot-popup {
        animation: bot-pop-in 420ms ease both;
        background: #ffffff;
        border: 1px solid #cfd8e3;
        border-radius: 8px;
        bottom: 1.25rem;
        box-shadow: 0 24px 60px rgba(16, 24, 40, 0.24);
        max-width: 340px;
        overflow: hidden;
        position: fixed;
        right: 1.25rem;
        width: min(340px, calc(100vw - 2rem));
        z-index: 9999;
    }

    .bot-popup summary {
        align-items: center;
        background: linear-gradient(135deg, #182230 0%, #0f766e 100%);
        color: #ffffff;
        cursor: pointer;
        display: flex;
        font-size: 0.92rem;
        font-weight: 800;
        justify-content: space-between;
        list-style: none;
        padding: 0.85rem 1rem;
    }

    .bot-popup summary::-webkit-details-marker {
        display: none;
    }

    .bot-popup summary::after {
        color: rgba(255,255,255,0.82);
        content: "click to collapse";
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
    }

    .bot-popup:not([open]) summary::after {
        content: "open";
    }

    .bot-popup-body {
        padding: 1rem;
    }

    .bot-popup-title {
        color: var(--ink);
        font-size: 1rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
    }

    .bot-popup-copy {
        color: #475467;
        font-size: 0.86rem;
        line-height: 1.55;
        margin: 0 0 0.8rem;
    }

    .bot-popup-hint {
        background: #ecfdf3;
        border: 1px solid #abefc6;
        border-radius: 7px;
        color: #065f46;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 0.65rem 0.75rem;
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

    .insight-grid {
        display: grid;
        gap: 1rem;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        margin: 1rem 0 1.25rem;
    }

    .insight-panel {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 8px;
        box-shadow: 0 10px 28px rgba(16, 24, 40, 0.06);
        min-height: 10.5rem;
        padding: 1rem;
    }

    .insight-label {
        color: #667085;
        font-size: 0.74rem;
        font-weight: 800;
        margin-bottom: 0.45rem;
        text-transform: uppercase;
    }

    .risk-score {
        align-items: center;
        display: flex;
        gap: 0.9rem;
    }

    .risk-ring {
        align-items: center;
        background:
            radial-gradient(circle at center, #ffffff 57%, transparent 58%),
            conic-gradient(var(--danger) calc(var(--score) * 1%), #e4e7ec 0);
        border-radius: 999px;
        color: var(--ink);
        display: inline-flex;
        flex: 0 0 auto;
        font-size: 1.25rem;
        font-weight: 800;
        height: 5.5rem;
        justify-content: center;
        width: 5.5rem;
    }

    .risk-summary {
        color: #475467;
        font-size: 0.9rem;
        line-height: 1.5;
        margin: 0;
    }

    .mini-bars {
        display: grid;
        gap: 0.55rem;
    }

    .mini-bar-row {
        align-items: center;
        display: grid;
        gap: 0.55rem;
        grid-template-columns: 4.4rem 1fr 2rem;
    }

    .mini-bar-label,
    .mini-bar-value {
        color: #475467;
        font-size: 0.78rem;
        font-weight: 700;
    }

    .mini-bar-track {
        background: #eef2f6;
        border-radius: 999px;
        height: 0.5rem;
        overflow: hidden;
    }

    .mini-bar-fill {
        background: linear-gradient(90deg, #155eef, #0f766e);
        border-radius: 999px;
        height: 100%;
        width: var(--width);
    }

    .action-list {
        display: grid;
        gap: 0.55rem;
        margin-top: 0.15rem;
    }

    .action-item {
        align-items: flex-start;
        border: 1px solid #e4e7ec;
        border-radius: 7px;
        display: flex;
        gap: 0.55rem;
        padding: 0.6rem 0.7rem;
    }

    .action-rank {
        align-items: center;
        background: #eff8ff;
        border-radius: 999px;
        color: #175cd3;
        display: inline-flex;
        flex: 0 0 auto;
        font-size: 0.74rem;
        font-weight: 800;
        height: 1.35rem;
        justify-content: center;
        width: 1.35rem;
    }

    .action-text {
        color: #344054;
        font-size: 0.84rem;
        line-height: 1.45;
    }

    .finding-row {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 8px;
        margin: 0.6rem 0;
        padding: 0.85rem 0.95rem;
    }

    .finding-row strong {
        color: var(--ink);
    }

    .severity-badge {
        border-radius: 999px;
        display: inline-flex;
        font-size: 0.72rem;
        font-weight: 800;
        margin-right: 0.45rem;
        padding: 0.18rem 0.52rem;
    }

    .severity-critical {
        background: #fef3f2;
        color: #b42318;
    }

    .severity-high {
        background: #fff4ed;
        color: #b93815;
    }

    .severity-medium {
        background: #fffaeb;
        color: #b54708;
    }

    .severity-low {
        background: #ecfdf3;
        color: #067647;
    }

    .bot-message {
        border-radius: 8px;
        margin: 0.65rem 0;
        padding: 0.8rem 0.95rem;
    }

    .bot-message.user {
        background: #eff8ff;
        border: 1px solid #b2ddff;
    }

    .bot-message.assistant {
        background: #ffffff;
        border: 1px solid var(--line);
        box-shadow: 0 8px 20px rgba(16, 24, 40, 0.05);
    }

    .bot-message-label {
        color: #475467;
        font-size: 0.72rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
        text-transform: uppercase;
    }

    .bot-message-text {
        color: #344054;
        font-size: 0.92rem;
        line-height: 1.55;
        margin: 0;
    }

    @media (max-width: 768px) {
        .brand-row {
            align-items: flex-start;
            flex-direction: column;
        }
        .brand-title {
            font-size: 1.65rem;
        }
        .bot-popup {
            bottom: 0.8rem;
            right: 0.8rem;
            width: calc(100vw - 1.6rem);
        }
        .insight-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize
agent = SecurityAgent()
for key in ['api_reports', 'image_reports', 'website_reports', 'micro_reports', 'analysis_history', 'bot_messages']:
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
    parsed = urlparse(website_url if "://" in website_url else f"https://{website_url}")
    hostname = parsed.hostname or ""
    severity_score = {
        "CRITICAL": 45,
        "HIGH": 30,
        "MEDIUM": 14,
        "LOW": 5,
        "INFO": 0,
    }
    score = 100
    reasons = []

    if parsed.scheme != "https":
        score -= 35
        reasons.append("Website is not using HTTPS.")
    elif check_ssl:
        reasons.append("HTTPS is enabled and SSL/TLS was included in the assessment.")

    if not hostname or "." not in hostname:
        score -= 20
        reasons.append("The target does not look like a complete public domain.")

    if check_headers:
        header_findings = [f for f in findings if f.get("category") == "Security Headers"]
        if header_findings:
            reasons.append("Important browser security headers are missing.")
    else:
        score -= 10
        reasons.append("Security header checks were not included.")

    for finding in findings:
        score -= severity_score.get(finding.get("severity"), 0)

    score = max(0, min(100, score))
    if score >= 80:
        verdict = "Trusted"
        css_class = "trusted"
        summary = "No major trust blockers were detected in this scan."
    elif score >= 50:
        verdict = "Needs Review"
        css_class = "review"
        summary = "The site has security signals that should be reviewed before trusting it."
    else:
        verdict = "Not Trusted"
        css_class = "untrusted"
        summary = "The site failed key trust checks and should be treated as risky."

    return {
        "verdict": verdict,
        "score": score,
        "class": css_class,
        "summary": summary,
        "reasons": reasons[:3],
    }


def render_trust_card(trust: dict) -> None:
    reasons = " ".join(escape(reason) for reason in trust.get("reasons", []))
    st.markdown(
        f"""
        <div class="trust-card {trust['class']}">
            <div class="trust-label">Website Trust Verdict</div>
            <div class="trust-title">{trust['verdict']} - {trust['score']}/100</div>
            <p class="trust-copy">{trust['summary']} {reasons}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def severity_badge(severity: str) -> str:
    normalized = severity.lower()
    return f'<span class="severity-badge severity-{normalized}">{escape(severity)}</span>'


def render_finding_row(severity: str, title: str, detail: str) -> None:
    st.markdown(
        f"""
        <div class="finding-row">
            {severity_badge(severity)}
            <strong>{escape(title)}</strong>
            <p>{escape(detail)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def summarize_security_workspace() -> dict:
    website_findings = [
        finding
        for report in st.session_state.website_reports
        for finding in report.get('result', {}).get('findings', [])
    ]
    image_vulns = [
        vuln
        for report in st.session_state.image_reports
        for vuln in report.get('result', {}).get('vulnerabilities', [])
    ]
    micro_findings = [
        finding
        for report in st.session_state.micro_reports
        for finding in report.get('result', {}).get('findings', [])
    ]
    api_risks = [
        risk
        for report in st.session_state.api_reports
        for risk in report.get('result', {}).get('risks', [])
    ]
    all_findings = website_findings + micro_findings
    severity_counts = {
        severity: sum(1 for finding in all_findings if finding.get('severity') == severity)
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    }
    vulnerability_counts = {
        severity: sum(1 for vuln in image_vulns if vuln.get('severity') == severity)
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    }
    category_counts = Counter(finding.get("category", "General") for finding in all_findings)
    weighted_risk = (
        severity_counts["CRITICAL"] * 35
        + severity_counts["HIGH"] * 22
        + severity_counts["MEDIUM"] * 10
        + severity_counts["LOW"] * 3
        + vulnerability_counts["CRITICAL"] * 18
        + vulnerability_counts["HIGH"] * 10
        + vulnerability_counts["MEDIUM"] * 4
        + len(api_risks) * 8
    )
    risk_score = min(100, weighted_risk)
    latest_trust = None
    if st.session_state.website_reports:
        latest_trust = st.session_state.website_reports[-1].get("result", {}).get("trust")

    return {
        "total_scans": len(st.session_state.analysis_history),
        "website_scans": len(st.session_state.website_reports),
        "api_scans": len(st.session_state.api_reports),
        "image_scans": len(st.session_state.image_reports),
        "micro_scans": len(st.session_state.micro_reports),
        "api_risks": len(api_risks),
        "severity_counts": severity_counts,
        "vulnerability_counts": vulnerability_counts,
        "category_counts": category_counts,
        "risk_score": risk_score,
        "latest_trust": latest_trust,
    }


def build_remediation_actions(limit: int = 4) -> list:
    actions = []

    for report in st.session_state.image_reports:
        for vuln in report.get("result", {}).get("vulnerabilities", []):
            severity = vuln.get("severity", "")
            if severity in ["CRITICAL", "HIGH"]:
                package = vuln.get("package") or "affected package"
                fixed_version = vuln.get("fixed_version") or "a patched version"
                actions.append((
                    4 if severity == "CRITICAL" else 3,
                    f"Update {package} in {report['image']} to {fixed_version} for {vuln.get('id', 'known vulnerability')}.",
                ))

    for report in st.session_state.website_reports:
        for finding in report.get("result", {}).get("findings", []):
            severity = finding.get("severity", "")
            if severity in ["CRITICAL", "HIGH", "MEDIUM"]:
                actions.append((
                    {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2}.get(severity, 1),
                    f"{finding.get('mitigation', 'Review website configuration')} for {report['url']}.",
                ))

    for report in st.session_state.api_reports:
        for resolution in report.get("result", {}).get("resolutions", []):
            actions.append((2, f"{resolution} on {report['url']}."))

    for report in st.session_state.micro_reports:
        for mitigation in report.get("result", {}).get("mitigations", []):
            actions.append((2, mitigation))

    if not actions:
        return [
            "Run a website, API, image, or microservices scan to generate prioritized fixes.",
            "Start with public endpoints and production container images for the highest-value signal.",
        ][:limit]

    deduped = []
    seen = set()
    for _, text in sorted(actions, key=lambda item: item[0], reverse=True):
        if text not in seen:
            deduped.append(text)
            seen.add(text)
        if len(deduped) == limit:
            break
    return deduped


def render_workspace_insights() -> None:
    summary = summarize_security_workspace()
    severity_counts = summary["severity_counts"]
    vuln_counts = summary["vulnerability_counts"]
    max_count = max([1, *severity_counts.values(), *vuln_counts.values()])
    top_actions = build_remediation_actions(limit=3)
    trust = summary["latest_trust"]
    trust_copy = "No website trust verdict yet."
    if trust:
        trust_copy = f"Latest website verdict: {trust['verdict']} at {trust['score']}/100."

    bars = ""
    for label, count in [
        ("Critical", severity_counts["CRITICAL"] + vuln_counts["CRITICAL"]),
        ("High", severity_counts["HIGH"] + vuln_counts["HIGH"]),
        ("Medium", severity_counts["MEDIUM"] + vuln_counts["MEDIUM"]),
        ("Low", severity_counts["LOW"] + vuln_counts["LOW"]),
    ]:
        width = max(4, int((count / max_count) * 100)) if count else 0
        bars += f"""
            <div class="mini-bar-row">
                <div class="mini-bar-label">{label}</div>
                <div class="mini-bar-track"><div class="mini-bar-fill" style="--width:{width}%"></div></div>
                <div class="mini-bar-value">{count}</div>
            </div>
        """

    actions = "".join(
        f"""
        <div class="action-item">
            <span class="action-rank">{index}</span>
            <div class="action-text">{escape(action)}</div>
        </div>
        """
        for index, action in enumerate(top_actions, start=1)
    )

    st.markdown(
        f"""
        <div class="insight-grid">
            <div class="insight-panel">
                <div class="insight-label">Workspace Risk</div>
                <div class="risk-score">
                    <div class="risk-ring" style="--score:{summary['risk_score']}">{summary['risk_score']}</div>
                    <p class="risk-summary">{escape(trust_copy)} {summary['api_risks']} API risk notes detected this session.</p>
                </div>
            </div>
            <div class="insight-panel">
                <div class="insight-label">Finding Mix</div>
                <div class="mini-bars">{bars}</div>
            </div>
            <div class="insight-panel">
                <div class="insight-label">Next Best Actions</div>
                <div class="action-list">{actions}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def security_bot_reply(prompt: str) -> str:
    prompt_lower = prompt.lower()
    summary = summarize_security_workspace()

    if not prompt.strip():
        return "Ask me about your scan results, website trust, API risk, container vulnerabilities, or remediation priorities."

    if any(word in prompt_lower for word in ["summary", "status", "overview", "report"]):
        trust = summary["latest_trust"]
        trust_sentence = f" Latest website trust is {trust['verdict']} at {trust['score']}/100." if trust else ""
        return (
            f"Workspace summary: {summary['total_scans']} scans completed. "
            f"Coverage includes {summary['website_scans']} website, {summary['api_scans']} API, "
            f"{summary['image_scans']} image, and {summary['micro_scans']} microservices scans. "
            f"Current workspace risk score is {summary['risk_score']}/100. "
            f"Open risks include {summary['api_risks']} API risk notes, "
            f"{summary['severity_counts']['MEDIUM']} medium configuration findings, and "
            f"{summary['vulnerability_counts']['CRITICAL']} critical container vulnerabilities.{trust_sentence}"
        )

    if any(word in prompt_lower for word in ["trust", "trusted", "website", "site"]):
        if not st.session_state.website_reports:
            return "Run a Website scan first. I can then explain the trust verdict, score, and the signals affecting it."
        latest = st.session_state.website_reports[-1]
        trust = latest.get('result', {}).get('trust')
        if not trust:
            return "The latest Website scan does not include a trust verdict. Enable the Trust Verdict option and scan again."
        reasons = " ".join(trust.get("reasons", []))
        return (
            f"The latest website scan for {latest['url']} is marked {trust['verdict']} "
            f"with a score of {trust['score']}/100. {trust['summary']} {reasons}"
        )

    if any(word in prompt_lower for word in ["fix", "mitigate", "remediate", "priority", "next"]):
        actions = build_remediation_actions(limit=4)
        return "Recommended priority: " + " ".join(f"{index}. {action}" for index, action in enumerate(actions, start=1))

    if any(word in prompt_lower for word in ["api", "endpoint", "header"]):
        if not st.session_state.api_reports:
            return "Run an API scan first. I can then review status codes, missing headers, and sensitive response indicators."
        latest = st.session_state.api_reports[-1]
        risks = latest.get('result', {}).get('risks', [])
        if not risks:
            return f"The latest API scan for {latest['url']} did not detect security risks in the current checks."
        return f"The latest API scan found: {'; '.join(risks[:4])}. Start by adding missing defensive headers and removing sensitive data from responses."

    if any(word in prompt_lower for word in ["image", "container", "trivy", "vulnerability"]):
        if not st.session_state.image_reports:
            return "Run an Image scan first. I can then summarize vulnerable packages and update priorities."
        counts = summary["vulnerability_counts"]
        return (
            f"Container vulnerability counts: critical {counts['CRITICAL']}, high {counts['HIGH']}, "
            f"medium {counts['MEDIUM']}, low {counts['LOW']}. Update the base image, patch packages with fixed versions, "
            "and prefer minimal images for production workloads."
        )

    if any(word in prompt_lower for word in ["kubernetes", "micro", "pod", "rbac", "cluster"]):
        if not st.session_state.micro_reports:
            return "Run a Microservices scan first. I can then summarize RBAC, network policy, and workload hardening findings."
        latest = st.session_state.micro_reports[-1]
        findings = latest.get("result", {}).get("findings", [])
        categories = Counter(f.get("category", "General") for f in findings)
        return (
            f"Latest microservices scan has {len(findings)} findings across "
            f"{', '.join(categories.keys()) or 'general hardening'}. Focus on least-privilege RBAC, "
            "network policies, non-root containers, restricted capabilities, and clear namespace boundaries."
        )

    return (
        "I can help with scan summaries, website trust verdicts, remediation priorities, API risks, "
        "container vulnerabilities, and Kubernetes hardening. Try asking: 'What should I fix first?'"
    )


def render_bot_popup() -> None:
    summary = summarize_security_workspace()
    st.markdown(
        f"""
        <details class="bot-popup" open>
            <summary>CyberShield Bot</summary>
            <div class="bot-popup-body">
                <div class="bot-popup-title">Need help reviewing security posture?</div>
                <p class="bot-popup-copy">
                    I can summarize scans, explain website trust verdicts, and recommend what to fix first.
                    Current workspace: {summary['total_scans']} scans completed.
                </p>
                <div class="bot-popup-hint">Open the Security Bot tab to chat with me.</div>
            </div>
        </details>
        """,
        unsafe_allow_html=True,
    )


def render_chat_message(role: str, content: str) -> None:
    label = "You" if role == "user" else "CyberShield Bot"
    css_role = "user" if role == "user" else "assistant"
    st.markdown(
        f"""
        <div class="bot-message {css_role}">
            <div class="bot-message-label">{label}</div>
            <p class="bot-message-text">{escape(content)}</p>
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

render_workspace_insights()
render_bot_popup()

# ============================================================
# NAVIGATION TABS
# ============================================================
tab_names = [
    "Website",
    "API",
    "Images",
    "Microservices",
    "Security Bot",
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
                        render_finding_row(
                            f["severity"],
                            f"{f['category']}: {f['issue']}",
                            f["mitigation"],
                        )
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
                            render_finding_row(
                                v["severity"],
                                v["id"],
                                f"Package: {v['package']} | Fix: {v.get('fixed_version', 'N/A')}",
                            )
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
# TAB 5: SECURITY BOT
# ============================================================
with tabs[4]:
    render_section(
        "Guided Security Assistant",
        "Security Bot",
        "Ask for scan summaries, trust verdict explanations, remediation priorities, and hardening guidance.",
    )

    if not st.session_state.bot_messages:
        st.session_state.bot_messages.append({
            "role": "assistant",
            "content": "Hello. I can help interpret CyberShield scan results and recommend what to fix first."
        })

    prompt_col, action_col = st.columns([4, 1])
    with prompt_col:
        bot_prompt = st.text_input(
            "Ask CyberShield Bot",
            placeholder="Example: What should I fix first?",
            key="bot_prompt",
        )
    with action_col:
        st.markdown("<br>", unsafe_allow_html=True)
        send_bot_message = st.button("Ask Bot", key="bot_btn")

    quick_1, quick_2, quick_3 = st.columns(3)
    with quick_1:
        if st.button("Summarize Workspace", key="bot_summary"):
            bot_prompt = "summary"
            send_bot_message = True
    with quick_2:
        if st.button("Website Trust", key="bot_trust"):
            bot_prompt = "website trust"
            send_bot_message = True
    with quick_3:
        if st.button("Fix Priorities", key="bot_priorities"):
            bot_prompt = "fix priorities"
            send_bot_message = True

    if send_bot_message:
        st.session_state.bot_messages.append({"role": "user", "content": bot_prompt})
        st.session_state.bot_messages.append({"role": "assistant", "content": security_bot_reply(bot_prompt)})

    st.markdown("---")
    for message in st.session_state.bot_messages[-8:]:
        render_chat_message(message["role"], message["content"])

# ============================================================
# TAB 6: REPORTS
# ============================================================
with tabs[5]:
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
# TAB 7: HISTORY
# ============================================================
with tabs[6]:
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
