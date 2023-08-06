from cryptocompsdk.social.current.parse import CouldNotGetSocialLatestException, social_latest_from_dict, SocialLatest
from cryptocompsdk.request import APIBase
from cryptocompsdk.urls import SOCIAL_LATEST_URL


class SocialLatestAPI(APIBase):
    _exception_class = CouldNotGetSocialLatestException

    def get(self, coin_id: int = 1182) -> SocialLatest:
        payload = dict(
            coinId=coin_id,
        )

        return self._get_one_or_paginated(SOCIAL_LATEST_URL, payload=payload)

    def _class_factory(self, data: dict) -> SocialLatest:
        return social_latest_from_dict(data)
