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
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.chains import  ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
# config api key
from dotenv import load_dotenv, find_dotenv
llm_name = "gpt-3.5-turbo"

def get_api():
    _ = load_dotenv(find_dotenv()) # read local .env file
    return os.environ['OPENAI_API_KEY']

def passModerationTest(message):
    response = openai.Moderation.create(
        model="text-moderation-latest",
        input=message)
    moderation_output = response["results"][0]
    # print(moderation_output)
    if moderation_output["flagged"] != False: # flagged = true -> not pass
        return False
    else:
        return True


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
def saveVectorStores(splits):
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embeddingText(),
    )
    return vectordb

#Search similarity
def similaritySearch(vectordb, question, k):
    docs = vectordb.similarity_search(query=question, k=k)
    return docs

# def pretty_print_docs(docs):
#     response = "\n{'-' * 100}\n".join([f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)])
#     return response

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

def answerWithBuildPrompt(vectordb, template, question):
    llm=ChatOpenAI(model_name=llm_name, temperature=0)
    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template,)
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    qa = ConversationalRetrievalChain.from_llm(llm,
                                       retriever=vectordb.as_retriever(),
                                       return_source_documents=True,
                                       memory=memory,
                                       chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
    result = qa({"question": question})
    return result['answer']

def db_loader(pdfPath):
    pages = loadPDF(pdfPath)

    #split document
    docs = splitCharacterText(pages)

    # indexing and Save in vectorstores
    vectordb = saveVectorStores(docs)
    return vectordb

def qa_Chain(vectorstore):
    return ConversationalRetrievalChain.from_llm(OpenAI(temperature=0), vectorstore.as_retriever())

# ########################################################
# #      11/24/2023 Sharon try coding on DataLoading     #
# #      Yajie / AALIYAH please test ASAP                #       
# ########################################################
# # Sharon: General function to load PDF
# def loadPDF(path, docs):
#     loader = PyPDFLoader(path)
#     docs.extend(loader.load())
#     return docs

# # Sharon: General function to load Video
# def loadVideo(url, docs):
#     save_dir="docs/youtube/"
#     loader = GenericLoader(
#         YoutubeAudioLoader([url],save_dir),
#         OpenAIWhisperParser()
#     )
#     docs.extend(loader.load())
#     return docs

# # Sharon: General function to load URL
# def loadURL(url, docs):
#     loader = WebBaseLoader(url)
#     docs.extend(loader.load())
#     return docs

# # Sharon: General function to load data and return vectordb
# def loadData(sourcePDF, sourceVideo, sourceURL, docs):
#     if sourcePDF:
#         for source in sourcePDF:
#             docs = loadPDF(source, docs)

#     if sourceVideo:
#         for source in sourceVideo:
#             docs = loadVideo(source, docs)

#     if sourceURL:
#         for source in sourceURL:
#             docs = loadURL(source, docs)
    
#     splits = splitCharacterText(docs)
#     # indexing and Save in vectorstores
#     vectordb = saveVectorStores(splits)
#     return vectordb


