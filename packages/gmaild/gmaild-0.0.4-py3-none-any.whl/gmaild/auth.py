from google.oauth2 import service_account
import googleapiclient.discovery


SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify'
]


class Service:
    def __init__(self, delegate_email, creds_file, creds_dir):
        creds_path = '{}/{}'.format(creds_dir, creds_file)
        credentials = service_account.Credentials.from_service_account_file(
                creds_path, scopes=SCOPES).with_subject(delegate_email)

        self.authorized_service = googleapiclient.discovery.build(
            'gmail', 'v1', credentials=credentials)

    def use(self):
        return self.authorized_service
