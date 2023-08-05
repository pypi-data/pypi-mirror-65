# -*- coding: utf-8 -*-


class HttpVerb(object):
    """
    Constants representing http method verbs. Available values are:

    * yandex_checkout_payout.domain.common.HttpVerb.GET
    * yandex_checkout_payout.domain.common.HttpVerb.POST
    * yandex_checkout_payout.domain.common.HttpVerb.PUT
    * yandex_checkout_payout.domain.common.HttpVerb.PATCH
    * yandex_checkout_payout.domain.common.HttpVerb.HEAD
    * yandex_checkout_payout.domain.common.HttpVerb.OPTIONS
    * yandex_checkout_payout.domain.common.HttpVerb.DELETE
    """
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    PATCH = 'patch'
    HEAD = 'head'
    OPTIONS = 'options'
    DELETE = 'delete'
