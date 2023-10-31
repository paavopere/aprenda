# Aprenda

Work in progress: A GPT chatbot to help an English speaker learn Spanish.

Dev setup:

```
git clone git@github.com:paavopere/aprenda.git
cd aprenda
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a secrets file and add an OpenAI API key there:

```
mkdir .streamlit
echo 'OPENAI_API_KEY = "<insert your key here>"' > .streamlit/secrets
```

Run:

```
streamlit run aprenda/streamlit_app.py
```

Example (in a future version, the translations and corrections will be lifted out from the debug info output):

![image](https://github.com/paavopere/aprenda/assets/2135878/718ccf6b-0894-416d-8bea-a3fa8e97cf90)

