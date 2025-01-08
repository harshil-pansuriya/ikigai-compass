import streamlit as st
from utils.vector_store import clear_vectordb
from utils.rag_chain import generate_response
from utils.prompts import CHAT_PROMPT

def initialize_chat():
    if "chat_history" not in st.session_state:
        welcome_message = {
            "role": "assistant",
            "content": "👋 Hello! I'm your Ikigai assistant. How can I help you today?"
        }
        st.session_state.chat_history = [welcome_message]

def display_chat_messages():
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

def handle_user_input(user_input):
    if not user_input:
        return
        
    # Add user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })
    
    # Get relevant context from vector store
    context = st.session_state.vector_store.similarity_search(user_input, k=2)
    context_text = "\n".join([doc.page_content for doc in context])
    
    # Get chat history for context
    chat_history = "\n".join([
        f"{msg['role']}: {msg['content']}"
        for msg in st.session_state.chat_history[-4:]  # Last 4 messages for context
    ])
    
    # Generate response using unified prompt
    prompt = CHAT_PROMPT.format(
        chat_history=chat_history,
        context=context_text,
        question=user_input
    )
    
    response = generate_response(st.session_state.rag_chain, prompt)
    
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })

def main():
    st.title("💭 Ikigai Chat Assistant")
    
    initialize_chat()
    
    # Clear DB button
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("Clear DB", use_container_width=True):
            clear_vectordb(st.session_state.vector_store)
            st.session_state.chat_history = []
            st.rerun()
    
    # Display chat
    display_chat_messages()
    
    # Chat input
    if user_input := st.chat_input("Ask me anything..."):
        handle_user_input(user_input)
        st.rerun()

if __name__ == "__main__":
    main()