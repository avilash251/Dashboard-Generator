import os
import google.generativeai as genai

# Load your Gemini API key (replace or use .env loader)
os.environ["GEMINI_API_KEY"] = "AIzaSyDoxaPFy-Bk4hPQUKGYXrDdlAcNTB0kbus"

# Configure Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

try:
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content("Give me 3 DevOps metrics to monitor")
    print(response.text)
except Exception as e:
    print("Error: ", str(e))