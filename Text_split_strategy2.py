import yaml
import os
import re
from pathlib import Path
import pandas as pd
from datetime import datetime
import nltk
nltk.download('punkt')

# Load settings from settings.yml
settings_path = "./settings.yaml"
with open(settings_path, "r") as file:
    settings = yaml.safe_load(file)

from graphrag.index.utils.hashing import gen_md5_hash

# Extract settings
encoding_name = settings['encoding_model']
input_base_dir = settings['input']['base_dir']
file_pattern = settings['input']['file_pattern']
output_dir = settings['storage']['base_dir']
timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
output_dir = output_dir.replace('${timestamp}', timestamp)
os.makedirs(output_dir, exist_ok=True)

# Specify your input file
input_file_name = 'input_file'
input_file_path = input_file_name  # Since we have the full path

# Check if the file exists
if not os.path.isfile(input_file_path):
    raise FileNotFoundError(f"Input file not found: {input_file_path}")

# Read the text from the input file
with open(input_file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Normalize line endings
text = text.replace('\r\n', '\n').replace('\r', '\n')

# Remove leading/trailing whitespace if desired
text = text.strip()

# Extract metadata (if applicable)
group = {}  # You can populate this with metadata if needed

# Generate document_id
new_item = {**group, "text": text}
new_item["id"] = gen_md5_hash(new_item, new_item.keys())
document_id = new_item["id"]

# Split the text into sentences using NLTK
from nltk.tokenize import sent_tokenize

sentences = sent_tokenize(text)

# Process each sentence as a chunk
chunk_data = []
for i, chunk_text in enumerate(sentences):
    # Normalize line endings in chunk_text
    chunk_text = chunk_text.replace('\r\n', '\n').replace('\r', '\n')

    # Remove leading/trailing whitespace if desired
    chunk_text = chunk_text.strip()

    # Count tokens in the chunk (optional)
    # You can use your tokenization method here if needed
    # For simplicity, we'll count words as tokens
    n_tokens = len(chunk_text.split())

    # Create item for hashing
    item = {
        'chunk_text': chunk_text,
    }

    # Generate chunk_id
    chunk_id = gen_md5_hash(item, ['chunk_text'])

    chunk_data.append({
        'id': chunk_id,
        'document_id': document_id,
        'chunk_index': i,
        'chunk_text': chunk_text,
        'n_tokens': n_tokens,
        'source': os.path.relpath(input_file_path, input_base_dir),
    })

# Create DataFrame and save
chunk_df = pd.DataFrame(chunk_data)
chunk_df = chunk_df[['id', 'document_id', 'chunk_index', 'chunk_text', 'n_tokens', 'source']]
chunk_df.to_csv(os.path.join(output_dir, "chunked_text.csv"), index=False)

# Optional: Print the DataFrame
print(chunk_df)
