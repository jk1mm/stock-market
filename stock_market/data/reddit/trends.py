from typing import Dict, List, Union

from prawcore import NotFound

from stock_market.data.reddit._connection import reddit_connection

TIME_FILTERS = ["all", "day", "hour", "month", "week", "year"]


def get_reddit_top_posts(
    subreddit: str,
    num_post: int = 10,
    time_period: str = "day",
) -> Dict[str, Union[List[int], List[str]]]:
    """
    Extracts top posts from Reddit's subreddit channel.

    Parameters
    ----------
    subreddit: str
        Subreddit channel name.

    num_post: int, default 10
        Number of top posts to extract.

    time_period: str, default "day"
        Time period of the top posts.

    Returns
    -------
    top_posts: Dict[str, Union[List[int], List[str]]]
        Top post high level information: title and number of comments.

    """
    time_period = time_period.lower()
    if time_period not in TIME_FILTERS:
        raise Warning(
            f"Time period must be one of the following options: {TIME_FILTERS}"
        )

    title_list = list()
    volume_list = list()

    # Check if subreddit exists
    try:
        # Top posts in subreddit
        top_agg = reddit_connection.subreddits.search_by_name(subreddit, exact=True)[
            0
        ].top(limit=num_post, time_filter=time_period)
    except NotFound:
        raise Warning("Specified subreddit does not exist.")

    for post in top_agg:
        title_list.append(post.title)
        volume_list.append(post.num_comments)

    top_posts = {
        "titles": title_list,
        "num_comments": volume_list,
    }

    return top_posts
