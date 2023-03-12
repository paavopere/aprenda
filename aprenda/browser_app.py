from copy import deepcopy
import mistune
from flask import Flask, render_template
from aprenda import chat


app = Flask(__name__)


@app.route('/')
def hello():
    chat.new_message('¿Sobre qué te gustaría hablar?')
    messages: list = deepcopy(chat.messages)
    for msg in messages:
        msg['content-html'] = mistune.html(msg['content'])
        print(msg)

    return render_template('template.html.jinja2', messages=messages)
