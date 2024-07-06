
# Content Engine for Analysing multiple PDFs

This Content Engine is designed to analyze and compare multiple PDF documents, specifically identifying and highlighting their differences. The system utilizes Retrieval Augmented Generation (RAG) techniques to effectively retrieve, assess, and generate insights from the documents.


## Setup

This project implements the following key components:

    Backend Framework: LangChain
    Frontend Framework: Streamlit
    Vector Store: Chroma
    Embedding Model: HuggingFace MiniLM
    Local Language Model: TheBloke/ Llama-2-7B-Chat-GGML

## Installation


- Clone the repository

        git clone (https://github.com/DSwathika/Content-Engine)

        cd content-engine

- Install dependencies

        pip install -r requirements.txt

- Download and set up models

        Download the required models for embeddings and the language model. Place them in the appropriate directories.

- Run the application

        streamlit run app.py

## Project Structure


    content-engine/
    ├── app.py                    
    ├── chatbot.py              
    ├── document_processor.py     
    ├── query_engine.py          
    ├── requirements.txt         
    └── README.md                 
## Functionalities

1. Document Processing
    
    The DocumentProcessor class in document_processor.py is responsible for:

- Loading PDF documents
- Extracting text
- Splitting the text into chunks
- Generating embeddings for the text chunks
- Storing the embeddings in a Chroma vector store

2. Query Engine
    
    The QueryEngine class in query_engine.py is responsible for:

- Utilizing the Llama-2 model for generating answers based on retrieved document chunks
- Handling the retrieval of relevant document chunks using the Chroma vector store
- Structuring the answers and source document references


3. Chatbot Interface
    The Chatbot class in chatbot.py is responsible for:

- Decomposing complex user queries into sub-queries
- Handling multiple sub-queries and consolidating the results
- Comparing and highlighting differences between the results of sub-queries
- Managing the conversation history

4. Streamlit Interface
    The app.py file is responsible for:

- Setting up the Streamlit interface
- Handling file uploads for PDF documents
- Processing documents and initializing the vector store
- Allowing users to enter queries and displaying the answers and comparisons

## Expected Outcome


- A scalable and modular architecture for the Content Engine.
- Locally running LLM ensuring data privacy and reducing dependency on external APIs.
- A chatbot interface for interacting with the system, allowing users to obtain insights and compare information across the documents.
- Comprehensive documentation and user guides for ease of use.

## Authors

- [Swathika](https://github.com/DSwathika)

