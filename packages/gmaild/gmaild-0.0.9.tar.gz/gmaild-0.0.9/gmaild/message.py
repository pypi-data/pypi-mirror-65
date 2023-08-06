import base64
import email
import logging

from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)


class AttachmentPart:
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data

    def load(self):
        return {
            'filename': self.filename,
            'data': self.data
        }


class Message:
    def __init__(self, message_id):
        self.id = message_id
        self.date = None
        self.sender = None
        self.cc = None
        self.subject = None
        self.text_body = None
        self.html_body = None
        self.attachments = []

    def add_date(self, date):
        self.date = date

    def add_sender(self, sender):
        self.sender = sender

    def add_cc(self, cc):
        self.cc = cc

    def add_subject(self, subject):
        self.subject = subject

    def add_text_body(self, text_body):
        self.text_body = text_body

    def add_html_body(self, html_body):
        self.html_body = html_body

    def add_attachment(self, attachment):
        if isinstance(attachment, AttachmentPart):
            self.attachments.append(attachment)
        else:
            raise TypeError('input must be an AttachmentPart')


class Payload:
    def __init__(self):
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

    def deliver(self):
        payload = []
        for msg in self.messages:
            message = dict()
            message['id'] = msg.id
            if msg.date:
                message['date'] = msg.date
            if msg.sender:
                message['from'] = msg.sender
            if msg.cc:
                message['cc'] = msg.cc
            if msg.subject:
                message['subject'] = msg.subject
            if msg.text_body:
                message['text_body'] = msg.text_body
            if msg.html_body:
                message['html_body'] = msg.html_body
            if len(msg.attachments) != 0:
                attachments = [att.load() for att in msg.attachments]
                message['attachments'] = attachments
            payload.append(message)
        return payload


class MessageHandler:
    def __init__(self, service):
        self.service = service
        self.payload = Payload()

    def process_messages(self, response):
        try:
            for msg in response:
                raw_message = self._get_raw_message(msg['id'])
                self._parse_message_contents(raw_message, msg['id'])
                self._mark_as_read(msg['id'])
            return self.payload.deliver()
        except Exception as error:
            logger.error('Cannot process message: {}'.format(error))

    def _get_raw_message(self, msg_id):
        try:
            response = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='raw').execute()

            message = base64.urlsafe_b64decode(response['raw'].encode('ASCII'))
            return message
        except HttpError as error:
            logger.error('Cannot get email with id {}: {}'.format(msg_id, error))

    def _parse_message_contents(self, message_bytes, msg_id):
        # Builtin email.Message object
        message = email.message_from_bytes(message_bytes)

        # inboxcourier.Message object
        courier_message = Message(msg_id)

        # Parsing all email parts
        courier_message = get_date(courier_message, message)
        courier_message = get_sender(courier_message, message)
        courier_message = get_cc(courier_message, message)
        courier_message = get_subject(courier_message, message)
        courier_message = get_text_body(courier_message, message)
        courier_message = get_html_body(courier_message, message)
        courier_message = get_attachments(courier_message, message)

        self.payload.add_message(courier_message)

    def _mark_as_read(self, msg_id):
        try:
            labels = {'removeLabelIds': ['UNREAD'], 'addLabelIds': []}
            self.service.users().messages().modify(
                userId='me',
                id=msg_id,
                body=labels).execute()
        except HttpError as error:
            logger.error('Cannot mark email as unread: {}'.format(error))


def get_date(message, email):
    try:
        date = email.get('date')
        if date:
            message.add_date(date)
        return message
    except Exception as error:
        logger.warning('error retrieving email date: {}'.format(error))


def get_sender(message, email):
    try:
        sender = email.get('from')
        if sender:
            message.add_sender(sender)
        return message
    except Exception as error:
        logger.warning('error retrieving email sender: {}'.format(error))


def get_cc(message, email):
    try:
        cc = email.get_all('cc')
        if cc:
            message.add_cc(cc)
        return message
    except Exception as error:
        logger.warning('error retrieving email cc: {}'.format(error))


def get_subject(message, email):
    try:
        subject = email.get('subject')
        if subject:
            message.add_subject(subject)
        return message
    except Exception as error:
        logger.warning('error retrieving email subject: {}'.format(error))


def get_text_body(message, email):
    '''Get body of a Message.'''
    try:
        text_body = ''
        has_text_body = False

        for part in email.walk():
            if part.get_content_type() == 'text/plain':
                has_text_body = True
                text_body += part.get_payload()
        if has_text_body:
            message.add_text_body(text_body)
        return message
    except Exception as error:
        logger.warning('Cannot get email body: {}'.format(error))


def get_html_body(message, email):
    try:
        html_body = ''
        has_html_body = False

        for part in email.walk():
            if part.get_content_type() == 'text/html':
                has_html_body = True
                html_body += part.get_payload()
        if has_html_body:
            message.add_html_body(html_body)
        return message
    except Exception as error:
        logger.warning('Cannot get email body: {}'.format(error))


def get_attachments(message, email):
    try:
        for part in email.walk():
            content_disposition = part.get('Content-Disposition')
            if content_disposition and 'attachment' in content_disposition:
                filename = part.get_filename()
                data = part.get_payload()
                message.add_attachment(AttachmentPart(filename, data))
        return message

    except Exception as error:
        logger.error('Cannot get attachment from email: {}'.format(error))
