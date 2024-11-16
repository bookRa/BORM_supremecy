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


def analyze_story(text):
    characters = query_openai(
        f"List all characters in the following story with descriptions: {text[:1500]}"
    )
    settings = query_openai(f"Describe the settings in this story: {text[:1500]}")
    script = query_openai(
        f"Convert this excerpt into a script format with dialogues and stage directions: {text[:1500]}"
    )
    return {"characters": characters, "settings": settings, "script": script}
