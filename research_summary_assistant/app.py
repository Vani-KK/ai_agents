import streamlit as st
from main import research_agent

st.set_page_config(
    page_title="Research Assistant",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 AI Research Assistant")
st.markdown("Enter any topic and I'll search the web, read multiple sources, and generate a research report.")
st.divider()

topic = st.text_input(
    label="Research Topic",
    placeholder="e.g. quantum computing, AI agents, climate change..."
)

if st.button("Generate Report 🚀"):
    if topic.strip() == "":
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Searching the web and reading articles..."):
            report = research_agent(topic)
        
        st.success("Report ready!")
        st.divider()
        st.markdown(report)

        st.download_button(
    label="📥 Download Report",
    data=report,
    file_name=f"{topic}_report.txt",
    mime="text/plain"
)