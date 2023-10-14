import utils

# # Load SFBU Catalog
# pdfPath="/home/sharoncao0802/CS589_Projects/SFBU_OpenAI_Project/DataLoading/pdfFiles/2023Catalog.pdf"

# pages = utils.loadPDF(pdfPath)

# print("Number of pages: ",len(pages))
# page = pages[0]

# print("First 500 lines: ", page.page_content[0:500])
# print("Metadata of page: ",page.metadata)

# # Load SFBU Student Video
# url="https://www.youtube.com/watch?v=kuZNIvdwnMc"
# docs=utils.loadVideo(url)
# print(docs[0].page_content[0:500])

# # Load SFBU Insurance URL
# url="https://www.sfbu.edu/admissions/student-health-insurance"
# docs=utils.loadURL(url)
# print(docs[0].page_content[0:500])

# Load SFBU Insurance URL
path="/home/sharoncao0802/CS589_Projects/SFBU_OpenAI_Project/DataLoading/docs/NotionDB"
docs=utils.loadNotion(path)
print(docs[0].page_content[0:100])
print(docs[0].metadata)