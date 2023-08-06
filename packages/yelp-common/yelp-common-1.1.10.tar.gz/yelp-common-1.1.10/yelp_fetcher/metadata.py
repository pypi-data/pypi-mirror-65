from typing import TypedDict

from yelp_fetcher._util import fetch_soup
from yelp_fetcher.scraper.user_details import (
    get_user_city,
    get_user_details_url,
    get_user_name,
    get_user_review_count,
)


class Metadata(TypedDict):
    user_id: str
    name: str
    city: str
    review_count: str


def fetch_metadata(user_id: str) -> Metadata:
    url = get_user_details_url(user_id)
    user_soup = fetch_soup(url)
    return Metadata(
        user_id=user_id,
        name=get_user_name(user_soup),
        city=get_user_city(user_soup),
        review_count=get_user_review_count(user_soup),
    )
