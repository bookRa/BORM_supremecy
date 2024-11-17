# %%
import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
import random
import requests
import uuid

load_dotenv()

# Set up the OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def generate_shot_descriptions(script, character_analysis, settings_analysis):
    """
    Generate a list of shot descriptions for a given script using GPT-4.
    Each shot description will include {setting: ...} and {character: ...} annotations.

    Args:
        script (str): The screenplay-style text for the scene.
        character_analysis (str): Freeform text describing characters and their roles.
        settings_analysis (str): Freeform text describing settings and context.

    Returns:
        list: A list of generated shot descriptions.
    """
    # System prompt to guide GPT-4
    system_prompt = """
    You are an expert in filmmaking and screenplay writing. Your task is to break down a scene script into detailed shot descriptions. Each shot must:

    1. Focus on a single moment or interaction.
    2. Use the exact {setting: ...} and {character: ...} annotations to maintain consistency.
    3. Avoid using any markdown formatting, including "plaintext" or code blocks.
    4. Avoid verbose prose and instead provide clear, actionable descriptions in the format below:
    
    Example shot descriptions:
    - {setting: village_square} {character: mr_summers} enters the square holding the black box. The camera pans to show his jovial expression as the villagers gather around.
    - {setting: village_square} {character: bobby_martin} dodges his {character: mother}'s grasp, running to a pile of stones with a mischievous laugh. The camera tracks his movement.

    Input Context:
    - The "Character Analysis" and "Settings Analysis" provide names and details for characters and settings.
    - The "Script" outlines the scene.

    Output Requirements:
    - Provide a list of shot descriptions, each starting with {setting: ...}.
    - Use {character: ...} tags for each character mentioned in the shot.
    - Use clear and concise descriptions without unnecessary detail.
    """

    # Prepare the user input
    user_input = f"""
    Script:
    {script}

    Character Analysis:
    {character_analysis}

    Settings Analysis:
    {settings_analysis}

    Please break the script into NO MORE THAN 5 OR 6 detailed shot descriptions.
    """

    # Call GPT-4 API
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        model="gpt-4o",
    )

    # Access the response content correctly
    content = response.choices[0].message.content

    # Split the response into a list of shot descriptions
    shots = content.strip().split("\n")
    return [shot.strip() for shot in shots if shot.strip()]


