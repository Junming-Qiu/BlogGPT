import openai
import os
import sqlite3
import logging
import time
import requests

# Enable/disable logging
logging.basicConfig(level=logging.DEBUG)

# Get api keys
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

# logging.getLogger('openai').setLevel(logging.INFO)
# logging.getLogger('urllib3').setLevel(logging.INFO)

# Agent class generates blog articles and images
class Agent:
    # Get DB connections and set internal settings
    def __init__(self, db, identity) -> None:
        self.connection = sqlite3.connect(db)
        self.cur = self.connection.cursor()
        self.identity = identity
        self.ITER = 2

    # Generate low quality image
    def get_image(self, prompt):
        response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256",
        )

        return response['data'][0]['url']

    # Generate text completion (Add system prompt)
    def get_completion(self, prompt, temperature=0, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature, # this is the degree of randomness of the model's output
        )
        return response.choices[0].message["content"]
    
    # Generate title, author name, content, image
    def generate_blog(self):
        logger = logging.getLogger('Agent:generate_blog')
        logger.debug("Generating...")
        # Generate title
        title = self.get_completion(f"Generate me one random interesting blog title without {self.identity['negatives']}. Give only a title.", 1).strip("\"")
        logger.debug(f"Title: {title}")
        time.sleep(0.2)

        # Author name
        author = self.get_completion(f"Give me a random name of a blog author relating to the title: '{title}'. Do not include the title in the response", 0.8)
        logger.debug(f"Author: {author}")
        time.sleep(0.2)

        # Generate content
        content = self.get_completion(f"{self.identity['init']} Knowing this, given the title: '{title}', generate me a well written blog post.", 0.2)
        category = self.get_completion(f"What is the category of this blog post: '{content}'. Give me one category from the following: {self.identity['categories']}").strip("'\"")
        img_prompt = self.get_completion(f"Generate a realistic prompt for an image generation model based off the title: '{title}'. Use 200 characters maximum. Image does not include text")
        img_link = self.get_image(img_prompt)

        img_name = title.replace(' ', '_')
        img_data = requests.get(img_link).content

        dir_path = os.path.dirname(os.path.realpath(__file__))

        with open(f"{dir_path}/../web/static/media/{img_name}.jpg", "wb+") as f:
            f.write(img_data)

        img_path = f"/static/media/{img_name}.jpg"

        return {"title": title, "author": author, "content": content, "category": category, "img_path": img_path}

    # Commit all info to DB
    def commit_db(self, info):        
        self.cur.execute("INSERT INTO posts (title, content, author, category, img_path) VALUES (?, ?, ?, ?, ?)",
            (info['title'], info['content'], info['author'], info['category'], info['img_path'])
            )
        self.connection.commit()

    # Makes blog, then revises it, then commits
    def run(self):
        logger = logging.getLogger("Agent:run")    
        res = self.generate_blog()
        revision = res['content']

        for i in range(self.ITER):
            logger.debug(f"ITER: {i}")
            time.sleep(0.2)

            feedback = self.get_completion(f"{self.identity['eval']} Give constructive feedback. Article: '{revision}'")
            time.sleep(0.2)
            revision = self.get_completion(f"Given the text: '{revision}' and the feedback: '{feedback}', revise the article. Only give the revision. Do not include the feedback or disclaimers in the response")
            logger.debug(feedback)

        revision = revision.replace("\n", "<br/>")
        res['content'] = revision
        self.commit_db(res)
        logger.debug('Committing to DB')

# Grab GPT prompts
def main():
    identity = {}
    path = f"{os.path.dirname(__file__)}/identity"

    with open(f'{path}/init.txt', 'r') as f:
        identity['init'] = f.read()

    with open(f'{path}/negatives.txt', 'r') as f:
        identity['negatives'] = f.read()

    with open(f'{path}/eval.txt', 'r') as f:
        identity['eval'] = f.read()

    with open(f'{path}/categories.txt') as f:
        identity['categories'] = f.read()

    a = Agent('database.db', identity)
    a.run()
 

if __name__ == "__main__":
    main()