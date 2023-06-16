import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')
print(os.getenv('OPENAI_API_KEY'))

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def listener():
    query = ""
    while query != "STOP":
        query = input("Enter ChatGPT Query: ")
        response = get_completion(query)
        print(response)


def main():
    listener()

if __name__ == "__main__":
    main()