import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import CharacterTextSplitter
from langchain.schema import Document
from pinecone import Pinecone, ServerlessSpec

# Load environment variables (for API keys)
load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'qa' not in st.session_state:
    st.session_state.qa = None
if 'current_pdf' not in st.session_state:
    st.session_state.current_pdf = None

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to process the extracted text and store embeddings
def process_text(text):
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(text)
    documents = [Document(page_content=chunk[:4096]) for chunk in chunks]
    return documents

# Streamlit UI
st.title("PDF Question-Answering Chatbot")

# Upload PDF file
uploaded_pdf = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_pdf is not None and uploaded_pdf != st.session_state.current_pdf:
    st.session_state.current_pdf = uploaded_pdf
    
    # Extract text from the uploaded PDF
    pdf_text = extract_text_from_pdf(uploaded_pdf)
    
    # Process the text (split into smaller chunks and wrap them as Documents)
    documents = process_text(pdf_text)
    st.success(f"PDF processed successfully! Extracted {len(documents)} chunks.")
    
    # Delete existing index if it exists
    index_name = os.getenv("INDEX_NAME")
    if index_name in pc.list_indexes().names():
        pc.delete_index(index_name)
    
    # Create a new index
    pc.create_index(
        name=index_name,
        dimension=1536,  # OpenAI embeddings are 1536 dimensions
        metric='cosine',
        spec=ServerlessSpec(
            cloud=os.getenv("PINECONE_CLOUD", "aws"),
            region=os.getenv("PINECONE_REGION", "us-east-1")
        )
    )
    
    # Initialize embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    # Initialize vectorstore
    st.session_state.vectorstore = PineconeVectorStore.from_documents(
        documents,
        embeddings,
        index_name=index_name,
        pinecone_api_key=os.getenv("PINECONE_API_KEY")
    )
    
    # Initialize chat model
    chat = ChatOpenAI(verbose=True, temperature=0, model_name="gpt-3.5-turbo")
    
    # Initialize the conversational retrieval chain
    st.session_state.qa = ConversationalRetrievalChain.from_llm(
        llm=chat, chain_type="stuff", retriever=st.session_state.vectorstore.as_retriever()
    )
    
    # Clear chat history when a new PDF is uploaded
    st.session_state.chat_history = []

# Chatbot interaction
st.subheader("Ask a question about the PDF")
user_question = st.text_input("Your Question:")

if st.button("Ask"):
    if user_question and st.session_state.qa:
        # Get the chatbot response
        response = st.session_state.qa({"question": user_question, "chat_history": st.session_state.chat_history})
        st.write(f"*Answer*: {response['answer']}")
        
        # Update the chat history
        st.session_state.chat_history.append((user_question, response['answer']))
    elif not st.session_state.qa:
        st.warning("Please upload a PDF first.")

# Display chat history
if st.session_state.chat_history:
    st.subheader("Chat History")
    for q, a in st.session_state.chat_history:
        st.write(f"*Q*: {q}")
        st.write(f"*A*: {a}")
        st.write("---")

# End the conversation
if st.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.success("Chat history cleared.")