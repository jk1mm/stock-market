import praw
import os
from dotenv import load_dotenv

load_dotenv()


reddit_connection = praw.Reddit(
    user_agent=os.getenv("REDDIT_APP_NAME", "reddit app"),
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
)
