import openai
import os

def callToOpenAI(userprompt):
    setOpenAiKey()
    prepromptresponse = collect_messages(userprompt, getContext('contextpreprompt.txt'))
    if "MISSING" in prepromptresponse or "missing" in prepromptresponse:
        return prepromptresponse

    return collect_messages(userprompt, getContext('contextprompt.txt'))

def get_completion_from_messages(messages, model="gpt-4", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def collect_messages(softwareprompt, userprompt):
    context = [{'role':'system', 'content': f"{softwareprompt}"}]
    context.append({'role':'user', 'content':f"{userprompt}"})
    response = get_completion_from_messages(context)
    return response

def setOpenAiKey():
    with open("chatgptapikey.env", "r") as f:
        secret = f.read()
    openai.api_key = secret.strip()

def getContext(filename):
    with open(filename, "r") as f:
        return f.read()
