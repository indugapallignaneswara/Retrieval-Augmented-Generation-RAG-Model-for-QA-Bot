# import os
# from dotenv import load_dotenv
# from langchain_openai import OpenAIEmbeddings
# from langchain.chains import RetrievalQA
# from langchain_community.chat_models import ChatOpenAI
# from langchain_pinecone import PineconeVectorStore

# embeddings = OpenAIEmbeddings()
# vectorstore = PineconeVectorStore(
#         index_name=os.environ["INDEX_NAME"], embedding=embeddings
# )

# chat = ChatOpenAI(verbose=True, temperature=0, model_name="gpt-3.5-turbo")

# qa = RetrievalQA.from_chain_type(
#     llm=chat, chain_type="stuff", retriever=vectorstore.as_retriever()
# )    

# res = qa.invoke(" How do Transformers differ from RNNs or LSTMs?")
# print(res) 

# res = qa.invoke("who is Gnaneswara?")
# print(res)

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from langchain_pinecone import PineconeVectorStore

try:
    # Load environment variables
    load_dotenv()

    embeddings = OpenAIEmbeddings()
    vectorstore = PineconeVectorStore(
        index_name=os.environ.get("INDEX_NAME", ""), embedding=embeddings
    )

    chat = ChatOpenAI(verbose=True, temperature=0, model_name="gpt-3.5-turbo")

    qa = RetrievalQA.from_chain_type(
        llm=chat, chain_type="stuff", retriever=vectorstore.as_retriever()
    )

    # Test the first question
    res1 = qa.invoke("How do Transformers differ from RNNs or LSTMs?")
    print("Response 1: ", res1)

    # Test the second question
    res2 = qa.invoke("What is Response 1?")
    print("Response 2: ", res2)
except Exception as e:
    print(f"An error occurred: {e}")
