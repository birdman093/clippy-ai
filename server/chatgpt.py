import openai
import os

def callToOpenAI(userprompt):
    setOpenAiKey()
    return test(userprompt)

def test(userprompt: str):
    return collect_messages(userprompt)

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def collect_messages(userprompt):
    context = [{'role':'system', 'content':getSoftwarePrompt()}]
    context.append({'role':'user', 'content':f"{userprompt}"})
    response = get_completion_from_messages(context)
    return response

def setOpenAiKey():
    with open("chatgptapikey.env", "r") as f:
        secret = f.read()
    openai.api_key  = secret.strip()

def getSoftwarePrompt():
    with open("contextprompt.txt", "r") as f:
        return f.read()
