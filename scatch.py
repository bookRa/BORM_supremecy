# %%
import os
from dotenv import load_dotenv
import pandas as pd
from openai import OpenAI
from openai_api import query_openai
from process_text import test_process_pdf

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def analyze_story(prompt, text):
    return query_openai(f"{prompt} {text[:1500]}")


# %%
def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


# analyze_story(read_file("settings_prompt.md"), test_process_pdf())

# %%

df = pd.read_csv("extracted_story_details.csv")
df.columns


# %%
print(df["Settings"])
df["Settings"] = read_file("canned_setting.md")
print(df["Settings"])
df.to_csv(path_or_buf=r"extracted_story_details.csv", sep=",", header=True, index=False)

# %%
analyze_story(
    read_file("prompt_for_settings_extraction.md"), read_file("canned_setting.md")
)


# %%
import json
from io import StringIO

response = json.load(
    StringIO(
        '{\n  "Time of Day and Weather": "A clear and sunny morning on June 27th, indicating the fresh warmth of a full-summer day with profusely blossoming flowers and richly green grass.",\n  "Village Square": "Located between the post office and the bank, serving as the central gathering place for the villagers.",\n  "Population Size": "A small village with about three hundred people, allowing the lottery event to be completed in less than two hours.",\n  "Children\'s Gathering": "The children gather first, with a recently ended school term creating a sense of uneasy liberty. The boys engage in collecting stones and forming piles, while the girls stand and talk among themselves. Very small children are either rolling in the dust or holding onto older siblings."\n}'
    )
)

print(response)


# %%
print(type(response))
for setting, description in response.items():
    print(f"{setting}: {description}")
