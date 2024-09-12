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
    - Injury Location Name: Choosing only from the list: {"Body systems", "Multiple body parts", "Cranial region, including skull", "Leg(s)", "Lower back (lumbar, sacral, coccygeal regions)", "Shoulder", "Ankle(s)", "Finger(s), fingernail(s)", "Arm(s)", "Wrist(s)", "Not Coded", "Foot (feet), except toe(s)", "Chest, including ribs, internal organs", "Pelvic region", "Upper extremities, unspecified, NEC", "Multiple trunk locations", "Multiple lower extremities locations", "Hand(s), except finger(s)", "Upper back (cervical, thoracic regions)", "Multiple back regions", "Abdomen", "Back, unspecified, NEC", "Head, unspecified, NEC", "Eye(s)", "Face", "Toe(s), toenail(s)", "Ear(s)", "Multiple head locations", "Lower extremities, unspecified, NEC", "Trunk, unspecified, NEC", "Other body parts including unclassified, NEC"} indentify the part of the body that the accommodation aims to protect or assist;
    - Industry Name: Choosing only from the list: {"Agriculture, forestry, fishing and hunting", "Mining, quarrying, and oil and gas extraction", "Utilities", "Construction", "Manufacturing", "Wholesale trade", "Retail trade", "Transportation and warehousing", "Information and cultural industries", "Finance and insurance", "Real estate and rental and leasing", "Professional, scientific, and technical services", "Management of companies and enterprises", "Administrative and support, waste management, and remediation services", "Educational services", "Health care and social assistance", "Arts, entertainment, and recreation", "Accommodation and food services", "Other services (except public administration)", "Public administration"} indentify the industry in which the accommodation is used (e.g., Construction);
    - Activity Name: Indentify the physical tasks associated with or accommodated by the accommodation.

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
