import re

BIZ_REVIEW_URL = "https://www.yelp.com/biz/{}?hrid={}"


def get_biz_review_url(biz_id, review_id):
    return BIZ_REVIEW_URL.format(biz_id, review_id)


def review_id_on_page(page_text, review_id):
    return bool(re.search(review_id, page_text))
