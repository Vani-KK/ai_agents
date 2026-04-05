import streamlit as st
from indexer import index_pdf
from retriever import retrieve_relevant_chunks
from answerer import answer_question
import tempfile
import os

st.set_page_config(
    page_title="PDF Chatbot",
    page_icon="📄",
    layout="centered"
)

st.title("📄 PDF Chatbot")
st.markdown("Upload a PDF and ask questions about it.")
st.divider()

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file is not None:
    # Check if this is a new file or same one
    if "indexed_file" not in st.session_state or st.session_state.indexed_file != uploaded_file.name:
        
        with st.spinner("Reading and indexing your PDF..."):
            # Save uploaded file temporarily to disk
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            
            # Index it
            num_chunks = index_pdf(tmp_path)
            
            # Delete temp file
            os.unlink(tmp_path)
            
            # Remember we indexed this file
            st.session_state.indexed_file = uploaded_file.name
        
        st.success(f"PDF indexed successfully! Created {num_chunks} chunks.")

    st.divider()
    st.subheader("Ask a question")
    
    question = st.text_input("Your question", placeholder="What is this document about?")
    
    if st.button("Get Answer 🔍"):
        if question.strip() == "":
            st.warning("Please type a question first.")
        else:
            with st.spinner("Searching document and generating answer..."):
                # Retrieve relevant chunks
                chunks = retrieve_relevant_chunks(question)
                
                # Generate answer
                answer = answer_question(question, chunks)
            
            st.divider()
            st.subheader("Answer")
            st.write(answer)
            
            # Show the chunks used (good for learning/debugging)
            with st.expander("📚 View source chunks used"):
                for i, chunk in enumerate(chunks):
                    st.markdown(f"**Chunk {i+1}:**")
                    st.write(chunk)
                    st.divider()