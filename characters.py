from openai_api import analyze_story
import re


def bold_character_names(characters_text):
    """
    Add bold formatting to character names in the extracted character list.
    """
    # Use regex to match the name/role line (first line of each character description)
    bolded_text = re.sub(r"^([\w\s\/]+)(?=\s*\()", r"**\1**", characters_text, flags=re.MULTILINE)
    return bolded_text

