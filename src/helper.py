# from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings
# # Correct imports for HuggingFaceEmbeddings and HuggingFaceHub
# from langchain_community.llms import HuggingFaceHub  # For HuggingFaceHub
# from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader


# #Extract Data from the PDF file
# def load_pdf_file(data):
#     loader = DirectoryLoader(data,
#                              glob = "*.pdf",
#                              loader_cls=PyPDFLoader)
    
#     documents = loader.load()
#     return documents


# #chunking operation
# # split the data into text chunks
# def text_split(extracted_data):
#     text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap = 20) 
#     text_chunks = text_splitter.split_documents(extracted_data)
#     return text_chunks



# #download the embeddings from the hugging face
# def download_hugging_face_embeddings():
#     embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
#     return embeddings
# embeddings = download_hugging_face_embeddings()







from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceHub  # For HuggingFaceHub

# Extract Data from the PDF file
def load_pdf_file(data):
    loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

# Chunking operation
# Split the data into text chunks
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

# Download the embeddings from Hugging Face
def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return embeddings

embeddings = download_hugging_face_embeddings()