import pandas as pd
import json
import re

def clean_text_minimal(text):
    text = str(text)  # Ensure text is a string
    text = re.sub(r'(\w)-\s+(\w)', r'\1\2', text)
    text = re.sub(r'\r\n|\r|\n', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    text = text.strip()  # Remove leading and trailing whitespace
    return text

judge_id = 2738

# Load the data
with open(f"data/raw/{judge_id}.json", 'r') as file:
    data = json.load(file)

# Prepare the data
opinions_data = [{'id': opinion['id'], 'plain_text': opinion['plain_text']} for opinion in data]

# Create a DataFrame
df = pd.DataFrame(opinions_data)

# Apply the minimal cleaning function
df['plain_text'] = df['plain_text'].apply(clean_text_minimal)

# Define paths for cleaned data
cleaned_json_path = f"data/clean/{judge_id}.json"
cleaned_csv_path = f"data/clean/{judge_id}.csv"

# Save to JSON and CSV
df.to_json(cleaned_json_path, orient='records', lines=True, indent=4)
df.to_csv(cleaned_csv_path, index=False)
