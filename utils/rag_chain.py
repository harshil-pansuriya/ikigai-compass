import os
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

def create_rag_chain(vector_store):
    
    llm = ChatGroq(api_key= os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")
    
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever= vector_store.as_retriever(),
        memory=memory
    )
    return chain

def generate_response(chain, question):
    return chain.run(question)