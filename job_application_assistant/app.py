import streamlit as st
from crew import run_crew
from pypdf import PdfReader
import tempfile
import os

st.set_page_config(
    page_title="Job Application Assistant",
    page_icon="💼",
    layout="wide"
)


st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    
    header[data-testid="stHeader"] {
        background-color: #0e1117;
    }
    
    * { color: #e6edf3 !important; }
    
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #e6edf3 !important;
    }
    
    /* Result cards */
    .result-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #161b22;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #161b22;
        border-radius: 6px;
    }

    /* Text areas */
    textarea {
        background-color: #161b22 !important;
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: #161b22 !important;
        border: 1px dashed #30363d !important;
        border-radius: 8px;
    }

    [data-testid="stFileUploaderDropzone"] {
        background-color: #161b22 !important;
    }

    /* Buttons */
    .stButton button {
        background-color: #238636 !important;
        border: 1px solid #2ea043 !important;
        border-radius: 6px !important;
        color: #ffffff !important;
        font-weight: bold !important;
        width: 100% !important;
        padding: 10px !important;
    }

    .stButton button:hover {
        background-color: #2ea043 !important;
    }

    footer { display: none !important; }
            
            /* Fix placeholder text visibility */
    textarea::placeholder {
        color: #8b949e !important;
        opacity: 1 !important;
    }

    input::placeholder {
        color: #8b949e !important;
        opacity: 1 !important;
    }

    /* Fix file uploader button */
    [data-testid="stFileUploaderDropzone"] button {
        background-color: #21262d !important;
        border: 1px solid #30363d !important;
        border-radius: 6px !important;
        color: #e6edf3 !important;
    }

    [data-testid="stFileUploaderDropzone"] button:hover {
        background-color: #30363d !important;
        border-color: #8b949e !important;
    }

    /* Fix radio button area */
    [data-testid="stRadio"] label {
        color: #e6edf3 !important;
    }
            
    /* Result text in tabs - dark text on light background */
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #ffffff !important;
        border-radius: 8px;
        padding: 20px;
    }
    
    .stTabs [data-baseweb="tab-panel"] p,
    .stTabs [data-baseweb="tab-panel"] li,
    .stTabs [data-baseweb="tab-panel"] h1,
    .stTabs [data-baseweb="tab-panel"] h2,
    .stTabs [data-baseweb="tab-panel"] h3,
    .stTabs [data-baseweb="tab-panel"] span,
    .stTabs [data-baseweb="tab-panel"] strong {
        color: #0e1117 !important;
    }
            
</style>
""", unsafe_allow_html=True)

if "results" not in st.session_state:
    st.session_state.results = None

def extract_pdf_text(uploaded_file) -> str:
    """Extract text from uploaded PDF file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    
    reader = PdfReader(tmp_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    os.unlink(tmp_path)
    return text


with st.sidebar:
    st.title("💼 Job Application Assistant")
    st.markdown("*Powered by AI Agents*")
    st.divider()
    
    # Job Description Input
    st.subheader("📋 Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder="We are looking for a Python Developer with..."
    )
    
    st.divider()
    
    # Candidate Background — two options
    st.subheader("👤 Your Background")
    
    input_method = st.radio(
        "How would you like to provide your background?",
        ["Upload Resume PDF", "Type Manually"]
    )
    
    candidate_background = ""
    
    if input_method == "Upload Resume PDF":
        uploaded_resume = st.file_uploader(
            "Upload your resume",
            type="pdf"
        )
        
        if uploaded_resume:
            with st.spinner("Reading your resume..."):
                candidate_background = extract_pdf_text(uploaded_resume)
            st.success(f"✅ Resume loaded! ({len(candidate_background)} characters)")
            
            # Show preview
            with st.expander("📄 Preview extracted text"):
                st.text(candidate_background[:500] + "...")
    
    else:
        candidate_background = st.text_area(
            "Describe your background",
            height=200,
            placeholder="""Name: Your Name
Experience: X years in...
Skills: Python, SQL, ...
Achievements: Built X that did Y...
Education: Degree in..."""
        )
    
    st.divider()
    
    # Generate button
    generate_button = st.button("🚀 Generate Application Materials")



# Main area
st.title("💼 AI Job Application Assistant")
st.markdown("Upload a job description and your background — our AI team will craft your perfect application.")
st.divider()

# Validation and generation
if generate_button:
    if not job_description.strip():
        st.error("❌ Please paste a job description first.")
    elif not candidate_background.strip():
        st.error("❌ Please provide your background — either upload a PDF or type it manually.")
    else:
        # Show progress
        st.info("🤖 Your AI team is working on your application...")
        
        progress_col1, progress_col2, progress_col3 = st.columns(3)
        
        with progress_col1:
            st.markdown("**1. Job Analyst** 🔍")
            st.caption("Analyzing job requirements...")
        
        with progress_col2:
            st.markdown("**2. Resume Tailor** ✍️")
            st.caption("Tailoring your resume...")
        
        with progress_col3:
            st.markdown("**3. Cover Letter Writer** 📝")
            st.caption("Writing cover letter...")
        
        # Run the crew
        with st.spinner("AI agents working... this takes about 1-2 minutes"):
            result = run_crew(job_description, candidate_background)
            st.session_state.results = result  # save to session state

# Show instructions if nothing generated yet
if not st.session_state.results:
    st.markdown("""
    ### How it works
    
    **Step 1** — Paste the job description in the sidebar
    
    **Step 2** — Upload your resume PDF or type your background
    
    **Step 3** — Click Generate and let the AI team work
    
    ---
    
    ### Your AI Team
    
    🔍 **Job Analyst** — Extracts requirements, keywords, and culture insights
    
    ✍️ **Resume Tailor** — Rewrites your resume to match the job perfectly
    
    📝 **Cover Letter Writer** — Crafts a personalized, compelling cover letter
    
    ---
    
    *Results include download buttons so you can save everything locally.*
    """)

# Show results if they exist in session state
if st.session_state.results:
    st.success("✅ Your application materials are ready!")
    st.divider()
    
    result = st.session_state.results
    
    tab1, tab2, tab3 = st.tabs([
        "🔍 Job Analysis",
        "📄 Tailored Resume",
        "✉️ Cover Letter"
    ])
    
    with tab1:
        st.subheader("Job Analysis")
        st.markdown(result["job_analysis"])
        st.download_button(
            label="📥 Download Analysis",
            data=result["job_analysis"],
            file_name="job_analysis.txt",
            mime="text/plain"
        )
    
    with tab2:
        st.subheader("Tailored Resume")
        st.markdown(result["tailored_resume"])
        st.download_button(
            label="📥 Download Resume",
            data=result["tailored_resume"],
            file_name="tailored_resume.txt",
            mime="text/plain"
        )
    
    with tab3:
        st.subheader("Cover Letter")
        st.markdown(result["cover_letter"])
        st.download_button(
            label="📥 Download Cover Letter",
            data=result["cover_letter"],
            file_name="cover_letter.txt",
            mime="text/plain"
        )

        