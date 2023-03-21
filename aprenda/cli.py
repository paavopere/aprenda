from aprenda import Chat, models, SYSTEM_PROMPT, EXAMPLES
import json


def print_message(message: dict):
    role = message['role']
    content = message['content']

    if role == 'user':
        print(f"{role}: {content}")

    if role == 'assistant':
        conts = json.loads(content)
        if 'correction' in conts:
            print(f"C   : {conts['correction']}")
        if 'spanish-translation' in conts:
            print(f"T   : {conts['spanish-translation']}")
        if 'response' in conts:
            print(f"\n{conts['response']}\n")



if __name__ == '__main__':
    chat = Chat(
        # model='gpt-4',  # we'll hit limits very fast if we use this
        system_prompt=SYSTEM_PROMPT,
        example_messages=EXAMPLES
    )

    print('Model:', chat.model)
    print('System prompt: ', chat.system_prompt)

    print('Examples:')
    for m in chat.example_messages:
        print_message(m)

    print('-- Chat starts here --')

    while True:
        user_message = input('user: ')
        response = chat.new_message(user_message)
        message = response['choices'][0]['message']
        print(f"({response['usage']['total_tokens']} tokens) {message['role']}: "
              f"{message['content']}")
