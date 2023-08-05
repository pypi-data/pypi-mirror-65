from enum import Enum

JOB_TYPE = "job_type"

URL = "url"

USER_ID = "user_id"
BIZ_ID = "biz_id"
REVIEW_ID = "review_id"


class JobType(Enum):
    REVIEWS = "reviews"
    STATUSES = "statuses"


class LambdaMessage:
    def __init__(self, job_type):
        assert job_type
        self.job_type = job_type
