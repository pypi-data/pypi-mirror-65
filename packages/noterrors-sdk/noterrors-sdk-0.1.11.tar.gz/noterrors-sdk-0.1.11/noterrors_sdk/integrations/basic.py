import urllib3
import requests

from .base import ClientBase

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BasicClient(ClientBase):

    def prepare(self):
        self.client = requests.Session()
        self.client.verify = False

    def capture_message(self, message, type, attachments=None):
        if self.client is None:
            self.prepare()
        copy_id = self.save_copy(message, type)
        with self.client.post(self.address + '/api/v1/events', json=self.prepare_message(message, type, attachments),
                headers=self.headers, verify=False) as resp:
            if resp.status_code == 200:
                self.clean_copy(copy_id)

