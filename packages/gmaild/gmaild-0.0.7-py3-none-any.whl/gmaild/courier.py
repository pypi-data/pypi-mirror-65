import threading

from . import auth, dispatch


class Courier:
    def __init__(self, delegate_email, creds_file, creds_dir='.'):
        authorized_service = auth.Service(delegate_email, creds_file, creds_dir)
        self.dispatcher = dispatch.Dispatcher(authorized_service.use())

    def run(self, label_ids, filter_action, topic_name):
        # TODO: validate input
        pubsub_request = {
            'labelIds': label_ids,
            'labelFilterAction': filter_action,
            'topicName': topic_name
        }

        # Calls watch() on inbox once per day as recommended by google api docs
        watcher_thread = threading.Thread(
            target=self.dispatcher.watch_inbox,
            args=(pubsub_request,),
            daemon=True)

        watcher_thread.start()

    # Returns all messages that match the query string
    def deliver_mail(self, query):
        return self.dispatcher.check_inbox(query)
