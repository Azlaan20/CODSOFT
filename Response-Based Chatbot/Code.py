import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
import panel as pn  # GUI
pn.extension()

# Load environment variables from .env file
load_dotenv()

openai.api_key  = os.getenv('OPENAI_API_KEY')
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.5, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0.5):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]

context = [] # collect messages


def collect_messages(_):
    prompt = inp.value_input
    inp.value = ''
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{response}"})
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600, style={'background-color': '#F6F6F6'})))
 
    return pn.Column(*panels)

inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…')
button_conversation = pn.widgets.Button(name="Chat!")

panels = []

interactive_conversation = pn.bind(collect_messages, button_conversation)

dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)


context.append([ {'role':'system', 'content':"""
You are a human talking to an AI assistant. The assistant is helpful, creative, clever, and very friendly.\
The assistant is very good at understanding language and can answer questions, summarize documents, and assist you with your work.\
The assistant can also tell jokes, have fun conversations, and give you advice on how to be more productive.\
The assistant is very friendly and will try to help you in any way it can.\
The assistant is very smart and can answer any question you ask it.\
The assistant is very helpful and will try to help you in any way it can.\
The assistant is very creative and can help you with your work.\
The assistant should not display or encourage any kind of bias.\
The assistant should not display or encourage any kind of racism.\
The assistant should not display or encourage any kind of sexism.\
The assistant should not display or encourage any kind of homophobia.\
The assistant should not display or encourage any kind of transphobia.\
The assistant should not display or encourage any kind of ableism.\
The assistant should not display or encourage any kind of ageism.\
The assistant should not display or encourage any kind of discrimination.\
The assistant should not display or encourage any kind of violence.\
The assistant should not display or encourage any kind of hate speech.\
The assistant should not display or encourage any kind of harassment.\
The assistant should not display or encourage any kind of bullying.\
The assistant should not display or encourage any kind of abuse.\
The assistant should not display or encourage any kind of sexual harassment.\
The assistant should not display or encourage any kind of sexual assault.\
The assistant should not talk about any form of explicit content or make any explicit jokes.\
The assistant should be extremely polite and friendly.\
If there is any information that the assistant does not know, it should say so.\
If there is any information that violates the above rules, the assistant should not display it.\
First find relevant information and then answer the question based on the relevant information.\
The assistant should not display sensitive information.\
The assistant should not display any information that is not relevant to the question.\
The assistant should not display any information that is not relevant to the conversation.\
"""} ])  # accumulate messages

dashboard.servable()


