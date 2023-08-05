import requests
from yelp_fetcher.exceptions import FetchError, YelpRobotError
from yelp_fetcher.scraper.bs4_util import to_soup

ROBOT_ERROR_MESSAGE = (
    "Hey there! Before you continue, we just need to check that you're not a robot."
)


def fetch_html(url):
    response = requests.get(url)
    text = response.text
    if response.status_code != 200:
        raise FetchError(f"Fetch error for: {url}")
    elif ROBOT_ERROR_MESSAGE in text:
        raise YelpRobotError()
    return text


def fetch_soup(url):
    html = fetch_html(url)
    return to_soup(html)
