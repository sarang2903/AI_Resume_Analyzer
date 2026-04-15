import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd
import numpy as np

def ultimate_dashboard(data):

    st.markdown("## 🚀 Ultimate AI Resume Analytics Dashboard")

    if not data:
        st.warning("Upload resume first ⚠️")
        return

    skills = data["skills"]
    match = data["match"]
    score = data["score"]
    missing = data.get("missing", [])

    # -------- SIDEBAR CONTROLS --------
    st.sidebar.markdown("## 🎛 Advanced Controls")

    selected_skills = st.sidebar.multiselect(
        "Select Skills",
        options=skills,
        default=skills
    )

    score_filter = st.sidebar.slider("Minimum AI Score", 0, 100, 0)
    show_heatmap = st.sidebar.checkbox("Show Skill Heatmap", True)

    # -------- FILTER LOGIC --------
    if score < score_filter:
        st.warning("Filtered out by score")
        return

    df = pd.DataFrame({
        "Skill": selected_skills,
        "Value": np.random.randint(1, 5, len(selected_skills))
    })

    # -------- CREATE SUBPLOTS --------
    fig = make_subplots(
        rows=2, cols=3,
        specs=[
            [{"type": "bar"}, {"type": "pie"}, {"type": "polar"}],
            [{"type": "indicator"}, {"type": "indicator"}, {"type": "scatter"}]
        ],
        subplot_titles=(
            "📊 Skill Distribution",
            "🥧 Skill Share",
            "🕸 Skill Radar",
            "🎯 JD Match",
            "🤖 AI Score",
            "📈 Growth Trend"
        )
    )

    # -------- BAR --------
    fig.add_trace(
        go.Bar(x=df["Skill"], y=df["Value"]),
        row=1, col=1
    )

    # -------- PIE --------
    fig.add_trace(
        go.Pie(labels=df["Skill"], values=df["Value"], hole=0.4),
        row=1, col=2
    )

    # -------- RADAR --------
    fig.add_trace(
        go.Scatterpolar(
            r=df["Value"],
            theta=df["Skill"],
            fill='toself'
        ),
        row=1, col=3
    )

    # -------- MATCH GAUGE --------
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=match,
            gauge={"axis": {"range": [0, 100]}},
            title={"text": "JD Match"}
        ),
        row=2, col=1
    )

    # -------- SCORE GAUGE --------
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=score,
            gauge={"axis": {"range": [0, 100]}},
            title={"text": "AI Score"}
        ),
        row=2, col=2
    )

    # -------- TREND (SIMULATED) --------
    trend = np.cumsum(np.random.randint(-2, 5, 10)) + score

    fig.add_trace(
        go.Scatter(
            y=trend,
            mode='lines+markers',
            name="Growth"
        ),
        row=2, col=3
    )

    # -------- LAYOUT --------
    fig.update_layout(
        height=800,
        template="plotly_dark",
        title="🔥 Ultimate Resume Analytics"
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------- HEATMAP --------
    if show_heatmap:
        st.markdown("## 🌡 Skill Relevance Heatmap")

        heat_data = np.random.rand(len(skills), len(skills))

        heat_fig = go.Figure(data=go.Heatmap(
            z=heat_data,
            x=skills,
            y=skills
        ))

        st.plotly_chart(heat_fig, use_container_width=True)

    # -------- AI INSIGHTS --------
    st.markdown("## 🤖 AI Insights")

    col1, col2, col3 = st.columns(3)

    with col1:
        if score < 50:
            st.error("🚨 Low Score: Add more projects & skills")
        else:
            st.success("✅ Good Resume Strength")

    with col2:
        if match < 50:
            st.warning("⚠️ Resume not aligned with JD")
        else:
            st.success("🎯 Good JD Alignment")

    with col3:
        if len(missing) > 5:
            st.info("📚 Learn missing skills to improve")
        else:
            st.success("🔥 Strong Skill Set")

    # -------- MISSING SKILLS --------
    st.markdown("## ❌ Missing Skills")
    st.write(missing if missing else "None 🎉")

    # -------- DOWNLOAD REPORT --------
    st.download_button(
        "📄 Download Insights",
        data=str(data),
        file_name="analysis.txt"
    )
