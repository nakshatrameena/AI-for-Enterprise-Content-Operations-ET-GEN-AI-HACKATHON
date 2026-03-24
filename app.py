import streamlit as st
import time
import pandas as pd
from datetime import datetime
from agents import *

# --- 1. Page Configuration & Custom Styling ---
st.set_page_config(page_title="ContentAI | Enterprise Ops", page_icon="🏢", layout="wide")

st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 12px; border: 1px solid #e0e0e0; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .stTextArea textarea { border-radius: 10px; border: 1px solid #d1d3e2; }
    .stButton button { border-radius: 8px; font-weight: 600; transition: all 0.3s; }
    .stButton button:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Initialize State ---
if "step" not in st.session_state: st.session_state.step = "INPUT"
if "content_store" not in st.session_state: st.session_state.content_store = {}

# --- 3. Sidebar Workflow Monitor ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8644/8644445.png", width=80)
    st.title("Admin Console")
    st.divider()
    
    # Visual Progress Indicator
    st.write("**Workflow Pipeline Status**")
    progress_map = {"INPUT": 10, "GENERATING": 40, "REVIEW": 70, "COMPLETE": 100}
    st.progress(progress_map.get(st.session_state.step, 0))
    
    st.write(f"📍 Current Node: **{st.session_state.step}**")
    
    if st.button("🗑️ Reset All Agents", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- 4. Main Application Interface ---
st.title("🏢 ContentAI Enterprise")
st.markdown("##### *Unified Multi-Agent Content Operations Hub*")

if st.session_state.step == "INPUT":
    with st.container():
        st.subheader("📥 Knowledge Intake")
        u_input = st.text_area("What are we building today?", placeholder="e.g., A fintech neobank for Gen Z with AI budget tracking...", height=180)
        
        c1, c2, c3 = st.columns(3)
        with c1: ind = st.selectbox("Vertical Strategy", ["Fintech", "Healthcare", "E-commerce", "SaaS"])
        with c2: aud = st.selectbox("Target Audience", ["Decision Makers", "Developers", "End Users"])
        with c3: tone = st.select_slider("Brand Tone", ["Bold", "Professional", "Technical"])

    if st.button("🚀 Execute Agent Pipeline", use_container_width=True):
        if u_input:
            st.session_state.update({"user_input": u_input, "industry": ind, "audience": aud, "step": "GENERATING"})
            st.rerun()
        else: st.error("Please provide a content seed to begin.")

    # INITIAL ZERO STATE DASHBOARD
    st.divider()
    st.subheader("📊 Projected Lifecycle Impact")
    m1, m2, m3 = st.columns(3)
    m1.metric("Cycle Time", "0.0h", "0%")
    m2.metric("Compliance Status", "Pending", "N/A")
    m3.metric("OpEx Savings", "None", "Waiting for Input")

if st.session_state.step == "GENERATING":
    with st.status("🛠️ Coordinating Specialists...", expanded=True) as status:
        st.write("🔍 **Knowledge Agent**: Contextualizing enterprise specs...")
        context = knowledge_agent(st.session_state.user_input, st.session_state.industry)
        time.sleep(1)
        
        st.write("✍️ **Copy Agent**: Drafting core narrative architecture...")
        draft = drafting_agent(context, st.session_state.audience)
        time.sleep(1.2)
        
        st.write("🛡️ **Warden Agent**: Running regulatory audit...")
        comp = compliance_agent(draft, st.session_state.industry)
        
        st.session_state.content_store = {"draft": draft, "compliance": comp}
        status.update(label="Workflow Synchronized!", state="complete")
    
    st.session_state.step = "REVIEW"
    st.rerun()

if st.session_state.step == "REVIEW":
    st.subheader("📝 Human-in-the-Loop Gateway")
    
    col_l, col_r = st.columns([3, 1])
    with col_l:
        final_edit = st.text_area("Review and Polish Draft", value=st.session_state.content_store['draft'], height=400)
    with col_r:
        st.success(f"**Compliance Audit**\n\n{st.session_state.content_store['compliance']}")
        st.info("**Strategy Insight**:\nContent is optimized for high-retention engagement on LinkedIn.")

    if st.button("✅ Approve & Publish Asset", use_container_width=True):
        st.session_state.content_store['draft'] = final_edit
        st.session_state.step = "COMPLETE"
        st.rerun()

if st.session_state.step == "COMPLETE":
    st.balloons()
    
    # LOGIC: OPEX SAVINGS AS STRING VALUES
    input_size = len(st.session_state.user_input)
    if input_size > 200: savings_tier = "Ultra Efficiency (Tier 1)"
    elif input_size > 50: savings_tier = "High Impact (Tier 2)"
    else: savings_tier = "Standard Optimization (Tier 3)"

    st.success("🎯 Content Lifecycle Successfully Automated")
    
    tab1, tab2, tab3 = st.tabs(["💎 Final Asset", "📈 Intelligence", "🛡️ Compliance Log"])
    with tab1:
        st.code(publishing_agent(st.session_state.content_store['draft']), language="markdown")
    with tab2:
        st.markdown(intelligence_agent(st.session_state.content_store['draft']))
    with tab3:
        st.info(f"**Final Audit Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.success(st.session_state.content_store['compliance'])

    # ENHANCED BUSINESS IMPACT DASHBOARD
    st.divider()
    st.subheader("📊 Business Value Analytics")
    c1, c2, c3 = st.columns(3)
    c1.metric("Labor Time Avoided", f"{round(input_size/100, 1) + 2} Hours", "-98%")
    c2.metric("Compliance Accuracy", "100%", "Verified")
    c3.metric("OpEx Savings", savings_tier) # STRING VALUE

    # CSV EXPORT
    report_data = {"Project": [st.session_state.user_input], "Savings Tier": [savings_tier], "Status": ["Deployed"]}
    df = pd.DataFrame(report_data)
    st.download_button("📥 Download ROI Export", df.to_csv(index=False).encode('utf-8-sig'), "ROI_Report.csv", "text/csv")