import openai
import os
import sqlite3

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

class Agent:
    def __init__(self, db) -> None:
        self.connection = sqlite3.connect(db)
        self.cur = self.connection.cursor()
        self.ITER = 2

    def get_completion(self, prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0, # this is the degree of randomness of the model's output
        )
        return response.choices[0].message["content"]
    
    
    def generate_blog(self, prompt):
        print("Generating...")
        # Generate title
        title = self.get_completion(f"Give me a title for a blog article about: '{prompt}'")

        # Author name
        author = self.get_completion(f"Give me a random name of a tech blog author")

        # Generate content
        content = self.get_completion(f"You are a New York Times acclaimed writer and editor. You are an amazing writer. You avoid repetition and have a diverse vocabulary. Your writing is clear and descriptive. You write through example and stories. Knowing this, given the title: '{title}', generate me a well written blog post")

        return {"title": title, "author": author, "content": content}

    def commit_db(self, info):        
        self.cur.execute("INSERT INTO posts (title, content, author) VALUES (?, ?, ?)",
            (info['title'], info['content'], info['author'])
            )
        self.connection.commit()

    def run(self):
        idea = input("What blog to generate?: ")
        #idea = self.get_completion("Generate me an interesting blog idea")
        res = self.generate_blog(idea)
        revision = res['content']
        

        for i in range(self.ITER):
            print("ITER", i)
            feedback = self.get_completion(f"As a New York Times editor who is looking for the best hit articles for readers on a web blog, score the following article: '{revision}' in a combined score of 0 to 100, with 100 being the best. The score will account for readability, quality, and interesting article. Give constructive feedback.")
            revision = self.get_completion(f"Given the text: '{revision}' and the feedback: '{feedback}', rewrite the article accounting for the feedback to have a perfect 100 score in readability, quality, and interesting ideas")
            print(feedback)

        revision = revision.replace("\n", "<br/>")
        res['content'] = revision
        self.commit_db(res)

def main():
    a = Agent('database.db')
    a.run()

    

if __name__ == "__main__":
    main()