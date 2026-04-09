# import streamlit as st
# from indexer import index_pdf
# from retriever import retrieve_relevant_chunks
# from answerer import answer_question
# import tempfile
# import os

# st.set_page_config(
#     page_title="PDF Chatbot",
#     page_icon="📄",
#     layout="centered"
# )

# st.title("📄 PDF Chatbot")
# st.markdown("Upload a PDF and ask questions about it.")
# st.divider()

# uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

# if uploaded_file is not None:
#     # Check if this is a new file or same one
#     if "indexed_file" not in st.session_state or st.session_state.indexed_file != uploaded_file.name:
        
#         with st.spinner("Reading and indexing your PDF..."):
#             # Save uploaded file temporarily to disk
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#                 tmp.write(uploaded_file.read())
#                 tmp_path = tmp.name
            
#             # Index it
#             num_chunks = index_pdf(tmp_path)
            
#             # Delete temp file
#             os.unlink(tmp_path)
            
#             # Remember we indexed this file
#             st.session_state.indexed_file = uploaded_file.name
        
#         st.success(f"PDF indexed successfully! Created {num_chunks} chunks.")

#     st.divider()
#     st.subheader("Ask a question")
    
#     question = st.text_input("Your question", placeholder="What is this document about?")
    
#     if st.button("Get Answer 🔍"):
#         if question.strip() == "":
#             st.warning("Please type a question first.")
#         else:
#             with st.spinner("Searching document and generating answer..."):
#                 # Retrieve relevant chunks
#                 chunks = retrieve_relevant_chunks(question)
                
#                 # Generate answer
#                 answer = answer_question(question, chunks)
            
#             st.divider()
#             st.subheader("Answer")
#             st.write(answer)
            
#             # Show the chunks used (good for learning/debugging)
#             with st.expander("📚 View source chunks used"):
#                 for i, chunk in enumerate(chunks):
#                     st.markdown(f"**Chunk {i+1}:**")
#                     st.write(chunk)
#                     st.divider()



import streamlit as st
import hashlib
import os
import tempfile
from indexer import index_pdf
from retriever import retrieve_relevant_chunks
from answerer import answer_question

st.set_page_config(
    page_title="PDF Chatbot",
    page_icon="📄",
    layout="wide"  # wide gives us more space for chat + sidebar
)

