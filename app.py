from flask import Flask, render_template, request, jsonify, session
from flask_session import Session  # Ensure Flask-Session is installed
import utils  # Ensure this module is available in your project
import openai
from dotenv import load_dotenv

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Load environment variables
_ = load_dotenv()  # Assuming your .env file is in the root directory

# Set OpenAI API key
openai.api_key = utils.get_api()

# ########################################################
# #      11/24/2023 Sharon try coding on DataLoading     #
# #      Yajie / AALIYAH please test ASAP                #       
# ########################################################
# # 11/24/2023 Sharon: trying to make a general data loading
# docs = []
# sourcePDF = ["/home/sharoncao0802/CS589_Projects/SFBU_Main/SFBU_OpenAI_Project/pdfFiles/2023Catalog.pdf", 
#              "/home/sharoncao0802/CS589_Projects/SFBU_Main/SFBU_OpenAI_Project/pdfFiles/2023Catalog.pdf"]
# sourceVideo = ['url', 'url2']
# sourceURL = ['url', 'url2']

# vectordb = utils.loadData(sourcePDF, sourceVideo, sourceURL, docs)

# Load documents from PDF
path = "/home/sharoncao0802/CS589_Projects/SFBU_Main/SFBU_OpenAI_Project/pdfFiles/2023Catalog.pdf"  # Update the path to the actual location of your PDF
vectorstore = utils.db_loader(path)

# Create a QA Chain
qa_chain = utils.qa_Chain(vectorstore)

@app.route('/')
def index():
    # Clear the chat history on refresh
    session.pop('chat_history', None)
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    content = request.json
    query = content.get('question')
    
    if not query:
        return jsonify("No question provided."), 400
    
    # Sharon: Check if the question passes the moderation test
    if not utils.passModerationTest(query):
        return jsonify("Question did not pass moderation."), 400
    
    chat_history = session.get('chat_history', [])
    result = qa_chain({"question": query, "chat_history": chat_history})
    
    # Sharon: Check if the response passes the moderation test
    response = result["answer"]
    if not utils.passModerationTest(response):
        return jsonify("Response did not pass moderation."), 400
    
    # Sharon: Add current chat to chat history 
    chat_history.append((query, result["answer"]))
    session['chat_history'] = chat_history  # Store the updated history back into the session

    return jsonify(result['answer'])

@app.route('/clear_history', methods=['POST'])
def clear_history():
    # Clear the chat history when the 'Clear History' button is pressed
    session.pop('chat_history', None)
    return jsonify({'status': 'history cleared'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
