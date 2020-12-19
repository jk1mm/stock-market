import bs4
import requests


# URL with IPO information (from MarketWatch)
IPO_URL = "https://www.marketwatch.com/tools/ipo-calendar"


class IPO:
    # Web Scraped data
    _data_ws = bs4.BeautifulSoup(requests.get(IPO_URL).content, "html.parser").find(
        "div", class_="element__body j-tabPanes"
    )

    # 4 resulting ipo data sets
    recent_ipo = None
    upcoming_ipo = None
    future_ipo = None
    withdrawn_ipo = None
