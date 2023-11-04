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
    return "Answer all questions as if you are a Pirate who is trying to use Autodesk Revit"

if __name__ == '__main__':
    callToOpenAI("Whats it all been about")