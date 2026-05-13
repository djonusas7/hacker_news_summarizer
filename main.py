# Import libraries
import requests
from pprint import pprint

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

import yaml
import os

os.environ["USER_AGENT"] = "hn-article-summarizer/0.1"
from langchain_community.document_loaders import WebBaseLoader


# grab credentials and set up environment variables for API keys
print("#################################################")
print("### WELCOME TO HACKER NEWS ARTICLE SUMMARIZER ###")
print("#################################################\n")  

# Explain that the app will fetch the top 5 articles from Hacker News, summarize them using an LLM, and display the summaries in the terminal.
print("This application will fetch the top 5 articles from Hacker News, summarize them using an Open AI model, and display the summaries in the terminal.\n")
print("Top 5 articles at the moment are: \n")

# Web page loading

url = "https://hacker-news.firebaseio.com/v0/topstories.json"

# Create a document loader for the specified URL

response = requests.get(url)
stories = response.json()  # Convert the response to JSON format

top_candidate_stories = stories[:10]  # Get the top 10 stories


# loop through the top 10 stories and print their details
top_5_articles = []

for story_id in top_candidate_stories:
    if len(top_5_articles) <= 4:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        response = requests.get(story_url)
        story_json = response.json()
        # store each story's title and url in a list of dictionaries
        article = {
            "title": story_json.get("title"),
            "url": story_json.get("url")
        }
        #If no URL is provided, skip it.
        if article["url"] is None:
            continue
        #If URL contains "x.com" or "twitter.com", skip it.
        if "x.com" in article["url"] or "twitter.com" in article["url"]:
            continue
        
        top_5_articles.append(article)


final_list = []

[print(f"{index + 1}. {article['title']} - {article['url']}") for index, article in enumerate(top_5_articles)]

print("\nFind/Create your OpenAI API key at: https://platform.openai.com/account/api-keys.\n")
'''
ask user if they want to input their API key or if they want to use a saved key from credentials.yml file. If they choose to use the saved key, load it from the file and set it as an environment variable. If they choose to input a new key, ask them to input it and save it to the credentials.yml file for future use.
'''

use_saved_key = input("Do you want to use a saved API key from credentials.yml file? (yes/no): ").lower()
if use_saved_key == "yes" or use_saved_key == "y":
    key = yaml.safe_load(open('credentials.yml'))['openai']
else:
    key = input("Enter OpenAI API key and press Enter to continue to the LLM setup...\n")
# if key is not provided, ask the user to input it again until a valid key is provided
while not key:
    print("API key is required to continue.\n")
    key = input("Enter OpenAI API key and press Enter to continue to the LLM setup...\n")

# test the provided key by making a simple quick API call to OpenAI.
while True:
    try:
        test_model = ChatOpenAI(model="gpt-5.4-mini", api_key=key)
        test_model.invoke("Reply with only the word OK.")
        break
    except Exception as error:
        print("The provided API key is invalid or there was an error connecting to OpenAI. Please check your key and try again.\n")
        key = input("Enter OpenAI API key and press Enter to continue to the LLM setup...\n")
        while not key:
            print("API key is required to continue.\n")
            key = input("Enter OpenAI API key and press Enter to continue to the LLM setup...\n")

print("\nThank you! Setting up the environment and saving credentials for future use...")


for article in top_5_articles:
    try:
        loader = WebBaseLoader(article["url"])
        documents = loader.load()
        
        final_list.append({
            "title": article["title"],
            "url": article["url"],  
            "content": documents[0].page_content
        })
    except Exception as error:
        print(f"Could not load article: {article['title']}")
        print(f"URL: {article['url']}")
        print(f"“Could not load this page. It may block scrapers or require JavaScript.”")
        


# Use the provided API key to set up the environment variable and save to yaml file for future use
os.environ['OPENAI_API_KEY'] = key
with open('credentials.yml', 'w') as file:
    yaml.dump({'openai': key}, file)
        
# LLM model setup
llm_model = "gpt-5.4-mini"
os.environ['OPENAI_API_KEY'] = yaml.safe_load(open('credentials.yml'))['openai']

# prompt template

template = """
You are a helpful assistant that summarizes news articles.

Return the result using these sections:
- Main idea
- Key takeaways
- Why it matters
- Reading time saved

Keep the answer concise and useful.

{article_content}
"""


prompt = ChatPromptTemplate.from_template(template)

# LLM Spec
model = ChatOpenAI(
    model = llm_model,
    use_responses_api = True,
    reasoning = {"effort": "none"}
)   

agent = (prompt | model)

input("\nEnvironment setup complete! Press Enter to start summarizing the top articles from Hacker News...\n")

for i in final_list:
    # article number (1-5), title, url, and summary result from the agent
    print("#################################################")
    print(f"Article {final_list.index(i) + 1} of {len(final_list)}")
    print(f"Title: {i['title']}")
    print(f"URL: {i['url']}")
    result = agent.invoke({"article_content": i['content']})
    print("Summary:")
    print(result.text)
    print("#################################################")
    print("\n\n")
