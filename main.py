import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama

# Custom CSS for styling
st.markdown(
    """
    <style>
        .main-container {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 2px 2px 15px rgba(0,0,0,0.1);
        }
        .stButton>button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            font-size: 16px;
        }
        .stTextArea textarea {
            background-color: #ffffff;
            border-radius: 10px;
        }
        .title-container {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            color: #2E3B4E;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="title-container">🌍 AI Web Scraper</div>', unsafe_allow_html=True)

# --- CONTAINER 1: SCRAPING SECTION ---
with st.container():
    st.markdown("### 🔍 Scrape a Website")
    url = st.text_input("Enter the URL", key="url_input")
    
    if st.button("Scrape Site"):
        if url:
            st.write("🚀 Scraping the website...")
            result = scrape_website(url)
            body_content = extract_body_content(result)
            cleaned_content = clean_body_content(body_content)
            st.session_state.dom_content = cleaned_content
            st.success("✅ Scraping completed!")
        else:
            st.error("⚠️ Please enter a valid URL.")

# --- CONTAINER 2: DISPLAY SCRAPED CONTENT ---
if "dom_content" in st.session_state:
    with st.container():
        st.markdown("### 📜 Scraped DOM Content")
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", st.session_state.dom_content, height=250)

# --- CONTAINER 3: PARSING SECTION ---
if "dom_content" in st.session_state:
    with st.container():
        st.markdown("### 🛠️ Parse Content with AI")
        parse_description = st.text_area("Describe what you want to parse")

        if st.button("Parse Content"):
            if parse_description:
                st.write("🧠 Parsing the content...")

                # Parse the content with Ollama
                dom_chunks = split_dom_content(st.session_state.dom_content)
                parsed_result = parse_with_ollama(dom_chunks, parse_description)
                
                st.success("✅ Parsing completed!")
                st.write(parsed_result)
            else:
                st.error("⚠️ Please enter a description to parse the content.")

