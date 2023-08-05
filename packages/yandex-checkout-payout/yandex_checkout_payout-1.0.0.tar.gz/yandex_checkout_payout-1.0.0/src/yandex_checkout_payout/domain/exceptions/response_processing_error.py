# -*- coding: utf-8 -*-
from yandex_checkout_payout.domain.exceptions.api_error import ApiError


class ResponseProcessingError(ApiError):
    HTTP_CODE = 202
