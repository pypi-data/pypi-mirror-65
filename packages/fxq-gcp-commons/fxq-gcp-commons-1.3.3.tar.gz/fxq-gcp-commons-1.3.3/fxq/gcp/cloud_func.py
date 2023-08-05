from abc import ABC
from http import HTTPStatus

from flask import jsonify


class CloudFunctionResponse(ABC):
    pass


class _CloudFunctionResponseBuilder(ABC):
    def __init__(self, code, response_body):
        self._code = code
        self._response_body = response_body

    def build(self):
        return jsonify(self._response_body), self._code


class Success(CloudFunctionResponse):
    class Builder(_CloudFunctionResponseBuilder):
        def __init__(self):
            super().__init__(
                HTTPStatus.OK,
                {}
            )

        def with_body(self, body):
            self._response_body = body
            return self

        def with_code(self, code: HTTPStatus):
            self._code = code
            return self


class Error(CloudFunctionResponse):
    class Builder(_CloudFunctionResponseBuilder):
        def __init__(self):
            super().__init__(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {'error': "An Internal error occurred"}
            )

        def with_message(self, message: str):
            self._response_body['error'] = message
            return self

        def with_code(self, code: HTTPStatus):
            self._code = code
            return self


class PubSubEventContext:
    """
    The context object for the pubsb event.

    🤔 https://cloud.google.com/functions/docs/writing/background#function_parameters
    """

    def __init__(self, event_id: str, timestamp: str, event_type: str, resource: dict):
        """
        Constructor for the Context
        :param event_id: String - A unique ID for the event. For example: "70172329041928".
        :param timestamp: String (ISO 8601) - The date/time this event was created. For example: "2018-04-09T07:56:12.975Z".
        :param event_type: String - The type of the event. For example: "google.pubsub.topic.publish".
        :param resource: String - The resource that emitted the event.
        """
        self.event_id = event_id
        self.timestamp = timestamp
        self.event_type = event_type
        self.resource = resource
