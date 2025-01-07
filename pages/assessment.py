import streamlit as st
from utils.vector_store import store_user_answer
from utils.rag_chain import generate_response
from utils.prompts import IKIGAI_QUESTIONS, IKIGAI_IMPROVEMENT_PROMPT

def initialize_assessment():
    if "question_index" not in st.session_state:
        st.session_state.question_index = 0
        st.session_state.completed_questions = False
        st.session_state.answers = []

def show_progress():
    current = st.session_state.question_index + 1
    total = len(IKIGAI_QUESTIONS)
    progress = st.session_state.question_index / len(IKIGAI_QUESTIONS)
    st.progress(progress, text=f"Question {current} of {total}")

def display_current_question():
    question = IKIGAI_QUESTIONS[st.session_state.question_index]
    st.header(question["question"])
    st.write(question["description"])
    return question

def handle_user_answer(question, answer):
    answer_data = {
        "category": question["category"],
        "question": question["question"],
        "answer": answer
    }
    
    st.session_state.answers.append(answer_data)
    store_user_answer(st.session_state.vector_store, answer_data)
    
    if st.session_state.question_index < len(IKIGAI_QUESTIONS) - 1:
        st.session_state.question_index += 1
    else:
        st.session_state.completed_questions = True

def generate_analysis():
    if "analysis" not in st.session_state:
        answers_text = "\n\n".join([
            f"Category: {ans['category']}\n"
            f"Question: {ans['question']}\n"
            f"Answer: {ans['answer']}"
            for ans in st.session_state.answers
        ])
        
        prompt = IKIGAI_IMPROVEMENT_PROMPT.format(user_answers=answers_text)
        st.session_state.analysis = generate_response(
            st.session_state.rag_chain,
            prompt
        )

def main():
    st.title("🎯 Ikigai Assessment")
    
    initialize_assessment()
    
    if not st.session_state.completed_questions:
        show_progress()
        current_q = display_current_question()
        
        user_answer = st.text_area(
            "Your answer:",
            key=f"q_{st.session_state.question_index}"
        )
        
        is_last = st.session_state.question_index == len(IKIGAI_QUESTIONS) - 1
        button_text = "Generate Analysis" if is_last else "Next"
        
        if st.button(button_text):
            if user_answer:
                handle_user_answer(current_q, user_answer)
                st.rerun()
            else:
                st.warning("Please provide an answer before continuing.")
    else:
        generate_analysis()
        st.markdown("#### Your Ikigai Analysis")
        st.write(st.session_state.analysis)
        st.markdown("#### 💭 Want to explore more?")
        st.markdown("Head to the Chatbot page to ask questions about your Ikigai journey!")

if __name__ == "__main__":
    main()