import streamlit as st
from PIL import Image
from utils.vector_store import initialize_vectoredb
from utils.rag_chain import create_rag_chain

def setup_page_config():
    st.set_page_config(
        page_title="Ikigai Compass",
        page_icon="🎯",
        layout="wide"
    )

def initialize_services():
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = initialize_vectoredb()
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = create_rag_chain(st.session_state.vector_store)

def display_content():
    st.title("🎯 Welcome to Ikigai Compass")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        ## What is Ikigai?
        
        Ikigai (生き甲斐) is a Japanese concept that means 'reason for being.' It represents 
        the intersection of four fundamental elements:
        
        1. **What you Love** (Passion) 💝: 
        2. **What the World Needs** (Mission) 🌍 : 
        3. **What you are Good At** (Profession) ⭐ :
        4. **What you can be Paid For** (Vocation) 💰 :
        
        ### Why Find Your Ikigai?
        - Discover your life's purpose
        - Achieve better work-life harmony
        - Increase personal satisfaction
        - Make meaningful contributions
        - Create sustainable success
        """)

    with col2:
        try:
            image = Image.open('assets/ikigai.png')
            st.image(image, caption='The Four Elements of Ikigai', use_container_width=True)
        except FileNotFoundError:
            st.error("Ikigai diagram image not found")

        st.info("""
        📝 **The Process:**
        1. Answer four key Ikigai questions
        2. Receive personalized analysis
        3. Explore deeper with AI chat support
        """)

def display_footer():
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <small>
                Discover your purpose. Find your balance. Live your Ikigai.
            </small>
        </div>
        """, 
        unsafe_allow_html=True
    )

def main():
    setup_page_config()
    initialize_services()
    display_content()
    display_footer()

if __name__ == "__main__":
    main()