from typing import TypedDict

from yelp_fetcher._util import fetch_html
from yelp_fetcher.scraper.biz import get_biz_review_url, review_id_on_page


class ReviewStatus(TypedDict):
    user_id: str
    biz_id: str
    review_id: str
    is_alive: str


def fetch_status(user_id, biz_id, review_id):
    url = get_biz_review_url(biz_id, review_id)
    html = fetch_html(url)
    is_alive = review_id_on_page(html, review_id)
    return ReviewStatus(
        user_id=user_id, biz_id=biz_id, review_id=review_id, is_alive=is_alive
    )
