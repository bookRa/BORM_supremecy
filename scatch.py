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


analyze_story(read_file("settings_prompt.md"), test_process_pdf())

# %%

df = pd.read_csv("extracted_story_details.csv")
df.columns


# %%
print(df["Settings"])
df["Settings"] = read_file("canned_setting.md")

print(df["Settings"])
# df.to_csv(path_or_buf=r"extracted_story_details.csv", sep=",", header=True, index=False)
