from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def initialize_vectoredb():
    embeddings= HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store= Chroma(persist_directory="chroma_db", embedding_function=embeddings)
    
    return vector_store

def store_user_answer(vector_store, answer_data):
    text = (
        f"Category: {answer_data['category']}\n"
        f"Question: {answer_data['question']}\n"
        f"Answer: {answer_data['answer']}"
    )
    metadata = {
        "category": answer_data["category"],
        "question": answer_data["question"]
    }
    vector_store.add_texts(texts=[text], metadatas=[metadata])
    vector_store.persist()
    
def get_relevant_answers(vector_store, query, k=3):
    return vector_store.similarity_search(query, k=k)
    

def clear_vectordb(vector_store):
    vector_store._collection.delete(where={"$and": [{}]})
    vector_store.persist()