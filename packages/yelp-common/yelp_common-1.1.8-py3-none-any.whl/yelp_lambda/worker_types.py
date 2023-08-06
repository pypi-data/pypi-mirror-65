from typing import List

from yelp_fetcher.reviews import Review
from yelp_lambda.common_types import JobType, LambdaMessage


class WorkerRequest(LambdaMessage):
    def __init__(self, job_type):
        super().__init__(job_type)


class ReviewsWorkerRequest(WorkerRequest):
    def __init__(self, user_id, url):
        super().__init__(JobType.REVIEWS.value)
        self.user_id = user_id
        self.url = url


class StatusesWorkerRequest(WorkerRequest):
    def __init__(self, user_id, biz_id, review_id):
        super().__init__(JobType.STATUSES.value)
        self.user_id = user_id
        self.biz_id = biz_id
        self.review_id = review_id


class WorkerResponse(LambdaMessage):
    def __init__(self, job_type):
        super().__init__(job_type)


class ReviewsWorkerResult(WorkerResponse):
    def __init__(self, user_id, reviews: List[Review]):
        super().__init__(JobType.REVIEWS.value)
        self.user_id = user_id
        self.reviews = reviews


class StatusesWorkerResult(WorkerResponse):
    def __init__(self, user_id, biz_id, review_id, is_alive):
        super().__init__(JobType.STATUSES.value)
        self.user_id = user_id
        self.biz_id = biz_id
        self.review_id = review_id
        self.is_alive = is_alive
