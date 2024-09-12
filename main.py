import json
from openai import OpenAI

# Load the JSON data from the file
with open("test_files.json", "r") as file:
    data = json.load(file)

client = OpenAI()

for name, text in zip(data["name"], data["text"]):
    prompt = f"""
    Extract the following information from the provided text:
    - Accommodation Name: The specific tool or method being used to accommodate workers.
    - Description: A detailed explanation of the accommodation.
    - Injury Location Name: The part of the body that the accommodation aims to protect or assist.
    - Industry Name: The industry in which the accommodation is used (e.g., Construction).
    - Activity Name: The physical tasks involved with the accommodation.

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
