from flask import Flask, render_template, request, redirect, url_for
from utils import get_completion_from_messages

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    response = ""
    if request.method == 'POST':
        user_input = request.form['user_input']
        # For this example, I'll use a single message from the user. 
        # You can adjust it according to your needs.
        messages = [{"role": "user", "content": user_input}]
        response = get_completion_from_messages(messages)

    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
