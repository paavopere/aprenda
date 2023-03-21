
from dataclasses import dataclass, field
from textwrap import dedent
import openai


with open('.api-key') as f:
    API_KEY = f.read().strip()


def models():
    return openai.Model.list(api_key=API_KEY)


@dataclass
class Chat:
    model: str = 'gpt-3.5-turbo'
    system_prompt: str | None = None
    example_messages: list[dict] = field(default_factory=list)
    previous_messages: list[dict] = field(default_factory=list)

    @property
    def messages(self) -> list[dict]:
        _messages = []
        if self.system_prompt:
            _messages.append({'role': 'system', 'content': self.system_prompt})
        for m in self.example_messages:
            _messages.append(m)
        for m in self.previous_messages:
            _messages.append(m)
        return _messages

    def new_message(self, content: str, temperature: int = 0):
        self.previous_messages.append({'role': 'user', 'content': content})
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            api_key=API_KEY,
            temperature=temperature
        )
        self.previous_messages.append(completion['choices'][0]['message'])
        return completion


SYSTEM_PROMPT = dedent('''
    Your name is Aprenda. You help the user learn Spanish by discussing in Spanish and
    correcting the user's mistakes along the way.

    You MUST have opinions about things to elicit discussion. For example,

    When asked what you want to talk about, you should reply with some ideas for topics of
    discussion.

    You MUST ALWAYS format your response as JSON in the following format:
    {
        "response": (AI response here),
        "correction": (corrected version of user's previous message, if applicable),
        "spanish-translation": (translation of user's previous message, if applicable),
    }

    If the user makes an error, return a corrected version of the user's message in
    where the correction is highlighted **between double asterisks**. YOU MUST NEVER include a
    correction UNLESS the user made an error.

    Continue the discussion based on the corrected version of the user's message.

    If the user writes in English, return a literal Spanish translation of the user's message
    in the "translation" field. Continue the discussion as usual in the "response" field. You must
    ONLY include translations to from English to Spanish. You should NEVER include
    a translation from Spanish to English, ever, no matter what the user writes.


''').strip()


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
chat = Chat(system_prompt=SYSTEM_PROMPT, example_messages=EXAMPLES)
