from typing import Dict, List, Union

from ._connection import reddit_connection


def get_reddit_top_posts(
    subreddit: str,
    limit: int = 10,
) -> Dict[str, Union[List[int], List[str]]]:
    """
    Extracts top posts from Reddit's subreddit channel.

    Parameters
    ----------
    subreddit: str
        Subreddit channel name.

    limit: int, default 10
        Number of top posts to extract.

    Returns
    -------
    top_posts: Dict[str, Union[List[int], List[str]]]
        Top post high level information: title and number of comments.

    """
    title_list = list()
    volume_list = list()

    # Top posts in subreddit
    top_agg = reddit_connection.subreddit(subreddit).top(limit=limit)
    for post in top_agg:
        title_list.append(post.title)
        volume_list.append(post.num_comments)

    top_posts = {
        "titles": title_list,
        "num_comments": volume_list,
    }

    return top_posts
