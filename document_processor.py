import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

class DocumentProcessor:
    def __init__(self, file_paths):
        self.file_paths = [os.path.abspath(fp) for fp in file_paths]
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
        self.vector_store = None

    def process_documents(self):
        documents = []
        for file_path in self.file_paths:
            print(f"Processing file: {file_path}")
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = os.path.basename(file_path)
            documents.extend(docs)
        
        print(f"Total documents loaded: {len(documents)}")
        split_docs = self.text_splitter.split_documents(documents)
        print(f"Total chunks after splitting: {len(split_docs)}")

        if not os.path.exists("./chroma_db"):
            os.makedirs("./chroma_db")
        
        self.vector_store = Chroma.from_documents(split_docs, self.embeddings, persist_directory="./chroma_db")
        self.vector_store.persist()
        print("Vector store created and persisted.")

    def get_vector_store(self):
        if not self.vector_store:
            print("Loading existing vector store...")
            self.vector_store = Chroma(persist_directory="./chroma_db", embedding_function=self.embeddings)
        return self.vector_store
