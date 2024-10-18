# Retrieval-Augmented Generation (RAG) Model for QA Bot

This project is a PDF Question-Answering Chatbot that uses Streamlit for the user interface, Pinecone for vector storage, LangChain for text processing, and OpenAI for generating embeddings and providing answers. It allows users to upload a PDF, extract its contents, and interact with a chatbot to ask questions based on the content of the PDF.

## Features

- Upload a PDF and extract its text.
- Split the PDF text into smaller chunks for efficient processing.
- Use Pinecone to store vector embeddings of the PDF text.
- Integrate with OpenAI embeddings to build a conversational retrieval chain.
- Ask questions based on the content of the uploaded PDF using a chatbot interface.
- Retain chat history during the interaction and allow clearing the history.
- Powered by OpenAI's `gpt-3.5-turbo` model for high-quality conversational responses.

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/indugapallignaneswara/Retrieval-Augmented-Generation-RAG-Model-for-QA-Bot.git
cd Retrieval-Augmented-Generation-RAG-Model-for-QA-Bot
```
### Install dependencies: It's recommended to use a virtual environment for the installation.

```bash
python3 -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
pip install -r requirements.txt 
```
### Set up environment variables:

- Create a .env file in the root of the project and add your API keys and index details:

```bash

OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
INDEX_NAME=your_pinecone_index_name
PINECONE_CLOUD=aws  # (or any other supported cloud provider)
PINECONE_REGION=us-east-1  # (or the region where your Pinecone project is hosted)
```
### Run the application:

```bash
streamlit run app.py
```
## Docker Usage
You can also run this project using Docker for easy setup and deployment.

- Build the Docker Image
First, make sure Docker is installed on your system. To build the Docker image, run the following command in the root of the project:

```bash

docker build -t pdf-qa-bot .
```
- Run the Docker Container
- After the image is built, you can run the container with:

```bash

docker run -p 8501:8501 pdf-qa-bot
```
### This will start the Streamlit application on http://localhost:8501.

## Environment Variables
- Ensure that you have the necessary environment variables (OPENAI_API_KEY, PINECONE_API_KEY, etc.) set. You can pass them to Docker as shown below:



1. **Upload a PDF:**
   - Upload a PDF document via the Streamlit interface.
   - The app will extract the text and process it into chunks for embedding.

2. **Ask Questions:**
   - Once the PDF is processed, you can ask questions related to the content of the document.
   - The chatbot will use the conversational retrieval chain to answer questions by retrieving the relevant chunks from Pinecone.

3. **View Chat History:**
   - The chat history is displayed so you can review previous questions and answers.
   - You can clear the chat history at any time using the "Clear Chat History" button.

## Project Structure

```bash
Retrieval-Augmented-Generation-RAG-Model-for-QA-Bot/
│
├── app.py                # Main application file for the Streamlit app
├── Dockerfile            # Dockerfile for containerizing the application
├── requirements.txt      # Python dependencies for the project
├── .env                  # Environment variables (add API keys here)
└── README.md             # Project documentation
```

## Dependencies

- **Streamlit**: A framework for building web applications quickly.
- **PyPDF2**: Library to read and extract text from PDFs.
- **LangChain**: For managing text chunking and retrieval operations.
- **Pinecone**: Vector database for storing document embeddings.
- **OpenAI**: Provides embeddings and conversational models.
- **dotenv**: To load environment variables from a `.env` file.

To install all dependencies, run:
```bash
pip install -r requirements.txt
```

## How It Works

1. **Text Extraction**: The application extracts the text from the uploaded PDF using `PyPDF2`.
2. **Text Splitting**: The text is split into smaller chunks using LangChain's `CharacterTextSplitter` for better processing and storage.
3. **Embeddings Creation**: Using OpenAI's API, each text chunk is converted into embeddings, which are stored in Pinecone.
4. **Conversational Chain**: The chatbot uses these embeddings and OpenAI's language models to answer questions by retrieving the relevant chunks from Pinecone.

## Environment Variables

Make sure to set the following environment variables in a `.env` file:

```bash
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
INDEX_NAME=your_pinecone_index_name
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1
```

## Contributing

Contributions are welcome! If you would like to contribute to the project, feel free to open a pull request or report issues.

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Pinecone](https://www.pinecone.io/)
- [OpenAI](https://openai.com/)
- [LangChain](https://github.com/hwchase17/langchain)

---

Happy coding!
