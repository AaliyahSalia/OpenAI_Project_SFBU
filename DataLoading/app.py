import utils

# Load SFBU Catalog
pdfPath="/home/sharoncao0802/CS589_Projects/SFBU_Main/SFBU_OpenAI_Project/DataLoading/pdfFiles/2023Catalog.pdf"

pages = utils.loadPDF(pdfPath)

print("Number of pages: ",len(pages))
page = pages[0]

print("First 500 lines: ", page.page_content[0:500])
print("Metadata of page: ",page.metadata)

#split document
docs = utils.splitCharacterText(pages)
print("length for pages: ", len(pages))
print("length for split docs: ", len(docs))

# indexing and Save in vectorstores
path = "docs/chroma"
vectordb = utils.saveVectorStores(path,docs)

print(vectordb._collection.count())

# Similarity search
question = "Is there scholarship availiable and requirements?"
similarDoc = utils.similaritySearch(vectordb, question, 2)
print("Similarity search result 1: \n", similarDoc[0])
print("Similarity search result 2: \n", similarDoc[1])

# Retreiver Combining various techniques
compressed_doc = utils.retrieve(vectordb, question)
utils.pretty_print_docs(compressed_doc)

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