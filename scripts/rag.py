import ollama
import csv
import re
import json
import textwrap

# good, mistral
# file_path = "/Users/jake/Dropbox/Games/Doom/WADs/Maps/1337.TXT"

# bad, mistral
# file_path = "/Users/jake/Dropbox/Games/Doom/WADs/Maps/1monster.txt"

# decent, mistral
# file_path = "/Users/jake/Dropbox/Games/Doom/WADs/Maps/10sector.txt"

# very good, mistral
# file_path = "/Users/jake/Dropbox/Games/Doom/WADs/Maps/Sacrment.txt"

# ok, mistral. you'll need to merge multiple map IDs records using if empty etc
# file_path = "/Users/jake/Dropbox/Games/Doom/WADs/Maps/SERENITY.TXT"

# bad, mistral
# file_path = "/Users/jake/Dropbox/Games/Doom/WADs/Maps/FAVA.TXT"

# good, mistral
# file_path = "/Users/jake/Dropbox/Games/Doom/WADs/Maps/ENIGMA.TXT"

# ok, mistral
#file_path = "/Users/jake/Dropbox/Games/Doom/WADs/Maps/megawads/scythe.txt"

# kinda bad, mistral
# file_path = "/Users/jake/Dropbox/Games/Doom/WADs/Maps/megawads/stardate20x6.txt"

file_path = "tests/txt/REQUIEM.TXT"

# TODO: deffo need to rework the splitting so it can use broader context

model = "deepseek-r1:14b"
# model = "mistral"

MAX_TOKENS = 8192  # Adjust per model
CHUNK_SIZE = 4000  # Smaller than max to avoid truncation
OVERLAP = 2000      # Overlap for context continuity

def split_text_cleverly(content):

    section_pattern = re.compile(r"([-=]{10,}\s*.*?\s*[-=]{10,})", re.MULTILINE)
    sections = section_pattern.split(content)  # Split while keeping section headers

    # Step 2: Structure sections
    structured_sections = []
    for i in range(0, len(sections), 2):
        header = sections[i].strip() if i < len(sections) else ""
        body = sections[i + 1].strip() if i + 1 < len(sections) else ""
        # structured_sections.append((header, body))
        structured_sections.append(f"{header} {body}")

    return structured_sections

# TODO more clever text splitting
def split_text_with_overlap(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """Splits text into overlapping character-based chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += chunk_size - overlap  # Move forward but keep overlap
    return chunks

def get_content(file_path):
    content = ""
    for encoding in ("utf-8", "latin-1", "windows-1252"):
        try:
            with open(file_path, "r", encoding=encoding) as f:
                content = f.read()
        except UnicodeDecodeError:
            continue

    return content

def start():

    content = get_content(file_path)

    chunks = split_text_cleverly(content)

    # Chunk the text for large context processing
    # chunks = split_text_with_overlap(content)

    # Process each chunk using Ollama
    maps_data = []
    for idx, chunk in enumerate(chunks):
        prompt = f"""
        Given this text, please find the map or mission number if present (map to JSON as "mapId"), the map name or title if present (map to JSON as "mapTitle"), and the author names (map to JSON as "author") if present:
        
        {textwrap.shorten(chunk, width=MAX_TOKENS)}

        Return just the requested fields in valid, compact JSON with no line breaks, no additional text.
        """

        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])

        try:

            response_text = response["message"]["content"]
            think_match = re.search(r"<think>(.*?)</think>", response_text, re.DOTALL)
            json_only = re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL).strip()
            json_match = re.search(r"{.*}", json_only, re.DOTALL)

            think_text = think_match.group(1).strip() if think_match else ""
            json_text = json_match.group(0).strip() if json_match else ""

            print(think_text)
            result = json.loads(json_text)  # Convert JSON string to Python dict
            maps_data.append(result)
        except Exception as e:
            print(f"Error parsing Ollama response for chunk {idx}: {e}\n\t{response.get("message")}")
            # print(response["message"]["content"])

    # TODO: feed the array back in to the LLM to normalise it: "I have this JSON array of objects that must be reformatted so that map or mission ID always uses the key "mapId" and contains only an integer:""
    extended = []
    for maps_datum in maps_data:
        extended.extend(maps_datum)

    return

if __name__ == "__main__":
    start()
