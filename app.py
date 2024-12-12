# from flask import Flask, render_template,jsonify, request
# from src.helper import download_hugging_face_embeddings
# from langchain_pinecone import PineconeVectorStore
# from langchain.llms import HuggingFaceHub
# from langchain.prompts import ChatPromptTemplate
# from langchain.chains import create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate
# from dotenv import load_dotenv
# from langchain_huggingface import HuggingFaceEndpoint
# from langchain_community.llms import HuggingFaceHub
# # Correct imports for HuggingFaceEmbeddings and HuggingFaceHub

# from langchain_huggingface import HuggingFaceEmbeddings  # For embeddings


# from src.prompt import *
# import os


# app = Flask(__name__)

# load_dotenv()


# PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
# os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY  # Correct way to set the environment variable

# HUGGINGFACEHUB_API_TOKEN = os.environ.get('HUGGINGFACEHUB_API_TOKEN')
# os.environ['HUGGINGFACEHUB_API_TOKEN'] = HUGGINGFACEHUB_API_TOKEN  # Correct way to set the environment variable


# embeddings =  download_hugging_face_embeddings()

# index_name = "medi-chatbot"


# #embed each chunk and upsert the embeddings into the pine cone index.
# docsearch = PineconeVectorStore.from_existing_index(
#     index_name=index_name,
#     embedding=embeddings,
# )

# retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})


# # Hugging Face Hub ke liye free model configuration
# llm = HuggingFaceHub(
#     repo_id="google/flan-t5-large",
#     model_kwargs={
#         "temperature": 0.7,
#         "max_new_tokens": 250,
#         "top_p": 0.9
#     }
# )
# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", system_prompt),
#         ("human", "{input}")
#     ]
# )


# # Create a chain for generating responses
# question_answer_chain = create_stuff_documents_chain(llm,prompt)
# rag_chain = create_retrieval_chain(retriever,question_answer_chain)

# @app.route("/")
# def index():
#     return render_template('chat.html')

# @app.route("/get", methods=["GET", "POST"])
# def chat():
#     msg = request.form["msg"]
#     input = msg
#     print(input)
#     response = rag_chain.invoke({"input": msg})
#     print("Response : ", response["answer"])
#     return str(response["answer"])


# if __name__ == 'main':
#     app.run(host="0.0.0.0", port = 8080, debug= True)



from flask import Flask, render_template, request, jsonify
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load environment variables
load_dotenv()

# API Key Configuration
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
HUGGINGFACEHUB_API_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN')

# Validate API Keys
if not PINECONE_API_KEY or not HUGGINGFACEHUB_API_TOKEN:
    logger.error("Missing API keys. Please check your .env file.")
    raise ValueError("API keys are required")

# Download embeddings
try:
    embeddings = download_hugging_face_embeddings()
except Exception as e:
    logger.error(f"Embedding download failed: {e}")
    raise

# Pinecone Index Configuration
index_name = "medi-chatbot11"

# Initialize Vector Store
try:
    docsearch = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=embeddings,
    )
    retriever = docsearch.as_retriever(
        search_type="similarity", 
        search_kwargs={"k": 3}
    )
except Exception as e:
    logger.error(f"Vector store initialization failed: {e}")
    raise

# Language Model Configuration
llm = HuggingFaceHub(
    repo_id="google/flan-t5-large",
    model_kwargs={
        "temperature": 0.7,
        "max_length": 250
    }
)

# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful medical assistant."),
    ("human", "Context: {context}\n\nQuestion: {input}")
])

# Create Response Generation Chain
try:
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
except Exception as e:
    logger.error(f"Chain creation failed: {e}")
    raise

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    try:
        msg = request.form.get("msg", "")
        
        if not msg:
            return jsonify({"error": "No message provided"}), 400

        logger.info(f"User  Input: {msg}")
        
        # Invoke RAG chain
        response = rag_chain.invoke({"input": msg})
        
        # Extract answer
        answer = response.get('answer', 'No response generated')
        
        logger.info(f"Bot Response: {answer}")
        return str(answer)
    
    except Exception as e:
        logger.error(f"Chat processing error: {e}")
        return "An error occurred while processing your request", 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)