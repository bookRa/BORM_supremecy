import streamlit as st
import pandas as pd
from process_text import test_process_pdf, process_document
from openai_api import test_analyze_story, analyze_story
import time

st.title("Short Story Script Generator")
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf","epub"])


if uploaded_file is not None:
    st.write("File uploaded successfully!")
    # clean_text_extract = test_process_pdf(uploaded_file)
    progress_bar = st.progress(0)
    status_text = st.empty()
    status_text.write("Processing the uploaded file...")
    progress_bar.progress(10)
    clean_text_extract = process_document(uploaded_file)
    status_text.write("Analyzing the story...")
    progress_bar.progress(25)  
    for i in range(26, 99):  
        if i <= 100:  
            progress_bar.progress(i)
            time.sleep(0.1)  
        if 'story_analysis' in locals():  
            break  
    story_analysis = analyze_story(clean_text_extract)
    status_text.write("Finalizing results...")
    progress_bar.progress(100)  

    # Display results in tabs
    raw_text_tab, character_text_tab, settings_text_tab, script_text_tab = st.tabs(
        ["Raw Text", "Characters", "Settings", "Script"]
    )
    # story_analysis = test_analyze_story(clean_text_extract)
    with raw_text_tab:
        st.text(clean_text_extract)
    with character_text_tab:
        st.text(story_analysis["characters"])
    with settings_text_tab:
        st.text(story_analysis["settings"])
    with script_text_tab:
        st.text(story_analysis["script"])
