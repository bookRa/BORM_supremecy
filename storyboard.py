import os
import streamlit as st


def display_dynamic_storyboard(image_directory):
    """
    Display a dynamic storyboard layout using images from a directory.

    Args:
        image_directory (str): The directory containing the storyboard images.
    """
    # Get a list of image files sorted by filename
    image_files = sorted(
        [
            os.path.join(image_directory, f)
            for f in os.listdir(image_directory)
            if f.endswith(".png")
        ]
    )

    # Define CSS for styling
    st.markdown(
        """
        <style>
        .storyboard-panel {
            text-align: center;
            margin: 10px;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .storyboard-panel img {
            max-width: 100%;
            height: auto;
        }
        .storyboard-caption {
            padding: 10px;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display storyboard title
    st.write("### Storyboard")

    # Dynamically create rows for images
    num_columns = 3  # Number of columns per row
    columns = st.columns(num_columns)  # Create placeholders for the first row

    for idx, image_path in enumerate(image_files):
        # Dynamically choose a column to place the image in
        with columns[idx % num_columns]:
            st.markdown('<div class="storyboard-panel">', unsafe_allow_html=True)
            st.image(image_path, caption=f"Panel {idx + 1}")
            st.markdown("</div>", unsafe_allow_html=True)


# Call the function in the storyboard tab
def test_display_dynamic_storyboard():
    display_dynamic_storyboard("./storyboard_images")
