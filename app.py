import streamlit as st
import pandas as pd
from process_text import test_process_pdf, process_pdf
from openai_api import test_analyze_story, analyze_story
from storyboard import test_display_dynamic_storyboard, display_dynamic_storyboard

st.title("Short Story Script Generator")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    st.write("File uploaded successfully!")
    clean_text_extract = test_process_pdf()
    # clean_text_extract = process_pdf(uploaded_file)
    # Display results in tabs

    (
        raw_text_tab,
        character_text_tab,
        settings_text_tab,
        script_text_tab,
        storyboard_tab,
    ) = st.tabs(["Raw Text", "Characters", "Settings", "Script", "Storyboard"])
    story_analysis = test_analyze_story(clean_text_extract)
    # story_an  alysis = analyze_story(clean_text_extract)
    with raw_text_tab:
        st.markdown(clean_text_extract)
    with character_text_tab:
        st.markdown(story_analysis["characters"])
    with settings_text_tab:
        st.markdown(story_analysis["settings"])
    with script_text_tab:
        st.markdown(story_analysis["script"])
    with storyboard_tab:
        st.header("Storyboard")
        st.write("Below is a visual storyboard of the scenes:")
        test_display_dynamic_storyboard()
