import json

from google.cloud.pubsub_v1 import PublisherClient


class TopicPublisher:
    def __init__(self, project: str, topic: str):
        """
        Simple Interface to the Publisher mechanism for the pub/sub suite.

        Provide the Project and Topic in the constructor and call the publish method to publish data.

        :param project: Project ID from the GCP console. i.e. "fxqlabs-net-3a8ea"
        :param topic: Topic name from the GCP console. i.e. "etl-event"
        """
        self._publisher = PublisherClient()
        self._topic_path = self._publisher.topic_path(project, topic)

    def publish(self, data: dict, attributes={}, **kwargs) -> str:
        """
        Publish the provided data to the topic

        Example Usage::

            publisher.publish({"name": "elf", "age": 21})


        Resources:

        https://cloud.google.com/pubsub/docs/publisher#config


        :param data: Data must be dict that can be converted to json string.
        :param attributes: Additional Attributes in the form of a dictionary, these are passed as message attributes
        :param kwargs: Any additional Keyword Arguments to be passed as message attributes
        :return: Returns the Event ID as a string i.e. '1029474508993984'
        """
        future = self._publisher.publish(self._topic_path,
                                         data=json.dumps(data).encode("utf-8"),
                                         **attributes,
                                         **kwargs)
        if future.exception():
            raise Exception(future.exception())
        else:
            return future.result()
