import re

class Chatbot:
    def __init__(self, query_engine):
        self.query_engine = query_engine
        self.conversation_history = []

    def chat(self, user_input):
        self.conversation_history.append(f"Human: {user_input}")
        
        sub_queries = self.decompose_query(user_input)
        
        full_answer = ""
        all_sources = set()
        for sub_query in sub_queries:
            raw_result = self.query_engine.query(sub_query)
            processed_answer, sources = self.query_engine.process_raw_result(raw_result)
            full_answer += f"For the query '{sub_query}':\n{processed_answer}\n\n"
            all_sources.update(sources)
        
        comparison = self.compare_results(sub_queries, full_answer)
        
        final_answer = f"{full_answer}\nComparison:\n{comparison}\n\nAll Sources:\n"
        for source in all_sources:
            final_answer += f"- {source}\n"
        
        self.conversation_history.append(f"AI: {final_answer}")
        return final_answer

    def decompose_query(self, query):
        # Simple decomposition based on "and" keyword and question marks
        sub_queries = re.split(r'\band\b|\?', query.lower())
        sub_queries = [sq.strip() + "?" for sq in sub_queries if sq.strip()]
        return sub_queries if sub_queries else [query]

    def get_conversation_history(self):
        return "\n".join(self.conversation_history)
