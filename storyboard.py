import streamlit as st


def display_dynamic_storyboard(scenes, image_urls):
    """
    Display a dynamic storyboard layout inspired by the provided image.
    :param scenes: List of scene descriptions.
    :param image_urls: List of image URLs (placeholder or generated).
    """
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

    # Create a dynamic layout inspired by the attached image
    st.write("### Storyboard")

    # Layout with rows and columns
    col1, col2 = st.columns([3, 2])  # Adjust relative sizes
    with col1:
        st.markdown('<div class="storyboard-panel">', unsafe_allow_html=True)
        st.image(image_urls[0], caption=scenes[0])
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="storyboard-panel">', unsafe_allow_html=True)
        st.image(image_urls[1], caption=scenes[1])
        st.markdown("</div>", unsafe_allow_html=True)

    # Second row with multiple columns
    col3, col4, col5 = st.columns([1, 2, 1])  # Adjust sizes for visual interest
    with col3:
        st.markdown('<div class="storyboard-panel">', unsafe_allow_html=True)
        st.image(image_urls[2], caption=scenes[2])
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="storyboard-panel">', unsafe_allow_html=True)
        st.image(image_urls[3], caption=scenes[3])
        st.markdown("</div>", unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="storyboard-panel">', unsafe_allow_html=True)
        st.image(image_urls[4], caption=scenes[4])
        st.markdown("</div>", unsafe_allow_html=True)


# Placeholder data for demonstration
test_scenes = [
    "Scene 1: The villagers gather.",
    "Scene 2: Mr. Summers arrives.",
    "Scene 3: Tessie protests.",
    "Scene 4: The black box is opened.",
    "Scene 5: The final outcome.",
]

test_image_urls = [
    "https://via.placeholder.com/600x800",
    "https://via.placeholder.com/400x600",
    "https://via.placeholder.com/300x300",
    "https://via.placeholder.com/700x500",
    "https://via.placeholder.com/500x500",
]


# Call the function in the storyboard tab
def test_display_dynamic_storyboard():
    display_dynamic_storyboard(test_scenes, test_image_urls)
