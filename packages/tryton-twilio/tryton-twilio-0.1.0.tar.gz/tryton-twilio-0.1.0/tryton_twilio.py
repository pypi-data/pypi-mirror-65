# This file is part of tryton-twilio. The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import logging
import sys

from trytond.config import config
from trytond.transaction import Transaction
from twilio.rest import Client

account = config.get('twilio', 'account')
token = config.get('twilio', 'token')
from_ = config.get('twilio', 'from')
logger = logging.getLogger(__name__)


def send_sms_transactional(text, to, transaction=None, datamanager=None):
    if transaction is None:
        transaction = Transaction()
    assert isinstance(transaction, Transaction), transaction
    if datamanager is None:
        datamanager = SMSDataManager()
    datamanager = transaction.join(datamanager)
    datamanager.put(text, to)


def send_sms(text, to, client=None):
    if client is None:
        client = get_client()
    try:
        client.messages.create(to=to, from_=from_, body=text)
    except Exception:
        logger.error('fail to send SMS', exc_info=True)


def get_client():
    return Client(account, token)


class SMSDataManager:

    def __init__(self):
        self.queue = []
        self._client = None

    def put(self, text, to):
        self.queue.append((text, to))

    def __eq__(self, other):
        if not isinstance(other, SMSDataManager):
            return NotImplemented
        return id(self) == id(other)

    def abort(self, trans):
        self._finish()

    def tpc_begin(self, trans):
        pass

    def commit(self, trans):
        pass

    def tpc_vote(self, trans):
        if self._client is None:
            self._client = get_client()

    def tpc_finish(self, trans):
        if self._client is not None:
            for text, to in self.queue:
                send_sms(text, to, client=self._client)
            self._finish()

    def tpc_abort(self, trans):
        self._finish()

    def _finish(self):
        self._client = None
        self.queue = []


if __name__ == '__main__':
    def prompt(prompt):
        sys.stdout.write(prompt + ": ")
        sys.stdout.flush()
        return sys.stdin.readline().strip()
    config.update_etc()
    to = prompt("To")
    print("Enter message, end with ^D:")
    msg = ''
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        msg = msg + line
    print("Message length is %d" % len(msg))

    send_sms(msg, to)
