import os
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)

def generate_summary(content):
    """Generate a summary using the Gemini API"""
    if not content or content.strip() == "":
        return "No content to summarize."
    
    try:
        # Configure the model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Create the prompt
        prompt = f"""
        Please summarize the following content and extract key points:
        
        {content}
        
        Format the summary as bullet points with the most important insights.
        """
        
        # Generate the response
        response = model.generate_content(prompt)
        
        # Return the summary
        if response.text:
            return response.text
        else:
            return "Unable to generate summary."
            
    except Exception as e:
        return f"Error generating summary: {str(e)}"