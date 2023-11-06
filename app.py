# from flask import Flask, render_template, request, jsonify, session
# from flask_session import Session  # Ensure Flask-Session is installed
# import utils  # Ensure this module is available in your project
# import openai
# from dotenv import load_dotenv

# app = Flask(__name__)

# # Configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# # Load environment variables
# _ = load_dotenv()  # Assuming your .env file is in the root directory

# # Set OpenAI API key
# openai.api_key = utils.get_api()

# # Load documents from PDF
# path = "/home/sharoncao0802/CS589_Projects/CreateChatBot/pdfFiles/2023Catalog.pdf"  # Update the path to the actual location of your PDF
# vectorstore = utils.db_loader(path)

# # Create a QA Chain
# qa_chain = utils.qa_Chain(vectorstore)

# @app.route('/')
# def index():
#     if 'chat_history' not in session:
#         session['chat_history'] = []
#     return render_template('index.html', chat_history=session['chat_history'])

# @app.route('/ask', methods=['POST'])
# def ask():
#     content = request.json
#     query = content.get('question')

#     if not query:
#         return jsonify("No question provided."), 400

#     chat_history = session.get('chat_history', [])
#     result = qa_chain({"question": query, "chat_history": chat_history})
#     chat_history.append((query, result["answer"]))
#     session['chat_history'] = chat_history  # Store the updated history back into the session

#     return jsonify(result['answer'])

# if __name__ == '__main__':
#     app.run(debug=True)

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

    chat_history = session.get('chat_history', [])
    result = qa_chain({"question": query, "chat_history": chat_history})
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
