from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import logging
import google.generativeai as genai
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load environment variables
load_dotenv()

# API Key Configuration
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Validate API Keys
if not GEMINI_API_KEY:
    logger.error("Missing GEMINI_API_KEY. Please check your .env file.")
    raise ValueError("GEMINI_API_KEY is required")

# Configure the Gemini API key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model
llm = genai.GenerativeModel("gemini-1.5-flash")

# Define a function for generating responses
def generate_response(llm, prompt, context, input_text):
    # Combine system prompt and input
    full_prompt = prompt.format(context=context) + "\n\n" + input_text
    # Generate content without additional arguments
    response = llm.generate_content(full_prompt)
    return response.text

# Simulate retrieval (mock context retrieval)
def mock_retriever(query):
    return "Mocked retrieved context for: " + query

# Prompt Template
system_prompt = "You are a helpful medical assistant."

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    try:
        msg = request.form.get("msg", "")
        
        if not msg:
            return jsonify({"error": "No message provided"}), 400

        logger.info(f"User Input: {msg}")
        
        # Retrieve context (mocked here)
        retrieved_context = mock_retriever(msg)
        
        # Generate response using Gemini model
        response_text = generate_response(llm, system_prompt, retrieved_context, msg)
        
        logger.info(f"Bot Response: {response_text}")
        return str(response_text)
    
    except Exception as e:
        logger.error(f"Chat processing error: {e}")
        return "An error occurred while processing your request", 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
    
