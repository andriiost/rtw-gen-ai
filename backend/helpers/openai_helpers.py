from openai import AzureOpenAI
import os
import json
from datetime import datetime

# Azure OpenAI setup
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("OPENAI_API_VERSION")
)

deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# Helper function to process extracted text with Azure OpenAI
def process_with_openai(filename, file_extension, extracted_text):
    """
    Process extracted text using Azure OpenAI's GPT model to generate structured accommodation data.

    This function sends a structured prompt containing text about multiple accommodations to Azure OpenAI.
    The model processes the text and extracts details such as accommodation name, description, 
    injury location, industry, injury nature, and a summary of the document.

    :param filename: The name of the document being processed.
    :param file_extension: The extension of the file (e.g., 'pdf', 'docx').
    :param extracted_text: The text extracted from the document that needs to be processed.
    
    :return: A dictionary with accommodations and the document description in JSON format. 
             Each accommodation includes its name, description, injury location, industry, 
             injury nature, and additional metadata such as 'verified' status and 'date_created'.
    """
    prompt = f"""
    You will receive a text containing information about multiple accommodations. Extract each accommodation from the text with the following details:
    - Accommodation Name: The specific tool or method being used to accommodate workers. Retrieve directly from the text; do not create or alter names;;
    - Description: A detailed explanation of the accommodation.Get this info from the text directly. Retrieve directly from the text; do not create or alter description;ter names;
    - Injury Location Name: Choosing only from the list: {"Body systems", "Multiple body parts", "Cranial region, including skull", "Leg(s)", "Lower back (lumbar, sacral, coccygeal regions)", "Shoulder", "Ankle(s)", "Finger(s), fingernail(s)", "Arm(s)", "Wrist(s)", "Not Coded", "Foot (feet), except toe(s)", "Chest, including ribs, internal organs", "Pelvic region", "Upper extremities, unspecified, NEC", "Multiple trunk locations", "Multiple lower extremities locations", "Hand(s), except finger(s)", "Upper back (cervical, thoracic regions)", "Multiple back regions", "Abdomen", "Back, unspecified, NEC", "Head, unspecified, NEC", "Eye(s)", "Face", "Toe(s), toenail(s)", "Ear(s)", "Multiple head locations", "Lower extremities, unspecified, NEC", "Trunk, unspecified, NEC", "Other body parts including unclassified, NEC"} identify the part of the body that the accommodation aims to protect or assist;
    - Industry Name: Choosing only from the list: {"Agriculture, forestry, fishing, and hunting", "Mining, quarrying, and oil and gas extraction", "Utilities", "Construction", "Manufacturing", "Wholesale trade", "Retail trade", "Transportation and warehousing", "Information and cultural industries", "Finance and insurance", "Real estate and rental and leasing", "Professional, scientific, and technical services", "Management of companies and enterprises", "Administrative and support, waste management, and remediation services", "Educational services", "Health care and social assistance", "Arts, entertainment, and recreation", "Accommodation and food services", "Other services (except public administration)", "Public administration"} identify the industry in which the accommodation is used (e.g., Construction). If there is no industry specified say "Multiple";
    - Injury Nature Name: Choosing only from the list: {"Sprains and strains", "Psychiatric", "Fractures", "Concussion", "Traumatic injuries, disorders, complications, unspecified, NEC", "Multiple traumatic injuries", "Bruises, contusions", "COVID-19 novel coronavirus", "Intracranial injuries excluding concussions"} identify the nature of the injury that the accommodation aims to address. If there is no nature specified say "Multiple".
    - Summary: please create a summary of the document so that any one who wishes to know what the document is about can get a brief overview. Please take ideas directly from the document only.

    Format the extracted data as a JSON object, with an array if multiple are mentioned in the text. Use the following structure:
    {{
      "accommodations": [
        {{
         "accommodation_name": "",
          "accommodation_description": "",
          "injury_location_name": "",
          "industry_name": "",
          "injury_nature_name": ""
        }}
      ], 
      "document_description": ""
    }}
    Title: {filename}
    Text: {extracted_text}
    """
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to extract data from text and format it as JSON object."},
            {"role": "user", "content": prompt}
        ],
        # past_messages=10,
        max_tokens=2000,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )
    # Parse the response JSON string into a Python dictionary
    extracted_json = json.loads(response.choices[0].message.content)
    # Add verified and date_created fields
    current_date = datetime.now().strftime("%Y-%m-%d")  # Current date only
    for accommodation in extracted_json['accommodations']:
        accommodation['verified'] = False
        accommodation['date_created'] = current_date  # Assuming JSON format in response
    
    extracted_json["document_name"] = filename
    extracted_json["extension"] = file_extension
    return extracted_json