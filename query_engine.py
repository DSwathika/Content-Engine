from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class QueryEngine:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.llm = CTransformers(
            model="TheBloke/Llama-2-7B-Chat-GGML",
            model_type="llama",
            config={'max_new_tokens': 512, 'context_length': 2048, 'temperature': 0.01}
        )
        
        prompt_template = """
        Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't have enough information, don't try to make up an answer.

        {context}

        Question: {question}
        Answer: Let's approach this step-by-step:
        1) First, let's identify the key points from the context that are relevant to the question.
        2) Then, we'll organize these points into a coherent answer.
        3) If there's not enough information to answer the question, we'll clearly state that.

        Based on the context provided:
        """
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 5}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )

    def query(self, question):
        print(f"Received query: {question}")
        result = self.qa_chain({"query": question})
        print(f"Raw result: {result}")
        return result

    def process_raw_result(self, raw_result):
        answer = raw_result['result'].strip()
        sources = raw_result['source_documents']
        
        if not answer or "don't have enough information" in answer.lower():
            return "I don't have enough information to answer this question based on the provided documents.", []

        processed_answer = f"{answer}\n\nSources:\n"
        unique_sources = set()
        for source in sources:
            source_info = f"Document: {source.metadata['source']}, Page: {source.metadata.get('page', 'N/A')}"
            if source_info not in unique_sources:
                unique_sources.add(source_info)
                processed_answer += f"- {source_info}\n"
        
        return processed_answer, list(unique_sources)
