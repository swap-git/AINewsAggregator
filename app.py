import streamlit as st
import os
import json
import urllib.request
from datetime import date, timedelta
from source.crew import daily_ai_crew

# Page Configuration
st.set_page_config(page_title="Agentic AI: Global News", layout="wide")

st.title("🤖 Agentic AI: Global AI News Gathering")
st.markdown("---")

# Sidebar for Control
with st.sidebar:
    st.header("Search Focus")
    topic = st.text_input("Enter Topic (e.g., specific models, global regions)", placeholder="GenAI, Tech Trends...")
    run_btn = st.button("RUN INTELLIGENCE CREW", use_container_width=True)

# Main Output Generation Area
if run_btn and topic:
    with st.status("Gathering Intelligence...", expanded=True) as status:
        st.write("🔍 Researcher Agent scanning the globe...")
        # Initialize and kickoff your crew
        crew_instance = daily_ai_crew
        end_date = date.today()
        start_date = end_date - timedelta(days=2)
        result = crew_instance.kickoff(
            inputs={
                'topic': topic,
                'current_date': end_date.isoformat(),
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
            }
        )
        status.update(label="Intelligence Gathered!", state="complete", expanded=False)

    # Detailed Report Dashboard
    st.subheader("Validated, Detailed Intelligence")
    st.markdown(result.raw)  # Display the clean markdown report
else:
    st.info("Enter a focus topic in the sidebar and click 'Run' to begin.")