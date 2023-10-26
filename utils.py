import os
from dotenv import load_dotenv, find_dotenv
import openai
_ = load_dotenv(find_dotenv()) # read local .env file

def get_OpenAI_API_Key():
    return os.getenv("OPENAI_API_KEY")

# General function to get response with gpt-3.5
def get_completion_from_messages(messages, 
                                 model="gpt-3.5-turbo", 
                                 temperature=0, 
                                 max_tokens=1000):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
    )
    return response.choices[0].message["content"]