st.markdown("""
<style>
    /* Remove default white header */
    header[data-testid="stHeader"] {
        background-color: #0e1117;
    }
    
    /* Main background */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* ALL text white everywhere */
    * {
        color: #e6edf3 !important;
    }
    
    /* File uploader box */
    [data-testid="stFileUploader"] {
        background-color: #161b22 !important;
        border: 1px dashed #30363d !important;
        border-radius: 8px;
    }
    
    /* File uploader inner area */
    [data-testid="stFileUploaderDropzone"] {
        background-color: #161b22 !important;
    }
    
    /* Browse files button */
    [data-testid="stFileUploaderDropzone"] button {
        background-color: #21262d !important;
        border: 1px solid #30363d !important;
        border-radius: 6px;
    }
    
    /* Nuke all chat input styling and start fresh */
    [data-testid="stChatInput"] {
        background-color: #161b22 !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }

    [data-testid="stChatInputContainer"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        outline: none !important;
    }

    [data-testid="stChatInputContainer"]:focus-within {
        border: 1px solid #58a6ff !important;
        box-shadow: none !important;
        outline: none !important;
    }

    [data-testid="stChatInputContainer"] textarea {
        background-color: #161b22 !important;
        color: #e6edf3 !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }

    /* Remove the outer white wrapper */
    [data-testid="stChatInput"] > div {
        background-color: #161b22 !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Bottom toolbar area */
    [data-testid="stBottom"] {
        background-color: #0e1117 !important;
    }
    
    /* Chat messages */
    [data-testid="stChatMessage"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d;
        border-radius: 8px;
        margin-bottom: 8px;
    }
    
    /* Expander */
    [data-testid="stExpander"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px;
    }
    
    /* Success alert */
    [data-testid="stAlert"] {
        background-color: #1a2e1a !important;
        border: 1px solid #56d364 !important;
    }
    
    /* Clear chat button */
    .stButton button {
        background-color: #21262d !important;
        border: 1px solid #30363d !important;
        border-radius: 6px;
        width: 100%;
    }
    
    .stButton button:hover {
        background-color: #30363d !important;
    }
    
    /* Divider */
    hr {
        border-color: #30363d !important;
    }

    /* Toolbar and deploy button area */
    .stToolbar {
        background-color: #0e1117 !important;
    }

    /* Fix white footer area */
    [data-testid="stBottom"] > div {
        background-color: #0e1117 !important;
    }

    /* Fix input bar - match sidebar color */
    [data-testid="stChatInputContainer"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }

    /* Remove red border on focus */
    [data-testid="stChatInputContainer"]:focus-within {
        border: 1px solid #58a6ff !important;
        box-shadow: none !important;
    }

    /* Input textarea */
    [data-testid="stChatInputContainer"] textarea {
        background-color: #161b22 !important;
    }

    /* Hide Streamlit footer */
    footer {
        display: none !important;
    }

    /* Slightly bigger font */
    [data-testid="stChatMessage"] p {
        font-size: 15px !important;
        line-height: 1.7 !important;
    }
            
    /* Nuclear fix for input box */
    .stChatInput, 
    .stChatInput *,
    [data-testid="stChatInput"],
    [data-testid="stChatInput"] *,
    [data-testid="stChatInputContainer"],
    [data-testid="stChatInputContainer"] * {
        background-color: #161b22 !important;
        background: #161b22 !important;
        color: #e6edf3 !important;
        border-color: #30363d !important;
        box-shadow: none !important;
        outline: none !important;
    }

    /* Single clean border on outer container only */
    [data-testid="stChatInputContainer"] {
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
    }

    /* Remove all inner borders */
    [data-testid="stChatInputContainer"] * {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state variables if they don't exist yet
if "messages" not in st.session_state:
    st.session_state.messages = []

if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = []  # list of filenames already indexed

with st.sidebar:
    st.title("📄 PDF Chatbot")
    st.markdown("---")
    
    st.subheader("Upload PDFs")
    
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type="pdf",
        accept_multiple_files=True  # key change - allows multiple files
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Check if already indexed using hash
            file_hash = hashlib.md5(uploaded_file.getvalue()).hexdigest()
            
            if file_hash not in st.session_state.indexed_files:
                with st.spinner(f"Indexing {uploaded_file.name}..."):
                    # Save temp file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(uploaded_file.read())
                        tmp_path = tmp.name
                    
                    # Index it
                    num_chunks = index_pdf(tmp_path, uploaded_file.name)
                    
                    # Clean up temp file
                    os.unlink(tmp_path)
                    
                    # Remember this file's hash
                    st.session_state.indexed_files.append(file_hash)
                
                st.success(f"✅ {uploaded_file.name} indexed! ({num_chunks} chunks)")
            else:
                st.info(f"📎 {uploaded_file.name} already indexed")
    
    st.markdown("---")
    
    # Show indexed files count
    if st.session_state.indexed_files:
        st.markdown(f"**{len(st.session_state.indexed_files)} PDF(s) loaded**")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# Main area
st.title("💬 Chat with your PDFs")

# Show message if no PDFs uploaded yet
if not st.session_state.indexed_files:
    st.info("👈 Upload one or more PDFs from the sidebar to get started.")

else:
    # Render full chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input - fixed at bottom
    if prompt := st.chat_input("Ask a question about your PDFs..."):
        
        # Add user message to history and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chunks, sources = retrieve_relevant_chunks(prompt)
                answer = answer_question(prompt, chunks, sources)
            
            st.markdown(answer)
            st.markdown(f" **Sources:** {', '.join(sources)}")
            
            # Show sources in expander
            with st.expander("📚 View source chunks"):
                for i, chunk in enumerate(chunks):
                    st.markdown(f"**Chunk {i+1}:**")
                    st.write(chunk)
                    st.divider()
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": answer})

