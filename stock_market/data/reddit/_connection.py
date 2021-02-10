import praw
import os
from dotenv import load_dotenv

load_dotenv()


# Load credentials to env
def load_reddit_credentials(
    client_id: str,
    client_secret: str,
    username: str,
    password: str,
    user_agent: str = "reddit app",
):
    os.environ["REDDIT_APP_NAME"] = user_agent
    os.environ["REDDIT_CLIENT_ID"] = client_id
    os.environ["REDDIT_CLIENT_SECRET"] = client_secret
    os.environ["REDDIT_USERNAME"] = username
    os.environ["REDDIT_PASSWORD"] = password

    print("Credentials loaded!")


def reddit_connection():

    return praw.Reddit(
        user_agent=os.getenv("REDDIT_APP_NAME", "reddit app"),
        client_id=os.getenv("REDDIT_CLIENT_ID", ""),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET", ""),
        username=os.getenv("REDDIT_USERNAME", ""),
        password=os.getenv("REDDIT_PASSWORD", ""),
    )
