import os
import openai
# import for pdf Loading
from langchain.document_loaders import PyPDFLoader
# imports for video loading
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
# import for url loading
from langchain.document_loaders import WebBaseLoader
# import for notion 
from langchain.document_loaders import NotionDirectoryLoader
# import for split PDF
from langchain.text_splitter import CharacterTextSplitter
#import for embedding
from langchain.embeddings.openai import OpenAIEmbeddings
#import for Vectorstores
from langchain.vectorstores import Chroma
#import for retrieve
from langchain.llms import OpenAI
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

# config api key
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

# Function to load PDF file
# pip install pypdf 
def loadPDF(path):
    loader = PyPDFLoader(path)
    pages = loader.load()
    return pages


# Function to load video
# pip install yt_dlp
# pip install pydub
def loadVideo(url):
    save_dir="docs/youtube/"
    loader = GenericLoader(
        YoutubeAudioLoader([url],save_dir),
        OpenAIWhisperParser()
    )
    docs = loader.load()
    return docs

# function to load url
def loadURL(url):
    loader = WebBaseLoader(url)
    docs = loader.load()
    return docs

# function to load notion
def loadNotion(path):
    loader = NotionDirectoryLoader(path)
    docs = loader.load()
    return docs

#Split Documents
def splitCharacterText(pages):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    return text_splitter.split_documents(pages)

# Embedding
def embeddingText():
    return OpenAIEmbeddings()

#In vectordtores
def saveVectorStores(path, splits):
    persist_directory = path
    vectordb = Chroma.from_documents(
    documents=splits,
    embedding=embeddingText(),
    persist_directory=persist_directory
    )
    return vectordb

#Search similarity
def similaritySearch(vectordb, question, k):
    docs = vectordb.similarity_search(query=question, k=k)
    return docs

def pretty_print_docs(docs):
    print(f"\n{'-' * 100}\n".join([f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]))

# Retrieve
def retrieve(vectordb, question):
    # Wrap our vectorstore
    llm = OpenAI(temperature=0)
    compressor = LLMChainExtractor.from_llm(llm)
    compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=vectordb.as_retriever(search_type = "mmr")
    )
    compressed_docs = compression_retriever.get_relevant_documents(question)
    return compressed_docs