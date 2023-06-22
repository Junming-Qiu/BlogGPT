import openai
import os
import sqlite3
import logging
import time
import requests

logging.basicConfig(level=logging.DEBUG)

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

# logging.getLogger('openai').setLevel(logging.INFO)
# logging.getLogger('urllib3').setLevel(logging.INFO)

class Agent:
    def __init__(self, db, identity) -> None:
        self.connection = sqlite3.connect(db)
        self.cur = self.connection.cursor()
        self.identity = identity
        self.ITER = 2

    def get_image(self, prompt):
        response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256",
        )

        return response['data'][0]['url']

    def get_completion(self, prompt, temperature=0, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature, # this is the degree of randomness of the model's output
        )
        return response.choices[0].message["content"]
    
    
    def generate_blog(self):
        logger = logging.getLogger('Agent:generate_blog')
        logger.debug("Generating...")
        # Generate title
        title = self.get_completion(f"Generate me one random interesting blog title without {self.identity['negatives']}. Give only a title.", 1).strip("\"")
        logger.debug(f"Title: {title}")
        time.sleep(0.2)

        # Author name
        author = self.get_completion(f"Give me a random name of a blog author relating to the title: '{title}'", 0.8)
        logger.debug(f"Author: {author}")
        time.sleep(0.2)
        # Generate content
        content = self.get_completion(f"{self.identity['init']} Knowing this, given the title: '{title}', generate me a well written blog post.", 0.2)
        category = self.get_completion(f"What is the category of this blog post: '{content}'. Give me one category only delimited in single tick quotations.").strip("'\"")
        img_prompt = self.get_completion(f"Generate a realistic prompt for an image generation model based off the title: '{title}'. Use 250 characters maximum")
        img_link = self.get_image(img_prompt)

        img_data = requests.get(img_link).content
        with open(f"../web/static/media/{title}.jpg", "wb+") as f:
            f.write(img_data)

        return {"title": title, "author": author, "content": content, "category": category}

    def commit_db(self, info):        
        self.cur.execute("INSERT INTO posts (title, content, author, category) VALUES (?, ?, ?, ?)",
            (info['title'], info['content'], info['author'], info['category'])
            )
        self.connection.commit()

    def run(self):
        logger = logging.getLogger("Agent:run")    
        res = self.generate_blog()
        revision = res['content']

        for i in range(self.ITER):
            logger.debug(f"ITER: {i}")
            time.sleep(0.2)

            feedback = self.get_completion(f"{self.identity['eval']} Give constructive feedback. Article: '{revision}'")
            time.sleep(0.2)
            revision = self.get_completion(f"Given the text: '{revision}' and the feedback: '{feedback}', revise the article.")
            logger.debug(feedback)

        revision = revision.replace("\n", "<br/>")
        res['content'] = revision
        self.commit_db(res)
        logger.debug('Committing to DB')

def main():
    identity = {}
    with open(f'{os.path.dirname(__file__)}/identity/init.txt', 'r') as f:
        identity['init'] = f.read()

    with open(f'{os.path.dirname(__file__)}/identity/negatives.txt', 'r') as f:
        identity['negatives'] = f.read()

    with open(f'{os.path.dirname(__file__)}/identity/eval.txt', 'r') as f:
        identity['eval'] = f.read()

    a = Agent('database.db', identity)
    a.run()
 

if __name__ == "__main__":
    main()