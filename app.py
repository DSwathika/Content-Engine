import streamlit as st
import os
from document_processor import DocumentProcessor
from query_engine import QueryEngine
from chatbot import Chatbot

st.set_page_config(page_title="Multi-Document Comparison Analysis", layout="wide")

def main():
    st.title("Multi-Document Comparison Analysis Engine")

    # File uploader
    uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True, type="pdf")

    if uploaded_files:
        with st.spinner("Processing documents..."):
            if not os.path.exists("uploads"):
                os.makedirs("uploads")
            file_paths = []
            for file in uploaded_files:
                file_path = os.path.join("uploads", file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                file_paths.append(file_path)
            
            processor = DocumentProcessor(file_paths)
            processor.process_documents()
            vector_store = processor.get_vector_store()
            query_engine = QueryEngine(vector_store)
            chatbot = Chatbot(query_engine)
        
        st.success("Documents processed successfully!")

        # Chatbot interface
        st.subheader("Ask questions about the documents:")
        user_input = st.text_input("Enter your question:")
        
        if user_input:
            try:
                answer = chatbot.chat(user_input)
                st.markdown(answer)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.exception(e)
        
        # Display conversation history
        with st.expander("View Conversation History"):
            st.text(chatbot.get_conversation_history())

    else:
        st.info("Please upload PDF files to start the analysis.")

if __name__ == "__main__":
    main()
