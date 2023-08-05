import re

from yelp_fetcher.scraper.bs4_util import get_element_by_classname

USER_URL = "https://www.yelp.com/user_details?userid={}"


def get_user_details_url(user_id):
    return USER_URL.format(user_id)


def get_user_name(page):
    return get_element_by_classname(page, "user-profile_info").h1.text


def get_user_city(page):
    return get_element_by_classname(page, "user-location").text


def get_user_review_count(page):
    text = get_element_by_classname(page, "review-count").text
    return re.search(r"([0-9]+)", text).group()
