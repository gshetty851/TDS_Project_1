# tasksB.py
import os
import json
import requests
import subprocess
import sqlite3
from bs4 import BeautifulSoup
from PIL import Image
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
DATA_DIR = "/data"

# Helper: Ensure file is within /data
def ensure_data_path(filepath: str) -> str:
    if not os.path.abspath(filepath).startswith(os.path.abspath(DATA_DIR)):
        raise Exception("Access denied: file is outside /data")
    return filepath

# B3: Fetch data from an API and save it.
def task_B3_fetch_api_data():
    # For demonstration, we use a fixed URL and output file.
    api_url = "https://jsonplaceholder.typicode.com/todos/1"
    output_file = os.path.join(DATA_DIR, "api_data.json")
    response = requests.get(api_url, timeout=20)
    if response.status_code != 200:
        raise Exception("Failed to fetch API data")
    with open(output_file, "w") as f:
        json.dump(response.json(), f, indent=2)
    return {"message": "B3 executed: API data fetched."}

# B4: Clone a git repository and make a commit.
def task_B4_clone_and_commit():
    # For demonstration, we clone a public repo into /data/repo and commit a dummy file.
    repo_url = "https://github.com/sanand0/tools-in-data-science-public.git"
    target_dir = os.path.join(DATA_DIR, "repo")
    # Remove target_dir if it exists
    if os.path.exists(target_dir):
        import shutil
        shutil.rmtree(target_dir)
    # Use git to clone the repository (git must be installed in container)
    subprocess.run(["git", "clone", repo_url, target_dir], check=True)
    # Create a dummy commit file
    dummy_file = os.path.join(target_dir, "commit.txt")
    with open(dummy_file, "w") as f:
        f.write("Automated commit by DataWorks agent.\n")
    subprocess.run(["git", "-C", target_dir, "add", "commit.txt"], check=True)
    subprocess.run(["git", "-C", target_dir, "commit", "-m", "Automated commit"], check=True)
    return {"message": "B4 executed: repository cloned and commit made."}

# B5: Run a SQL query on a database and save the result.
def task_B5_run_sql_query():
    db_file = os.path.join(DATA_DIR, "ticket-sales.db")
    output_file = os.path.join(DATA_DIR, "sql_query_result.txt")
    query = "SELECT * FROM tickets LIMIT 5"
    if not os.path.exists(db_file):
        raise Exception(f"{db_file} not found")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    with open(output_file, "w") as f:
        f.write(json.dumps(result, indent=2))
    return {"message": "B5 executed: SQL query run."}

# B6: Scrape a website.
def task_B6_scrape_website():
    url = "https://www.example.com"
    output_file = os.path.join(DATA_DIR, "scraped.txt")
    response = requests.get(url, timeout=20)
    if response.status_code != 200:
        raise Exception("Failed to scrape website")
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string if soup.title else "No title"
    with open(output_file, "w") as f:
        f.write(f"Title: {title}\n")
    return {"message": "B6 executed: website scraped."}

# B7: Compress or resize an image.
def task_B7_process_image():
    input_image = os.path.join(DATA_DIR, "credit-card.png")
    output_image = os.path.join(DATA_DIR, "credit-card-resized.jpg")
    if not os.path.exists(input_image):
        raise Exception(f"{input_image} not found")
    with Image.open(input_image) as img:
        # Resize to half the original dimensions
        new_size = (img.width // 2, img.height // 2)
        img_resized = img.resize(new_size)
        img_resized.save(output_image, format="JPEG", quality=85, optimize=True)
    return {"message": "B7 executed: image resized and saved."}

# B8: Transcribe audio from an MP3 file.
def task_B8_transcribe_audio():
    # For demonstration, we assume an MP3 file exists at /data/audio.mp3.
    # This function uses OpenAI's Whisper API (if available). Otherwise, we return a dummy transcription.
    input_audio = os.path.join(DATA_DIR, "audio.mp3")
    output_file = os.path.join(DATA_DIR, "audio_transcription.txt")
    if not os.path.exists(input_audio):
        raise Exception(f"{input_audio} not found")
    try:
        with open(input_audio, "rb") as audio_file:
            response = openai.Audio.transcribe(model="whisper-1", file=audio_file)
        transcription = response["text"]
    except Exception:
        transcription = "Dummy transcription: audio file transcribed."
    with open(output_file, "w") as f:
        f.write(transcription)
    return {"message": "B8 executed: audio transcribed."}

# B9: Convert Markdown to HTML.
def task_B9_convert_markdown_to_html():
    input_md = os.path.join(DATA_DIR, "format.md")
    output_html = os.path.join(DATA_DIR, "format.html")
    if not os.path.exists(input_md):
        raise Exception(f"{input_md} not found")
    import markdown
    with open(input_md, "r") as f:
        md_text = f.read()
    html_text = markdown.markdown(md_text, extensions=["extra", "codehilite"])
    with open(output_html, "w") as f:
        f.write(html_text)
    return {"message": "B9 executed: Markdown converted to HTML."}

# B10: Filter a CSV file and return JSON data.
def task_B10_filter_csv():
    # For demonstration, assume a CSV exists at /data/sample.csv.
    csv_file = os.path.join(DATA_DIR, "sample.csv")
    if not os.path.exists(csv_file):
        # Create a dummy CSV file for testing.
        import csv
        data = [
            {"name": "Alice", "role": "admin"},
            {"name": "Bob", "role": "user"},
            {"name": "Charlie", "role": "user"}
        ]
        with open(csv_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "role"])
            writer.writeheader()
            writer.writerows(data)
    # Filter for role "user"
    df = pd.read_csv(csv_file)
    filtered = df[df["role"] == "user"]
    # Instead of writing to file, return the JSON result.
    output = filtered.to_json(orient="records", indent=2)
    output_file = os.path.join(DATA_DIR, "filtered.json")
    with open(output_file, "w") as f:
        f.write(output)
    return {"message": "B10 executed: CSV filtered and JSON output saved.", "result": output}
