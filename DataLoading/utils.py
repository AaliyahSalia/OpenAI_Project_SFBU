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