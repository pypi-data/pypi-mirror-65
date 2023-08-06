import asyncio
import json
import socket
import time

import aiohttp

from tqdm import tqdm

from dblue_mlwatch.config import API_KEY_HEADER
from dblue_mlwatch.logger import logger
from dblue_mlwatch.stores.base import BaseStore

DEFAULT_HEADERS = {
    "Content-Type": "application/json"
}


class RestStore(BaseStore):
    def __init__(self, endpoint, api_key, **kwargs):
        super(RestStore, self).__init__(**kwargs)

        self.url = endpoint
        self.api_key = api_key

        self.headers = DEFAULT_HEADERS
        self.headers[API_KEY_HEADER] = api_key

    def send(self, events: list, **kwargs) -> list:
        """
        Send events to the collector endpoint
        :param events: List of events to send
        :param kwargs:
        :return: List of status(Boolean) suggesting if the event successfully sent to collector or not
        """

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        statuses = loop.run_until_complete(self._send(events=events))

        return statuses

    async def _send(self, events) -> list:
        statuses = []
        connector = aiohttp.TCPConnector(family=socket.AF_INET, ttl_dns_cache=300)

        async with aiohttp.ClientSession(connector=connector) as session:
            # Only use tqdm for batch sending
            events = tqdm(events) if len(events) > 1 else events

            for event in events:
                status_code, response = await self._make_request(session=session, data=event, headers=self.headers)

                if status_code == 200:
                    statuses.append(True)
                else:
                    statuses.append(False)
                    logger.debug("Failed request: %s", event)
                    logger.error("Request failed with status code %s: %s", status_code, response)

        return statuses

    async def _make_request(self, session, data, retries=3, retry_interval=3, **kwargs) -> (int, str):

        for i in range(retries):
            logger.debug("Sending request: %s", json.dumps(data))
            async with session.post(url=self.url, json=data, **kwargs) as response:
                status_code = response.status
                response = await response.text()

            if status_code == 200:
                return status_code, response

            logger.error(
                "Request failed with status code %s, retrying up to %s more times: %s",
                status_code,
                retries - i - 1,
                response
            )
            time.sleep(retry_interval)
        logger.error("Request failed to return code 200 after %s tries", retries)
        return status_code, response
