from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_mistralai.chat_models import ChatMistralAI
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Mistral model
llm = ChatMistralAI(
    model="mistral-small",
    temperature=0.5,
    api_key=os.getenv("MISTRAL_API_KEY")
)

# Prompt template for answer generation
prompt_template = PromptTemplate(
    input_variables=["question", "context"],
    template="""
Answer the question based on the property listings provided.

Question: {question}
You were given these matching properties from the database:
Property Listings:
{context}

Answer in a clear, friendly, and helpful tone, like a real estate assistant.
"""
)

qa_chain = LLMChain(llm=llm, prompt=prompt_template)
