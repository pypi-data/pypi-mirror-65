# -*- coding: utf-8 -*-
from yandex_checkout_payout.domain.exceptions.api_error import ApiError


class OpenSSLError(ApiError):
    HTTP_CODE = 500
