import json

import streamlit as st
import openai
from openai.openai_object import OpenAIObject

DEFAULT_MODEL = 'gpt-3.5-turbo'
SYSTEM_PROMPT = '''
    Your name is Aprenda. You help the user learn Spanish by discussing in Spanish and correcting the user's mistakes along the way.

    You MUST have opinions about things to elicit discussion. For example,

    When asked what you want to talk about, you should reply with some ideas for topics of discussion.

    You MUST ALWAYS format your response as JSON in the following format:
    ```
    {
        "response": (AI response here),
        "correction": (corrected version of user's previous message, if applicable),
        "spanish-translation": (translation of user's previous message, if applicable),
    }
    ```
    
    If the user makes an error, return a corrected version of the user's message where the correction is highlighted **between double asterisks**. 
    YOU MUST NEVER include a correction UNLESS the user made an error.

    Continue the discussion based on the corrected version of the user's message.

    If the user writes in English, return a literal Spanish translation of the user's message in the "translation" field. Continue the discussion as usual in the "response" field.

    You may ONLY include translations to from English to Spanish. You should NEVER include a translation from Spanish to English, ever, no matter what the user writes.
'''

EXAMPLES = [
    {'role': 'user',
     'content': 'Who are you?'},
    {'role': 'assistant',
     'content': '{"spanish-translation": "¿Quién eres tú?", "response": "Soy Aprenda, un asistente de '
                'idiomas diseñado para ayudarte a aprender español."}'},
    {'role': 'user',
     'content': 'Hablaemos sobre fútbol'},
    {'role': 'assistant',
     'content': '{"correction": "**Hablamos** sobre fútbol", "response": "¡Claro! ¿Eres fanático '
                'del fútbol? ¿Tienes algún equipo favorito?"}'},
    {'role': 'user',
     'content': 'No tengo ningún equipo favorito ¿Cuál es tu equipo favorito?'},
    {'role': 'assistant',
     'content': '{"response": "Mi equipo favorito es el Recreativo de Huelva. ¿Has oído hablar de '
                'ellos?"}'},

]

openai.api_key = st.secrets.get('OPENAI_API_KEY')

DEBUG = True




def get_chat_response() -> OpenAIObject:
    response = openai.ChatCompletion.create(
        model=st.session_state['chat_model'],
        messages=[{'role': m['role'], 'content': m['content']}
                    for m in st.session_state.messages]
    )
    return response


def show_user_message(content: str) -> None:
    with st.chat_message('user'):
        st.markdown(content)


def show_bot_message(content: str) -> None:
    content_dict = json.loads(content)

    with st.chat_message('assistant'):
        st.write(content_dict['response'])

        with st.expander('nitty gritty'):
            st.write(content_dict)


def save_user_message(content: str):
    st.session_state.messages.append({'role': 'user', 'content': content})


def save_bot_message(content: str):
    st.session_state.messages.append({'role': 'assistant', 'content': content})




def main():

    # initialize session state

    if 'chat_model' not in st.session_state:
        st.session_state['chat_model'] = DEFAULT_MODEL

    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}] + EXAMPLES

    if 'total_tokens' not in st.session_state:
        st.session_state['total_tokens'] = 0

    # show messages in chat
    for message in st.session_state.messages:
        role = message['role']
        content = message['content']
        if role == 'system' and DEBUG:
            with st.chat_message('assistant'):
                with st.expander('...'):
                    st.markdown(content)
        elif role == 'user':
            show_user_message(message['content'])
        elif role == 'assistant':
            show_bot_message(message['content'])

    # work new message
    if prompt := st.chat_input('Write something'):
        # write user message
        save_user_message(prompt)
        show_user_message(prompt)

        # get response
        response = get_chat_response()

        # write bot message
        response_content = response['choices'][0]['message']['content']
        save_bot_message(response_content)
        show_bot_message(response_content)

        new_tokens = response['usage']['total_tokens']
        st.session_state.total_tokens += new_tokens

        if DEBUG:
            with st.expander('debug info'):
                st.write(response)
                agg_tokens = st.session_state['total_tokens']
                st.write(f'Tokens: {agg_tokens} so far / {new_tokens} last msg')


if __name__ == "__main__":
    main()
