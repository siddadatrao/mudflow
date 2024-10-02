import os
import requests
from bs4 import BeautifulSoup
import re
import assemblyai as aai
from .upload_utils import clump_text, send_data_to_pinecone
from .utils import connections

# Function to save the transcript in a folder called 'transcripts'
def save_transcript(transcript, new_file_name):
    folder_name = "transcripts"

    # Create 'transcripts' folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Full path to the file
    print(folder_name)
    print(new_file_name)
    full_file_path = os.path.join(folder_name, new_file_name)

    # Save the transcript to the new file
    with open(full_file_path, 'w') as f:
        f.write(transcript.text)
    

    openai_connection, pinecone_connection, openai_key, pinecone_key = connections()

    # Push to pinecone
    clumped_text = clump_text(transcript.text, 8)
    send_data_to_pinecone(clumped_text, openai_connection, pinecone_connection, "podcasts", "medrag")

    print(f"Transcript saved as {full_file_path}")


def change_extension_to_txt(filename):
    # Extract only the base filename, removing the directory path
    base_filename = os.path.basename(filename)
    
    # Check if the file has a .mp3 extension
    if base_filename.endswith(".mp3"):
        # Remove the .mp3 extension and add .txt
        new_filename = base_filename[:-4] + ".txt"
        
        # Rename the file
        os.rename(filename, new_filename)
        print(f"File renamed to {new_filename}")
        return new_filename
    else:
        print(f"The file {filename} does not have a .mp3 extension.")
        return None

def get_script(filename):
    aai_key = os.environ.get('AAIKEY')

    aai.settings.api_key = "9383688bb8884261ac74da3484cc0c15"
    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(filename)

    return transcript.text

def cleanup(filename):
    os.remove(filename)

def sanitize_filename(filename):
    """Remove illegal characters from the filename and replace spaces with underscores."""
    # Replace spaces with underscores
    filename = filename.replace(" ", "_")
    # Remove illegal characters for filenames
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_podcast(url, save_directory):
    # Fetch the webpage content
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return

    # Parse the webpage to find the MP3 link and title
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the title of the page
    title_tag = soup.find('title')
    title = title_tag.text if title_tag else "podcast"
    title = sanitize_filename(title)  # Sanitize the title for use as a filename

    # Find the MP3 link
    audio_tag = soup.find('audio')
    
    if audio_tag and 'src' in audio_tag.attrs:
        mp3_url = audio_tag['src']
        print(f"MP3 URL found: {mp3_url}")

        # Fetch the MP3 file
        mp3_response = requests.get(mp3_url)
        if mp3_response.status_code == 200:
            # Ensure the save directory exists
            if not os.path.exists(save_directory):
                print("make directory")
                os.makedirs(save_directory)

            # Create the full file path with the title and ".mp3" extension
            file_name = os.path.join(save_directory, f"{title}.mp3")

            # Save the MP3 file
            with open(file_name, 'wb') as f:
                f.write(mp3_response.content)
            print(f"MP3 file saved as {file_name}")
            return file_name
        else:
            print("Failed to download the MP3 file.")
    else:
        print("No MP3 link found on the provided page.")

if __name__ == "__main__":
    # Example Substack podcast URL
    podcast_url = input("Enter the Substack podcast URL: ")
    
    # Local directory to save the MP3 file
    save_directory = "./podcasts"

    # Call the download function
    download_podcast(podcast_url, save_directory)
