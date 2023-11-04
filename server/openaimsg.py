def CallToOpenAI():
    with open("openai.env", "r") as f:
        secret = f.read()
    return "Proof of concept"