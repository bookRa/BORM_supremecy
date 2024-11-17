import streamlit as st
import pandas as pd
from process_text import test_process_pdf, process_pdf
from openai_api import test_analyze_story, analyze_story
from storyboard import test_display_dynamic_storyboard, display_dynamic_storyboard
from storyboard_generator_pipeline import (
    generate_shot_descriptions,
    generate_dalle_prompts,
    generate_and_save_images,
    create_random_image_directory,
)


st.title("Short Story Script Generator")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    st.write("File uploaded successfully!")
    # clean_text_extract = test_process_pdf()
    clean_text_extract = process_pdf(uploaded_file)
    # Display results in tabs

    (
        raw_text_tab,
        character_text_tab,
        settings_text_tab,
        script_text_tab,
        storyboard_tab,
    ) = st.tabs(["Raw Text", "Characters", "Settings", "Script", "Storyboard"])
    # story_analysis = test_analyze_story(clean_text_extract)
    story_analysis = analyze_story(clean_text_extract)
    characters = story_analysis["characters"]
    settings = story_analysis["settings"]
    scripts = story_analysis["script"]
    with raw_text_tab:
        st.markdown(clean_text_extract)
    with character_text_tab:
        st.markdown(characters)
    with settings_text_tab:
        st.markdown(settings)
    with script_text_tab:
        st.markdown(scripts)
    with storyboard_tab:
        st.header("Storyboard")
        st.write("Below is a visual storyboard of the scenes:")
        shot_descriptions = generate_shot_descriptions(scripts, characters, settings)
        dalle_prompts = generate_dalle_prompts(shot_descriptions, characters, settings)
        directory = create_random_image_directory()
        generate_and_save_images(dalle_prompts, directory)
        # test_display_dynamic_storyboard()
        display_dynamic_storyboard(directory)
