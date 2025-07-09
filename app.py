from youtube_transcript_api import YouTubeTranscriptApi
import re
import google.generativeai as genai
from fastapi import FastAPI
import json

app = FastAPI()

# Configure Gemini API key
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-2.5-flash")

def parse_summary_json(json_string):
    try:
        # Convert JSON string to dictionary
        data = json.loads(json_string)

        # Print nicely (optional)
        print("Title:", data.get("Title", "N/A"))
        print("\nSummary:\n", data.get("Summary of the Video", "N/A"))
        return data  # Returns as a usable dictionary

    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        return None
    


# Function to extract video ID from YouTube URL
def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None


# Generate summary using Gemini
def generate_summary(transcript_str):
    prompt = f'''
    Given the transcript of a YouTube video and its title, generate a detailed summary of the transcript in JSON format. The summary should capture the main points of the video, focusing on key ideas, themes, or arguments presented. Make sure to translate things in English. Do not use any special characters or like '\\n' like terms.

    Use the following JSON structure for the output and dont add "```json```":

        "Title": "Title from the Transcript,"
        "Summary of the Video": "Detailed summary here"

    Transcript:
    {transcript_str}
    '''

    response = model.generate_content(prompt)
    return response.text

# FastAPI POST route to accept video URL from client like Postman
@app.get("/summarize")

async def summarize(url: str):    
    video_id = extract_video_id(url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["af", "am", "ar", "az", "be", "bg", "bn", "bs", "ca", "cs", "cy", "da", "de", "el","en", "en-GB", "en-US", "eo", "es", "es-419", "et", "eu", "fa", "fi", "fil", "fr", "fr-CA","gl", "gu", "he", "hi", "hr", "hu", "hy", "id", "is", "it", "ja", "jv", "ka", "kk", "km","kn", "ko", "lo", "lt", "lv", "ml", "mn", "mr", "ms", "my", "ne", "nl", "no", "or", "pa", "pl", "pt", "pt-BR", "pt-PT", "ro", "ru", "si", "sk", "sl", "sq", "sr", "sv", "sw", "ta", "te", "th", "tr", "uk", "ur", "uz", "vi", "zh", "zh-CN", "zh-HK", "zh-TW", "zu"])

    if transcript:
        summary = generate_summary(transcript)
        return parse_summary_json(summary)
    else:
        return {"error":"invalid transcript"}