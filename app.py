elif page == "📊 Analytics Dashboard":

    st.markdown('<div class="hero"><h1>📊 Advanced Resume Analytics</h1></div>', unsafe_allow_html=True)

    data = st.session_state.data

    if not data:
        st.warning("Upload resume first")
    else:
        skills = data["skills"]
        score = data["score"]
        match = data["match"]

        # -------- SIDEBAR FILTER --------
        selected_skills = st.sidebar.multiselect(
            "Filter Skills",
            skills,
            default=skills
        )

        df = pd.DataFrame({
            "Skill": selected_skills,
            "Value": np.random.randint(1, 5, len(selected_skills))
        })

        # -------- SUBPLOTS --------
        fig = make_subplots(
            rows=2, cols=2,
            specs=[
                [{"type": "bar"}, {"type": "pie"}],
                [{"type": "polar"}, {"type": "indicator"}]
            ],
            subplot_titles=(
                "Skill Distribution",
                "Skill Share",
                "Skill Radar",
                "AI Score"
            )
        )

        # BAR
        fig.add_trace(
            go.Bar(x=df["Skill"], y=df["Value"]),
            row=1, col=1
        )

        # PIE
        fig.add_trace(
            go.Pie(labels=df["Skill"], values=df["Value"]),
            row=1, col=2
        )

        # RADAR
        fig.add_trace(
            go.Scatterpolar(
                r=df["Value"],
                theta=df["Skill"],
                fill='toself'
            ),
            row=2, col=1
        )

        # GAUGE
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=score,
                title={"text": "AI Score"},
                gauge={"axis": {"range": [0, 100]}}
            ),
            row=2, col=2
        )

        fig.update_layout(height=700, template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

        # -------- TREND --------
        st.subheader("📈 Resume Growth Simulation")

        trend = np.cumsum(np.random.randint(-2, 5, 10)) + score

        trend_fig = go.Figure()
        trend_fig.add_trace(go.Scatter(
            y=trend,
            mode='lines+markers'
        ))

        st.plotly_chart(trend_fig, use_container_width=True)
