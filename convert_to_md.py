import csv
import os
from datetime import datetime

# Path to your CSV and output folder
csv_path = "F:\\0 - AI & Coding\\Projects\\Sticky Notes\\Sticky_Notes.csv"
output_folder = "F:\\0 - AI & Coding\\Projects\\Sticky Notes\\obsidian_notes"
os.makedirs(output_folder, exist_ok=True)

def format_date(date_str):
    """Convert date string to a readable format"""
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%B %d, %Y at %I:%M %p')  # Example: April 2, 2025 at 03:30 PM
    except:
        return date_str

# Read CSV and create Markdown files
with open(csv_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    
    # Check if required columns exist
    if "Text" not in reader.fieldnames:
        raise ValueError('The CSV file does not contain a "Text" column.')

    for i, row in enumerate(reader):
        note_content = row["Text"]
        updated_at = row.get("UpdatedAt", "")
        
        # Format the date for display
        formatted_date = format_date(updated_at) if updated_at else f"Note {i+1}"

        # Handle empty content
        if not note_content:
            note_content = f"Note {i+1} is empty."

        # Add Markdown formatting
        markdown_content = f"""# {formatted_date}

{note_content}"""

        # Write to Markdown file using the original timestamp as filename
        note_filename = os.path.join(output_folder, f"{updated_at or f'Note_{i+1}'}.md")
        try:
            with open(note_filename, "w", encoding="utf-8") as md_file:
                md_file.write(markdown_content)
        except Exception as e:
            print(f"Failed to write {note_filename}: {e}")

print(f"Notes exported to Markdown files in '{output_folder}'!")