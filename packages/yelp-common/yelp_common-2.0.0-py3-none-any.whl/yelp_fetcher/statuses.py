from enum import Enum
from typing import TypedDict

from yelp_fetcher._util import FetchError, fetch_html
from yelp_fetcher.scraper.biz import get_biz_review_url, review_id_on_page


class Status(Enum):
    ALIVE = "ALIVE"
    DEAD = "DEAD"
    UNKNOWN = "UNKNOWN"


class ReviewStatus(TypedDict):
    user_id: str
    biz_id: str
    review_id: str
    status: str


def fetch_status(user_id, biz_id, review_id):
    url = get_biz_review_url(biz_id, review_id)
    try:
        html = fetch_html(url)
        status = Status.ALIVE if review_id_on_page(html, review_id) else Status.DEAD
    except FetchError:
        status = Status.UNKNOWN

    return ReviewStatus(user_id=user_id, biz_id=biz_id, review_id=review_id, status=status.value)
