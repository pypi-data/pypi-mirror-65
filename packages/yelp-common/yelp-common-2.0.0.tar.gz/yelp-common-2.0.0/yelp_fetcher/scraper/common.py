import re

from yelp_fetcher.scraper.bs4_util import (
    get_element_by_classname,
    get_elements_by_classname,
)


def get_review_ids(page):
    review_ids = map(
        lambda r: r["data-review-id"], get_elements_by_classname(page, "review")
    )
    return list(review_ids)


def get_num_pages(page):
    page_of_pages_element = get_element_by_classname(page, "page-of-pages")
    if page_of_pages_element is None:
        return 0
    matches = re.search(r"Page ([0-9]+) of ([0-9]+)", page_of_pages_element.get_text())
    curr_page, max_pages = matches.groups()
    return int(max_pages)
