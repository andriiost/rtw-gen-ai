import json
from openai import OpenAI

# Load the JSON data from the file
with open("test_files.json", "r") as file:
    data = json.load(file)

client = OpenAI()

for name, text in zip(data["name"], data["text"]):
    prompt = f"""
    You will receive a text containing information about multiple accommodations. Extract each accommodation from the text with the following details:
    - Accommodation Name: The specific tool or method being used to accommodate workers. Retrieve directly from the text; do not create or alter names;;
    - Description: A detailed explanation of the accommodation.Get this info from the text directly. Retrieve directly from the text; do not create or alter description;ter names;
    - Injury Location Name: Choosing only from the list: {} indentify the part of the body that the accommodation aims to protect or assist;
    - Industry Name: Choosing only from the list: {} indentify the industry in which the accommodation is used (e.g., Construction);
    - Activity Name: Choosing only from the list: {} indentify the physical tasks associated with or accommodated by the accommodation.

    Format the extracted data as a JSON object, with an array if multiple are mentioned in the text. Use the following structure:
    {{
      "accommodations": [
        {{
          "accommodation_name": "",
          "description": "",
          "injury_location_name": "",
          "industry_name": "",
          "activity_name": ""
        }}
      ]
    }}

    Title: {name}
    Text: {text}
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to extract data from text and format it as JSON object."},
            {"role": "user", "content": prompt}
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    print(f"Response for '{name}':")
    print(response.choices[0].message.content)
    print("\n" + "=" * 50 + "\n")
