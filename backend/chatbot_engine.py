# backend/chatbot_engine.py

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from backend.vector import retriever


class ChatbotEngine:
    def __init__(self):
        # Load the LLM and prompt
        self.model = OllamaLLM(model="llama3.2")
        self.retriever = retriever

        self.template = """
        You are an expert medical assistant helping users with their health questions.
        Below are some related context excerpts: {reviews}
        Please provide a helpful and accurate answer to the following question: {question}
        """
        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.chain = self.prompt | self.model

    def ask(self, question: str) -> str:
        # Fetch relevant documents using retriever
        reviews = self.retriever.invoke(question)

        # Call the chain
        result = self.chain.invoke({"reviews": reviews, "question": question})
        return result
