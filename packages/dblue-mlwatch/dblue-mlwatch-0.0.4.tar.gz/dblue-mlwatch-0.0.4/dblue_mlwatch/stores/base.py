class BaseStore:

    def __init__(self, **kwargs):
        pass

    def send(self, events: list, **kwargs) -> list:
        """
        Send events to store
        :param events: List of records
        :param kwargs:
        :return: List of status(Boolean) suggesting if the event successfully sent to store or not
        """
        raise NotImplementedError()
