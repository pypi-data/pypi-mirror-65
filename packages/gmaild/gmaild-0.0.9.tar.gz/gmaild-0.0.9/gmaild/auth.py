from google.oauth2 import service_account
import googleapiclient.discovery
import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(logging.WARNING)
logger.addHandler(sh)

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify'
]


class Service:
    def __init__(self, delegate_email, creds_file, creds_dir):
        creds_path = '{}/{}'.format(creds_dir, creds_file)

        logger.warning("start building creds")
        credentials = service_account.Credentials.from_service_account_file(
                creds_path, scopes=SCOPES).with_subject(delegate_email)

        logger.warning("start building service")

        try:
            self._build_service(credentials)
        # Try again incase http://www.googleapis.com/ cannot be reached from within docker
        except Exception:
            self._build_service(credentials)

    def use(self):
        return self.authorized_service

    def _build_service(self, credentials):
        self.authorized_service = googleapiclient.discovery.build(
            'gmail', 'v1', credentials=credentials, cache_discovery=False)
        logger.warning("done building service")
