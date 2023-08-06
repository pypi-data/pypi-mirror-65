import asyncio
import aiohttp

from .base import ClientBase


class AiohttpClient(ClientBase):

    def prepare(self):
        self.client = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))

    def capture_message(self, message, type, attachments=None):
        asyncio.ensure_future(self._send_request(message, type, attachments))

    async def _send_request(self, message, type, attachments):
        if self.client is None:
            self.prepare()
        copy_id = self.save_copy(message, type)
        async with self.client.post(url=self.address + '/api/v1/events',
                                    json=self.prepare_message(message, type, attachments),
                                    headers=self.headers) as resp:
            if resp.status == 200:
                self.clean_copy(copy_id)

