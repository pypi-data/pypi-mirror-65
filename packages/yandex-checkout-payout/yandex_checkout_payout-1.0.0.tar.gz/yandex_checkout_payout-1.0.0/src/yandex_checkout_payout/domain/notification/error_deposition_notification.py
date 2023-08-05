# -*- coding: utf-8 -*-
from yandex_checkout_payout.domain.common.client import ApiClient
from yandex_checkout_payout.domain.common.openssl_helper import OpenSSLHelper
from yandex_checkout_payout.domain.common.xml_helper import XMLHelper
from yandex_checkout_payout.domain.exceptions.api_error import ApiError
from yandex_checkout_payout.domain.notification.error_deposition_notification_request import \
    ErrorDepositionNotificationRequest
from yandex_checkout_payout.domain.notification.error_deposition_notification_response import \
    ErrorDepositionNotificationResponse


class ErrorDepositionNotification:

    def __init__(self):
        self.client = ApiClient()

    @classmethod
    def input(cls, response):
        instance = cls()
        data = instance.client.prepare_response(response)
        if 'errorDepositionNotificationRequest' in data:
            return ErrorDepositionNotificationRequest(data['errorDepositionNotificationRequest'])
        else:
            raise ApiError('Invalid ErrorDepositionNotificationRequest')

    @classmethod
    def output(cls, status):
        instance = cls()
        data = ErrorDepositionNotificationResponse({"status": status})
        request = OpenSSLHelper.encrypt_pkcs7(XMLHelper.object_to_xml(data.map()), instance.client.keychain)
        if request:
            return request.decode("utf-8")
        else:
            raise ApiError('Cannot create ErrorDepositionNotificationResponse')
