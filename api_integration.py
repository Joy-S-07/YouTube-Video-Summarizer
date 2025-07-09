import google.generativeai as genai

api_key = "YOUR_API_KEY"
client = genai.configure(api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

transcript_str = "TRANSCRIPT_EXTRACTED_FROM_VIDEO"

prompt = f'''
    Given the transcript of a YouTube video and its title, generate a detailed summary of the transcript in JSON format. The summary should capture the main points of the video, focusing on key ideas, themes, or arguments presented. Make sure to translate things in English. Do not use any special characters or like '\\n' like terms.

    Use the following JSON structure for the output and dont add "```json```":

        "Title": "Title from the Transcript,"
        "Summary of the Video": "Detailed summary here"

    Transcript:
    {transcript_str}
    '''

response = model.generate_content(prompt)