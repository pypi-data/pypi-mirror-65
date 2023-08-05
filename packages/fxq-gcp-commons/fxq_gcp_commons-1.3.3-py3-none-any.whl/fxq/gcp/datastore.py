import uuid

from google.cloud import datastore


class DatastoreDao:
    def __init__(self):
        self.client = datastore.Client()

    def save(self, kind: str, obj: dict, return_entity=True):
        key = self.client.key(kind, str(uuid.uuid4()).replace("-", "", ))
        entity = datastore.Entity(key=key)
        entity.update(obj)
        self.client.put(entity)

        if return_entity:
            return self.client.get(key)
        else:
            return None

    def save_or_update(self, kind: str, obj: dict, update_on: list):
        """
        Updates the provided object in the datastore if it exists, otherwise will save as a new item.

        .. code-block:: python

            save_or_update(
                     kind='fxq_event',
                     obj={
                         "fxq_provider": "FXCM",
                         "fxq_last_update": datetime.now(),
                         **event
                     },
                     update_on=["name", "dateTime"]
                 )

        :param kind: GCP Datastore "Kind"
        :param obj: Object to be stored
        :param update_on: Which fields to use as match keys i.e. [name, age]
        :return:
        """
        did_update = False

        query = self.client.query(kind=kind)
        for key in update_on:
            query.add_filter(key, "=", obj[key])

        for entity in query.fetch():
            did_update = True
            entity.update(obj)
            self.client.put(entity)

        if not did_update:
            self.save(kind, obj, False)

    def get(self, kind: str, query_params: dict):
        """
        Example:

        get(
            kind='fxq_event', query_params={
                'name': ('=', 'ANZ Commodity Price')
            })

        :param kind:
        :param query_params:
        :return:
        """
        query = self.client.query(kind=kind)
        for field, q_tuple in query_params.items():
            query.add_filter(field, q_tuple[0], q_tuple[1])

        resp = []
        for entity in query.fetch():
            resp.append(entity)

        return resp
