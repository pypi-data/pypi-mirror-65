import time


class ClientBase:
    client = None

    def __init__(self, address, project_token, auth_key):
        self.address = address
        self.project_token = project_token
        self.auth_key = auth_key
        self.headers = {
            'Project-Token': project_token,
            'Authenticate': auth_key
        }

    def prepare(self):
        pass

    def prepare_message(self, message, type, attachments):
        # TODO: apply attachments
        if attachments:
            attachments = [a for a in attachments]
        return {'type': type, 'send_time': time.time(), 'function': '', 'filename': '', **message, 'attachments': attachments}

    def capture_message(self, message, type, attachments=None):
        raise NotImplementedError

    def save_copy(self, message, type):
        pass

    def clean_copy(self, copy_id):
        pass
