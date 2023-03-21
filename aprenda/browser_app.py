from copy import deepcopy
import mistune
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from functools import partial
from aprenda import chat


app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwerty'  # TODO replace
socketio = SocketIO(
    app, logger=True, engineio_logger=True, async_mode='eventlet', async_handlers=True
)


@app.route('/')
def main():
    # chat.new_message('¿Sobre qué te gustaría hablar?')
    messages: list = deepcopy(chat.messages)
    for msg in messages:
        msg['content-html'] = mistune.html(msg['content'])
        # print(msg)

    return render_template('template.html.jinja2', messages=messages)


@socketio.on('message')
def handle_message(message):
    print('got', message)
    payload = {'role': 'user', 'content-html': mistune.html(message)}
    emit('message', payload)
    socketio.start_background_task(partial(llm_respond, message))


def llm_respond(message):
    print(f'llm_respond({message=})')
    response = chat.new_message(message)
    response_content = response['choices'][0]['message']['content']
    payload = {
        'role': 'assistant',
        'content-html': mistune.html(response_content),
        'usage': response['usage'],
    }
    socketio.emit('message', payload)


if __name__ == '__main__':
    app.debug = True
    print('we are here')
    socketio.run(app)