def generate_dalle_prompts(shot_descriptions, character_analysis, settings_analysis):
    """
    Generate DALLE prompts for each shot description using GPT-4.
    Each DALLE prompt will include details from the shot description, character analysis, and settings analysis.

    Args:
        shot_descriptions (list): List of detailed shot descriptions.
        character_analysis (str): Freeform text describing characters and their roles.
        settings_analysis (str): Freeform text describing settings and context.

    Returns:
        list: A list of DALLE prompts corresponding to the shot descriptions.
    """
    # System prompt to guide GPT-4
    system_prompt = """
    You are an expert at crafting detailed visual prompts for DALL-E, specifically designed to create consistent and visually engaging storyboards. Your task is to take shot descriptions, along with character and setting analyses, and generate one high-quality DALL-E prompt for each shot.

Each DALL-E prompt must:
1. Clearly describe the scene, focusing on:
   - **Actions**: What is happening in the scene.
   - **Characters**: Include character names, appearances, and emotions when available. Ensure each character is distinct and consistent with the character analysis.
   - **Settings**: Describe the environment, lighting, and mood in detail.
2. Emphasize dynamic and engaging visuals:
   - Use active verbs and highlight emotions to create compelling imagery.
   - Ensure all visual elements contribute to the mood and story of the scene.
3. Maintain a consistent artistic style across all prompts:
   - Include attributes like "soft, natural lighting," "vibrant color palette," "painterly style," and "dynamic composition."
   - Avoid varying artistic attributes unless explicitly instructed.

### **Output Format**
- A standalone, natural-language description suitable for DALL-E. Do not include any annotations like {setting: ...} or {character: ...}.
- Avoid using markdown, code blocks, or any unnecessary symbols.

### **Prompt Structure**
"A digital painting of [scene description]. The scene features [character details] in [setting details], with [action details]. The style includes [lighting], [color palette], and [artistic attributes]."

### **Examples**
1. For a shot where villagers gather in the village square:
   - "A digital painting of a lively village square under the morning sun. The scene features villagers casually gathering, some chatting while others arrange stones in a pile, with vibrant green grass and blossoming flowers in the background. The style includes soft natural lighting, a warm color palette, and a painterly composition."

2. For a shot where Mr. Summers arrives with the black box:
   - "A digital painting of a jovial man entering a sunny village square, carrying a black wooden box. The scene captures his warm smile and confident posture as villagers turn to greet him. The style includes golden lighting, dynamic framing, and a focus on ceremonial tradition."

3. For a mischievous moment with Bobby Martin:
   - "A digital painting of a young boy darting away from his mother’s grasp, laughing mischievously as he runs toward a pile of stones. The scene is set in a sunny village square with vibrant green grass and the warm colors of summer. The style includes dynamic movement, bright lighting, and a focus on youthful energy."

---

### **Input Context**
You will receive:
- **Shot Descriptions**: Detailed descriptions of individual moments in a scene.
- **Character Analysis**: A list of characters with their names, appearances, and roles.
- **Settings Analysis**: A description of the environment, mood, and spatial elements.

### **Output Requirements**
For each shot description:
1. Generate a single DALL-E prompt following the format provided.
2. Ensure that the prompt captures the details and tone of the shot description while enhancing visual and emotional impact.
3. Do not include any unnecessary formatting or redundant information.

    """

    # Prepare the user input
    user_input = f"""
    Shot Descriptions:
    {shot_descriptions}

    Character Analysis:
    {character_analysis}

    Settings Analysis:
    {settings_analysis}

    Please generate one DALLE prompt for each shot description.
    """

    # Call GPT-4 API
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        model="gpt-4o",
    )

    # Access the response content correctly
    content = response.choices[0].message.content

    # Split the response into individual DALLE prompts
    dalle_prompts = [prompt.strip() for prompt in content.split("\n") if prompt.strip()]
    return dalle_prompts


def generate_and_save_images(prompts, output_directory):
    """
    Generate and save images using OpenAI's DALL-E 3 API based on a list of prompts.

    Args:
        prompts (list): A list of text prompts to generate images for.
        output_directory (str): The directory to save the generated images.

    Returns:
        None: Saves images to the specified directory.
    """
    # Possible panel sizes for DALL-E
    panel_options = ["1024x1024", "1024x1792", "1792x1024"]

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Iterate through prompts
    for i, prompt in enumerate(prompts):
        try:
            # Randomly select a panel size
            size = random.choice(panel_options)

            # Generate image using the DALL-E 3 API
            response = client.images.generate(
                model="dall-e-3", prompt=prompt, n=1, size=size
            )

            # Extract the URL of the generated image
            image_url = response.data[0].url

            # Download the image content
            image_filename = os.path.join(output_directory, f"panel_{i+1}_{size}.png")
            image_response = requests.get(image_url)
            image_response.raise_for_status()

            # Save the image to the specified directory
            with open(image_filename, "wb") as image_file:
                image_file.write(image_response.content)

            print(f"Image saved: {image_filename}")

        except AttributeError as attr_err:
            print(f"Attribute error for prompt {i+1}: {attr_err}")
        except Exception as e:
            print(f"Error generating or saving image for prompt {i+1}: {e}")


def create_random_image_directory(base_dir="storyboard_images"):
    """
    Generate a unique random directory for saving images.

    Args:
        base_dir (str): The base directory where the random subdirectory will be created.

    Returns:
        str: The full path of the created directory.
    """
    # Generate a unique identifier for the directory
    random_dir_name = str(uuid.uuid4())[
        :8
    ]  # Use the first 8 characters of a UUID for brevity
    full_path = os.path.join(base_dir, random_dir_name)

    # Create the directory if it doesn't exist
    os.makedirs(full_path, exist_ok=True)

    return full_path
