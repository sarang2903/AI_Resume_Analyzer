import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd

def advanced_dashboard(data):

    st.markdown("## 📊 Advanced Resume Analytics Dashboard")

    if not data:
        st.warning("⚠️ Please upload resume first")
        return

    skills = data["skills"]
    match = data["match"]
    score = data["score"]

    # -------- FILTERS --------
    st.sidebar.markdown("### 🎛 Filters")

    selected_skills = st.sidebar.multiselect(
        "Filter Skills",
        options=skills,
        default=skills
    )

    show_missing = st.sidebar.checkbox("Show Missing Skills", True)

    # -------- DATA --------
    df = pd.DataFrame({
        "Skill": selected_skills,
        "Value": [1]*len(selected_skills)
    })

    # -------- SUBPLOTS --------
    fig = make_subplots(
        rows=2, cols=2,
        specs=[
            [{"type": "bar"}, {"type": "pie"}],
            [{"type": "indicator"}, {"type": "indicator"}]
        ],
        subplot_titles=(
            "📊 Skill Distribution",
            "🥧 Skill Share",
            "🎯 JD Match",
            "🤖 AI Score"
        )
    )

    # -------- BAR CHART --------
    fig.add_trace(
        go.Bar(
            x=df["Skill"],
            y=df["Value"],
            name="Skills",
            hoverinfo="x+y"
        ),
        row=1, col=1
    )

    # -------- PIE CHART --------
    fig.add_trace(
        go.Pie(
            labels=df["Skill"],
            values=df["Value"],
            hole=0.4
        ),
        row=1, col=2
    )

    # -------- MATCH INDICATOR --------
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=match,
            title={"text": "JD Match %"},
            gauge={"axis": {"range": [0, 100]}}
        ),
        row=2, col=1
    )

    # -------- SCORE INDICATOR --------
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "AI Score"},
            gauge={"axis": {"range": [0, 100]}}
        ),
        row=2, col=2
    )

    # -------- LAYOUT --------
    fig.update_layout(
        height=700,
        title="🚀 Resume Performance Dashboard",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------- EXTRA INSIGHTS --------
    st.markdown("## 📌 Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.success(f"✅ Total Skills: {len(skills)}")
        st.info(f"🎯 Match Score: {match}%")

    with col2:
        st.warning(f"⚡ AI Score: {score}/100")

    # -------- MISSING SKILLS --------
    if show_missing:
        st.markdown("## ❌ Missing Skills")
        missing = data.get("missing", [])
        st.error(", ".join(missing[:15]) if missing else "No missing skills 🎉")
