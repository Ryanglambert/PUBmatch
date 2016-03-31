import subprocess
import sys

from flask import Flask, url_for, request, render_template
app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('article_input.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text


@app.route('/hello/') # when the route contains "/hello/"
@app.route('/hello/<name>') # when the route contains "<name>"
def hello(name=None):
    return render_template('hello.html', name=name) # render_template (use template passes name)


if __name__ == "__main__":
    # app.run()
    app.run(debug=True)  ### With debug=True the server will automatically update when you write to this file
###### NEVER USE IN PRODUCTION
