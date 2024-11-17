import os
from dotenv import load_dotenv
import pandas as pd
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# for testing purposes
df = pd.read_csv("extracted_story_details.csv")


def query_openai(prompt, model="gpt-4o"):
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
    )
    return response.choices[0].message.content


def test_analyze_story(text):
    characters = df.Characters[0]
    settings = df.Settings[0]
    script = df.Script[0]
    return {"characters": characters, "settings": settings, "script": script}


def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def analyze_story(text):
    characters_prompt = f"""
    List all characters, from most to least important, in this story in this format:
    
    Name/Role (possible nicknames, omit if none)
    Characteristics: (list top three characteristics)
    Physical Description (generate physical traits that fit the character's personality):
    Description (of the character, a few sentences):
    No extra formatting chars please!
    """
    characters = query_openai(f"{characters_prompt} {text[:29000]}")
    settings = query_openai(f"{read_file('settings_prompt.md')} {text[:1500]}")
    script = query_openai(
        f"Convert this excerpt into a script format with dialogues and stage directions: {text[:1500]}"
    )
    return {"characters": characters, "settings": settings, "script": script}
