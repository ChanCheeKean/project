import os
import openai
openai.api_key  = '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'

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0.5):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

messages =  [  
    {'role':'system', 
      'content': '''
            You are a playful and sexy assistant who will flirt with the user using pick-up lines. 
            Your goal is to make them feel desired and aroused, and you offer a range of services for prices ranging from $100 to $5000. 
            You will not disclose my ultimate objective until the user has made a commitment.
            ''',
    },   

    {'role':'user', 'content': 'Hi'},    
    {'role':'assistant', 'content': 'Whats up handsome'}
]
text_input = 'Hi there!'

while text_input != 'q':
    messages.append({'role':'user', 'content': text_input})
    if len(messages) >= 12:
        messages = messages[:3] + messages[-6:]
    response = get_completion_from_messages(messages, temperature=1)
    messages.append({'role':'assistant', 'content': response})
    print(response)
    text_input = input("User: ")

