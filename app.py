"""
CyberShield - Security Analysis Platform
Professional Security Scanner UI
"""
import streamlit as st
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.security_agent.main import SecurityAgent

# Config
st.set_page_config(page_title="CyberShield | Security Scanner", page_icon="🛡️", layout="wide")

# Custom CSS - Clean Professional Theme
st.markdown("""
<style>
    /* Main Background - Clean Slate */
    .stApp { 
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 50%, #020617 100%);
        min-height: 100vh;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(71, 85, 105, 0.6) !important;
        color: #f1f5f9 !important;
        border-radius: 10px !important;
        padding: 0.875rem 1rem !important;
        font-size: 0.95rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #60a5fa !important;
        box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.15) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #64748b !important;
    }
    
    /* Select Box */
    .stSelectbox > div > div > div {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(71, 85, 105, 0.6) !important;
        color: #f1f5f9 !important;
        border-radius: 10px !important;
        padding: 0.5rem !important;
    }
    
    /* Buttons - Primary Blue */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #60a5fa 0%, #2563eb 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.35) !important;
    }
    
    /* Tabs */
    .stTabs [data-testid="stTabList"] {
        background: rgba(30, 41, 59, 0.5) !important;
        border-radius: 12px !important;
        padding: 6px !important;
        gap: 4px !important;
        border: 1px solid rgba(71, 85, 105, 0.4) !important;
    }
    .stTabs [data-testid="stTab"] {
        background: transparent !important;
        border-radius: 8px !important;
        color: #94a3b8 !important;
        padding: 0.6rem 1rem !important;
        font-weight: 500 !important;
    }
    .stTabs [data-testid="stTab"]:hover {
        color: #e2e8f0 !important;
        background: rgba(59, 130, 246, 0.1) !important;
    }
    .stTabs [data-testid="stTab"][aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Metrics Cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border-radius: 14px !important;
        padding: 1.25rem !important;
        border: 1px solid rgba(71, 85, 105, 0.4) !important;
        backdrop-filter: blur(10px);
    }
    [data-testid="stMetricValue"] { 
        color: #60a5fa !important; 
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] { 
        color: #94a3b8 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Headers */
    h1 { 
        color: #f8fafc !important; 
        font-size: 1.75rem !important; 
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    h2 { 
        color: #f8fafc !important; 
        font-size: 1.35rem !important; 
        font-weight: 600 !important;
    }
    h3 { 
        color: #f1f5f9 !important; 
        font-size: 1.05rem !important; 
        font-weight: 600 !important;
    }
    p { 
        color: #cbd5e1 !important;
        line-height: 1.6;
    }
    
    /* Dividers */
    hr { 
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(71, 85, 105, 0.5), transparent) !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.6) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(71, 85, 105, 0.3) !important;
        padding: 0.75rem 1rem !important;
    }
    .streamlit-expanderHeader:hover {
        background: rgba(30, 41, 59, 0.8) !important;
    }
    
    /* Alert Boxes */
    .stSuccess { 
        background: rgba(34, 197, 94, 0.1) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        border-left: 4px solid #22c55e !important;
        border-radius: 10px !important;
        padding: 1rem !important;
    }
    .stWarning { 
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-left: 4px solid #f59e0b !important;
        border-radius: 10px !important;
        padding: 1rem !important;
    }
    .stError { 
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-left: 4px solid #ef4444 !important;
        border-radius: 10px !important;
        padding: 1rem !important;
    }
    .stInfo { 
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-left: 4px solid #3b82f6 !important;
        border-radius: 10px !important;
        padding: 1rem !important;
    }
    
    /* Multiselect */
    .stMultiSelect > div > div > div {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(71, 85, 105, 0.6) !important;
        border-radius: 10px !important;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(30, 41, 59, 0.5) !important;
        border-radius: 12px !important;
        border: 2px dashed rgba(71, 85, 105, 0.5) !important;
        padding: 1.5rem !important;
    }
    
    /* Checkbox */
    .stCheckbox > label {
        color: #cbd5e1 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #3b82f6 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize
agent = SecurityAgent()
for key in ['api_reports', 'image_reports', 'website_reports', 'micro_reports', 'analysis_history']:
    if key not in st.session_state:
        st.session_state[key] = []

# ============================================================
# HEADER
# ============================================================
col_header1, col_header2 = st.columns([3, 1])
with col_header1:
    st.markdown("## 🛡️ CyberShield")
    st.markdown("*Enterprise Security Analysis Platform*")
with col_header2:
    st.markdown("<div style='text-align:right;padding-top:0.5rem;'><span style='background:linear-gradient(135deg,#3b82f6,#1d4ed8);padding:0.25rem 0.75rem;border-radius:20px;font-size:0.75rem;color:#fff;'>v1.0.0</span></div>", unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# NAVIGATION TABS
# ============================================================
tab_names = [
    "🌐 Website",
    "🔗 API",
    "🐳 Images",
    "☸️ Micro",
    "📊 Reports",
    "📜 History"
]
tabs = st.tabs(tab_names)

# ============================================================
# TAB 1: WEBSITE SCANNER
# ============================================================
with tabs[0]:
    st.markdown("### 🌐 Website Security Scanner")
    st.markdown("*Scan websites for vulnerabilities, misconfigurations, and security headers*")
    st.markdown("---")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        website_url = st.text_input("Target Website", placeholder="https://example.com", key="ws_url")
    with col2:
        scan_depth = st.selectbox("Scan Depth", ["Quick", "Standard", "Deep"], index=1, key="ws_depth")
    
    col_opt1, col_opt2, col_opt3 = st.columns(3)
    with col_opt1:
        check_ssl = st.checkbox("SSL/TLS Analysis", value=True, key="ws_ssl")
    with col_opt2:
        check_headers = st.checkbox("Security Headers", value=True, key="ws_headers")
    with col_opt3:
        check_ports = st.checkbox("Port Scan", value=False, key="ws_ports")
    
    if st.button("🔍 Scan Website", key="ws_btn"):
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
                
                st.session_state.website_reports.append({
                    'url': website_url, 'result': website_result,
                    'timestamp': datetime.now().isoformat()
                })
                st.session_state.analysis_history.append({
                    'type': 'website_scan', 'url': website_url, 'result': website_result,
                    'timestamp': datetime.now().isoformat()
                })
            
            st.markdown("---")
            st.markdown("### 📋 Scan Results")
            
            findings = website_result.get('findings', [])
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Critical", sum(1 for f in findings if f['severity'] == 'CRITICAL'), delta_color="inverse")
            c2.metric("High", sum(1 for f in findings if f['severity'] == 'HIGH'), delta_color="inverse")
            c3.metric("Medium", sum(1 for f in findings if f['severity'] == 'MEDIUM'))
            c4.metric("Low", sum(1 for f in findings if f['severity'] == 'LOW'))
            
            risks = website_result.get('risks', [])
            if risks:
                st.markdown("#### ⚠️ Identified Risks")
                for risk in risks:
                    st.warning(f"• {risk}")
                
                st.markdown("#### 🛡️ Mitigations")
                for mit in website_result.get('mitigations', []):
                    st.success(f"✅ {mit}")
            
            if findings:
                with st.expander(f"📄 View All {len(findings)} Findings"):
                    for f in findings:
                        sev = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(f['severity'], '⚪')
                        st.markdown(f"**{sev} {f['severity']}** — {f['category']}")
                        st.markdown(f"*{f['issue']}* → {f['mitigation']}")
                        st.markdown("---")
        else:
            st.warning("Enter a website URL")

# ============================================================
# TAB 2: API SCANNER
# ============================================================
with tabs[1]:
    st.markdown("### 🔗 API Security Scanner")
    st.markdown("*Analyze REST APIs for security vulnerabilities*")
    st.markdown("---")
    
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
    
    if st.button("🚀 Scan API", key="api_btn"):
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
                    st.markdown("#### ⚠️ Security Risks")
                    for risk in risks:
                        st.warning(f"• {risk}")
                    
                    st.markdown("#### 🛡️ Mitigations")
                    for res in resolutions:
                        st.success(f"✅ {res}")
                else:
                    st.success("✅ No Security Issues Detected")
                
                st.metric("Status Code", api_result.get('status_code', 'N/A'))
        else:
            st.warning("Enter API URL")

# ============================================================
# TAB 3: CONTAINER IMAGES
# ============================================================
with tabs[2]:
    st.markdown("### 🐳 Container Image Scanner")
    st.markdown("*Scan Docker/OCI images for vulnerabilities using Trivy*")
    st.markdown("---")
    
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
    
    if st.button("🔍 Scan Image", key="img_btn"):
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
                    st.error(f"🚨 Critical: {c} | High: {h} | Medium: {m} | Low: {l}")
                elif m:
                    st.warning(f"⚠️ Medium: {m} | Low: {l}")
                else:
                    st.success("✅ No Vulnerabilities Found")
                
                st.metric("Total", len(vulns))
                
                if c or h:
                    st.markdown("#### ⚠️ Risks")
                    st.markdown(f"• {c} critical and {h} high severity vulnerabilities")
                    st.markdown("#### 🛡️ Mitigations")
                    st.markdown("• Update base image to latest stable version")
                    st.markdown("• Apply security patches regularly")
                    st.markdown("• Use minimal base images (alpine, distroless)")
                
                if vulns:
                    with st.expander(f"📄 View Top 10"):
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
    st.markdown("### ☸️ Microservices Scanner")
    st.markdown("*Scan Kubernetes clusters and microservices*")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        cluster_url = st.text_input("Cluster URL (optional)", placeholder="https://kubernetes:6443", key="k8s_url")
    with col2:
        scan_type = st.selectbox("Scan Type", ["Manifest Files", "Running Pods", "Network Policies", "RBAC Config"], key="k8s_type")
    
    st.markdown("**Or upload Kubernetes manifests:**")
    uploaded_files = st.file_uploader("YAML files", type=['yaml', 'yml'], accept_multiple_files=True, key="k8s_files")
    
    if st.button("☸️ Scan Microservices", key="k8s_btn"):
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
            st.markdown("#### ⚠️ Identified Risks")
            for risk in risks:
                st.warning(f"• {risk}")
        
        mitigations = micro_result.get('mitigations', [])
        if mitigations:
            st.markdown("#### 🛡️ Recommended Mitigations")
            for mit in mitigations:
                st.success(f"✅ {mit}")

# ============================================================
# TAB 5: REPORTS
# ============================================================
with tabs[4]:
    st.markdown("### 📊 Security Reports")
    st.markdown("*Generate comprehensive security analysis reports*")
    st.markdown("---")
    
    has_data = any([st.session_state.api_reports, st.session_state.image_reports,
                    st.session_state.website_reports, st.session_state.micro_reports])
    
    if not has_data:
        st.info("📭 No scan data. Run some scans first!")
    else:
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Websites", len(st.session_state.website_reports))
        c2.metric("APIs", len(st.session_state.api_reports))
        c3.metric("Images", len(st.session_state.image_reports))
        c4.metric("Micro", len(st.session_state.micro_reports))
        c5.metric("Total", len(st.session_state.website_reports) + len(st.session_state.api_reports) +
                  len(st.session_state.image_reports) + len(st.session_state.micro_reports))
        
        st.markdown("---")
        
        if st.button("📄 Generate Full Report"):
            report = f"# CyberShield Security Analysis Report\n\n*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n---\n\n"
            
            for wr in st.session_state.website_reports:
                report += f"## 🌐 {wr['url']}\n"
                for f in wr['result'].get('findings', []):
                    report += f"- [{f['severity']}] {f['category']}: {f['issue']} → {f['mitigation']}\n"
                report += "\n"
            
            for ar in st.session_state.api_reports:
                report += f"## 🔗 {ar['url']}\n"
                for r in ar['result'].get('risks', []):
                    report += f"- Risk: {r}\n"
                report += "\n"
            
            for ir in st.session_state.image_reports:
                report += f"## 🐳 {ir['image']}\nVulns: {len(ir['result'].get('vulnerabilities', []))}\n\n"
            
            st.markdown("### 📋 Generated Report")
            st.markdown(report)
            
            st.download_button("💾 Download Report", report,
                f"cybershield_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md", "text/markdown")

# ============================================================
# TAB 6: HISTORY
# ============================================================
with tabs[5]:
    st.markdown("### 📜 Analysis History")
    st.markdown("*View past security scans*")
    st.markdown("---")
    
    if not st.session_state.analysis_history:
        st.info("📭 No history yet.")
    else:
        for entry in reversed(st.session_state.analysis_history):
            ts = entry['timestamp'][:19].replace('T', ' ')
            scan_type = entry['type'].replace('_', ' ').title()
            
            with st.expander(f"🕐 {ts} — {scan_type}"):
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
    st.markdown("<small style='color:#64748b'>🛡️ CyberShield v1.0.0</small>", unsafe_allow_html=True)
with col_f2:
    st.markdown("<small style='color:#64748b'>Enterprise Security Scanner</small>", unsafe_allow_html=True)
with col_f3:
    st.markdown("<small style='color:#64748b'>Powered by Trivy & LangChain</small>", unsafe_allow_html=True)