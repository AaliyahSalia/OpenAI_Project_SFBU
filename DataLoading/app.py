import utils

# Load SFBU Catalog
pdfPath="/home/sharoncao0802/CS589_Projects/SFBU_Main/SFBU_OpenAI_Project/DataLoading/pdfFiles/2023Catalog.pdf"

pages = utils.loadPDF(pdfPath)
llm_name = "gpt-3.5-turbo"

#split document
docs = utils.splitCharacterText(pages)

# indexing and Save in vectorstores
path = "docs/chroma"
vectordb = utils.saveVectorStores(path,docs)

# print(vectordb._collection.count())

# chat OpenAI
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(model_name=llm_name, temperature=0)
# print(llm.predict("Hello world!"))


from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

from langchain.chains import ConversationalRetrievalChain
retriever=vectordb.as_retriever()
qa = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=retriever,
    memory=memory,
)

question = "Is there scholarship offered by SFBU?"
result = qa({"question": question})
print(question)
print(result['answer'])

question = "What are the due date for application?"
result = qa({"question": question})
print(question)
print(result['answer'])

question = " What's the amount?"
result = qa({"question": question})
print(question)
print(result['answer'])

# # Similarity search
# question = "Is there scholarship availiable and requirements?"
# similarDoc = utils.similaritySearch(vectordb, question, 2)
# print("Similarity search result 1: \n", similarDoc[0])
# print("Similarity search result 2: \n", similarDoc[1])

# # Retreiver Combining various techniques
# compressed_doc = utils.retrieve(vectordb, question)
# utils.pretty_print_docs(compressed_doc)

# # Load SFBU Student Video
# url="https://www.youtube.com/watch?v=kuZNIvdwnMc"
# docs=utils.loadVideo(url)
# print(docs[0].page_content[0:500])

# # Load SFBU Insurance URL
# url="https://www.sfbu.edu/admissions/student-health-insurance"
# docs=utils.loadURL(url)
# print(docs[0].page_content[0:500])

# # Load SFBU Insurance URL
# path="/home/sharoncao0802/CS589_Projects/SFBU_OpenAI_Project/DataLoading/docs/NotionDB"
# docs=utils.loadNotion(path)
# print(docs[0].page_content[0:100])
# print(docs[0].metadata)