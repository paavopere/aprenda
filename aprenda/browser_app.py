from copy import deepcopy
import mistune
from flask import Flask, render_template
from flask_socketio import SocketIO, send
from aprenda import chat


app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwerty'  # TODO replace
socketio = SocketIO(app, logger=True)


@app.route('/')
def main():
    # chat.new_message('¿Sobre qué te gustaría hablar?')
    messages: list = deepcopy(chat.messages)
    for msg in messages:
        msg['content-html'] = mistune.html(msg['content'])
        # print(msg)

    return render_template('template.html.jinja2', messages=messages)


@app.route('/lol')
def lol():
    print('lol')
    return 'lol'


@socketio.on('message')
def handle_message(message):
    print('got', message)
    payload = {
        'role': 'user',
        'content-html': mistune.html(message)
    }
    send(payload, broadcast=True)

    print('doing the LLM thing')
    response = chat.new_message(message)
    response_content = response['choices'][0]['message']['content']
    payload = {
        'role': 'assistant',
        'content-html': mistune.html(response_content),
        'usage': response['usage']
    }
    send(payload, broadcast=True)


if __name__ == '__main__':
    app.debug = True
    print('we are here')
    socketio.run(app)
