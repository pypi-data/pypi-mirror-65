from yelp_lambda.common_types import (
    BIZ_ID,
    REVIEW_ID,
    URL,
    USER_ID,
    JobType,
    LambdaMessage,
)
from yelp_lambda.worker_types import ReviewsWorkerRequest, StatusesWorkerRequest


class DispatcherRequest(LambdaMessage):
    def __init__(self, job_type, args_list):
        super().__init__(job_type)
        self.args_list = args_list

    def get_worker_requests(self):
        if self.job_type == JobType.REVIEWS.value:
            worker_request_type = ReviewsWorkerRequest
        elif self.job_type == JobType.STATUSES.value:
            worker_request_type = StatusesWorkerRequest
        else:
            raise ValueError(f"Unsupported job_type: {self.job_type}")

        return [worker_request_type(**args) for args in self.args_list]


class ReviewsDispatcherRequest(DispatcherRequest):
    def __init__(self, user_id, urls):
        self.user_id = user_id
        self.urls = urls
        args_list = [{USER_ID: user_id, URL: url} for url in urls]
        super().__init__(JobType.REVIEWS.value, args_list)


class StatusesDispatcherRequest(DispatcherRequest):
    def __init__(self, user_id, biz_ids_to_review_ids):
        self.user_id = user_id
        self.biz_ids_to_review_ids = biz_ids_to_review_ids
        args_list = [
            {USER_ID: user_id, BIZ_ID: biz_id, REVIEW_ID: review_id,}
            for biz_id, review_id in biz_ids_to_review_ids.items()
        ]
        super().__init__(JobType.STATUSES.value, args_list)
