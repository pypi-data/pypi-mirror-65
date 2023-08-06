import logging
import schedule
import time

from googleapiclient.errors import HttpError
from . import message

logger = logging.getLogger(__name__)


class Dispatcher:
    def __init__(self, service):
        self.service = service
        self.message_handler = message.MessageHandler(self.service)

    def watch_inbox(self, pubsub_request):
        # Call `watch()` on inbox once per day
        schedule.every().day.do(
            self._watch_inbox_helper,
            request=pubsub_request)

        schedule.run_all()
        while True:
            schedule.run_pending()
            time.sleep(1)

    def _watch_inbox_helper(self, request):
        self.service.users().watch(
            userId='me',
            body=request).execute()

    def check_inbox(self, query):
        try:
            received_messages = self._list_messages(query)
            processed_payload = self.message_handler.process_messages(received_messages)

            return processed_payload
        except Exception as error:
            logger.error('Cannot get mail: {}'.format(error))

    def _list_messages(self, query):
        try:
            response = self.service.users().messages().list(
                userId='me',
                q=query).execute()

            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.service.users().messages().list(
                    userId='me',
                    q=query,
                    pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages
        except HttpError as error:
            print('list_messages error: {}'.format(error))
