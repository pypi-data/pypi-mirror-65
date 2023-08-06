import platform
import time

from datetime import datetime
from typing import Dict, List

from dblue_mlwatch import config
from dblue_mlwatch.exceptions import DblueMLWatchException
from dblue_mlwatch.stores.rest import RestStore
from dblue_mlwatch.version import VERSION


class BaseTracker:

    def __init__(self, model_id: str, model_version: str, account: str = None, project: str = None,
                 api_key: str = None):
        """
        :param model_id: Dblue MLWatch model id
        :param model_version: Dblue MLWatch model version
        :param account: Dblue MLWatch account id
        :param project: Dblue MLWatch project id
        :param api_key: Dblue MLWatch API Key
        """

        model_id = model_id
        model_version = model_version

        account = account or config.ACCOUNT
        project = project or config.PROJECT
        api_key = api_key or config.API_KEY

        if not account:
            raise DblueMLWatchException(
                "Please specify account in the func call or in DBLUE_MLWATCH_ACCOUNT env variable"
            )

        if not project:
            raise DblueMLWatchException(
                "Please specify project in the func call or in DBLUE_MLWATCH_PROJECT env variable"
            )

        if not api_key:
            raise DblueMLWatchException(
                "Please specify api_key in the function call or in DBLUE_MLWATCH_API_KEY env variable"
            )

        self.account = account
        self.project = project
        self.model_id = model_id
        self.model_version = model_version
        self.api_key = api_key
        self.endpoint = config.ENDPOINT

        self.store = RestStore(endpoint=self.endpoint, api_key=self.api_key)

    def emit(self, events: List[Dict]) -> List:
        """
        Emit events to store
        :param events: List of events
        :return: List of emit statuses
        """
        common = {
            'account': self.account,
            'project': self.project,
            'model_id': self.model_id,
            'model_version': self.model_version,
            'sdk': 'py-{}'.format(VERSION),
            'local_time': datetime.now().isoformat(),
            'utc_time': datetime.utcnow().isoformat(),
            'event_tstamp': time.time(),
            'tz_offset': time.strftime("%z", time.gmtime()),
            'tz_name': time.tzname[0],
            'hostname': platform.node(),
        }

        for event in events:
            event.update(common)

        return self.store.send(events=events)
