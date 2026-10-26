import streamlit as st
import plotly.express as px
import pandas as pd
from database import init_db, get_rules, get_claims
from rule_engine import redact_sensitive_info, run_deterministic_checks
from evidence_validator import validate_findings

# Initialize local SQLite DB
init_db()

st.set_page_config(page_title="BrandGuard Governance Platform", layout="wide")

# Header & Role Switching
st.title("🛡️ BrandGuard: Pre-Publication Brand Governance")
st.caption("Explainable, Evidence-Checked Brand Compliance Engine")

role = st.sidebar.selectbox("Switch User Role", ["Creator", "Manager / Reviewer", "Brand Admin", "Leadership"])

if role == "Creator":
    st.header("✍️ Content Review & Fix Engine")
    
    sample_text = "Get 100% sugar-free energy drink! India's No.1 brand brings 30% faster stamina boost. Contact sales@brand.com or +919876543210."
    
    input_text = st.text_area("Paste draft copy for verification:", value=sample_text, height=140)
    
    redact_toggle = st.checkbox("Enable Privacy Redaction Layer", value=True)
    
    if st.button("Run Hybrid Governance Review", type="primary"):
        processed_text = redact_sensitive_info(input_text) if redact_toggle else input_text
        
        if redact_toggle:
            st.info(f"🔒 **Redacted Input:** {processed_text}")
            
        rules = get_rules()
        claims = get_claims()
        
        # Step 1: Deterministic Engine
        raw_findings = run_deterministic_checks(processed_text, rules, claims)
        
        # Step 2: Evidence Validator
        final_findings = validate_findings(raw_findings, input_text)
        
        st.subheader(f"🔍 Findings & Evidence Log ({len(final_findings)} items)")
        
        for idx, item in enumerate(final_findings):
            with st.expander(f"⚠️ [{item['severity']}] {item['type']} — Quote: \"{item['quote']}\"", expanded=True):
                st.write(f"**Reason:** {item['reason']}")
                st.write(f"**Source / Rule ID:** {item['rule_id']} | **Confidence:** {item['confidence']}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"Apply Minimal Fix", key=f"min_{idx}"):
                        st.success(f"Applied: {item['fix_minimal']}")
                with col2:
                    if st.button(f"Apply Moderate Fix", key=f"mod_{idx}"):
                        st.success(f"Applied: {item['fix_moderate']}")
                with col3:
                    if st.button(f"Apply Full Rewrite", key=f"rew_{idx}"):
                        st.success(f"Applied: {item['fix_rewrite']}")

elif role == "Brand Admin":
    st.header("⚙️ Brand Library & Claim Evidence Vault")
    
    tab1, tab2 = st.tabs(["Claim Evidence Vault", "Rulebook"])
    
    with tab1:
        st.subheader("Verified Claims & Expiry Tracker")
        claims_data = get_claims()
        df_claims = pd.DataFrame(claims_data, columns=["ID", "Claim Pattern", "Evidence Source", "Expiry Date", "Status"])
        st.dataframe(df_claims, use_container_width=True)
        
    with tab2:
        st.subheader("Active Rules Engine Constraints")
        rules_data = get_rules()
        df_rules = pd.DataFrame(rules_data, columns=["ID", "Category", "Rule Description", "Banned Terms", "Preferred Terms", "Severity"])
        st.dataframe(df_rules, use_container_width=True)

elif role == "Leadership":
    st.header("📊 Guideline Health & Analytics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Overall Guideline Health Score", value="87 / 100", delta="+3.2%")
    with col2:
        st.metric(label="Expired Claim Violations Prevented", value="24", delta="This Month")
        
    st.subheader("Recurring Violation Categories")
    chart_data = pd.DataFrame({
        "Category": ["Expired Claims", "Unbacked Claims", "Off-Brand Slang", "Missing Alt Text", "Tone Mismatch"],
        "Violations": [38, 27, 19, 14, 8]
    })
    fig = px.bar(chart_data, x="Category", y="Violations", color="Category", title="Pre-Publication Catch Distribution")
    st.plotly_chart(fig, use_container_width=True)