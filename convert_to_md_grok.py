import csv
import os
import json
from datetime import datetime

# Paths
csv_path = "F:\\0 - AI & Coding\\Sticky Notes\\Sticky_Notes.csv"
output_folder = "F:\\0 - AI & Coding\\Sticky Notes\\obsidian_notes"
os.makedirs(output_folder, exist_ok=True)

def apply_styles(text, styles):
    """Apply Markdown formatting based on styles."""
    if "strikethrough" in styles:
        text = f"~~{text}~~"
    if "italic" in styles:
        text = f"*{text}*"
    if "bold" in styles:
        text = f"**{text}**"
    # Note: Underline isn't standard in Markdown; ignored for now
    return text

def convert_block(block):
    """Convert a JSON block to Markdown."""
    content = block["content"]
    block_styles = block.get("blockStyles", {})
    is_list = block_styles.get("listType") == "bullet"
    
    text_segments = []
    for segment in content:
        text = segment["text"]
        styles = segment.get("styles", [])
        formatted_text = apply_styles(text, styles)
        text_segments.append(formatted_text)
    
    paragraph = "".join(text_segments)
    return f"- {paragraph}" if is_list else paragraph

def convert_document(document):
    """Convert the entire document to Markdown."""
    blocks = document["blocks"]
    markdown_blocks = [convert_block(block) for block in blocks]
    return "\n".join(markdown_blocks)

def create_front_matter(note_id, created_at, updated_at):
    """Create YAML front matter for Obsidian."""
    # Convert timestamps to readable format
    created_date = datetime.fromtimestamp(created_at/1000).strftime('%Y-%m-%d %H:%M:%S')
    updated_date = datetime.fromtimestamp(updated_at/1000).strftime('%Y-%m-%d %H:%M:%S')
    
    return f"""---
id: {note_id}
created: {created_date}
updated: {updated_date}
---
"""

# Process CSV
with open(csv_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    
    for i, row in enumerate(reader):
        last_server_version = row.get("LastServerVersion", "")
        note_id = row["Id"]
        
        try:
            note_data = json.loads(last_server_version)
            document = note_data["document"]
            created_at = int(note_data["createdAt"])
            updated_at = int(note_data["lastModified"])
            
            # Convert content to Markdown
            content = convert_document(document)
            front_matter = create_front_matter(note_id, created_at, updated_at)
            markdown_content = front_matter + content
            
            # Create filename using only the last updated date
            date_str = datetime.fromtimestamp(updated_at/1000).strftime('%Y-%m-%d')
            
            # Handle duplicate dates by adding a counter
            base_filename = os.path.join(output_folder, f"{date_str}.md")
            counter = 1
            note_filename = base_filename
            
            while os.path.exists(note_filename):
                note_filename = os.path.join(output_folder, f"{date_str}_{counter}.md")
                counter += 1
                
            with open(note_filename, "w", encoding="utf-8") as md_file:
                md_file.write(markdown_content)
        
        except json.JSONDecodeError:
            print(f"Row {i+1}: Invalid JSON in LastServerVersion")
        except KeyError as e:
            print(f"Row {i+1}: Missing key {e}")

print(f"Notes exported to Markdown files in '{output_folder}'!")