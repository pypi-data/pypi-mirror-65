from imaplib import IMAP4_SSL
from unittest import mock
from datetime import datetime

from pytest import fixture, raises
from pytz import timezone

from email_lib.emails import (
    EmailLogicError,
    EmailClient,
    EmailScraper,
    EmailQueryBuilder,
    EmailThread,
    EmailMessage,
)

SERVER = 'mail.server.com'
MAILBOX = 'INBOX'
ACCOUNT = 'da_test_account@server.com'
PASSWORD = 'd453KUR3PWD'


@fixture
def client():
    class FAKE_IMAP_SSL:
        def __init__(self, server):
            pass

    with mock.patch('email_lib.emails.IMAP4_SSL', FAKE_IMAP_SSL):
        return EmailClient(SERVER, ACCOUNT, PASSWORD)

class Part:
    def __init__(self, content_type, content):
        self.content_type = content_type
        self.content = content

    def get_content_type(self):
        return self.content_type

    def __str__(self):
        return self.content

class RawMessage(dict):
    def get_payload(self):
        return self['Payload']


def test_login_success(client):
    account = None
    password = None

    def fake_login(acct, pwd):
        nonlocal account, password
        account = acct
        password = pwd

    client_mock = mock.MagicMock()
    client_mock.login.side_effect = fake_login
    client.client = client_mock

    client.login()

    client_mock.login.assert_called_once()
    assert account == ACCOUNT
    assert password == PASSWORD


def test_login_failure(client):
    message = None

    def fake_login(*args):
        raise IMAP4_SSL.error()

    client_mock = mock.MagicMock()
    client_mock.login.side_effect = fake_login
    client.client = client_mock

    with raises(EmailLogicError) as err:
        client.login()

    assert str(err.value) == "Invalid imap login to {} for account {}".format(
        SERVER, ACCOUNT
    )


def test_set_mailbox_success(client):
    mailbox = None
    read_only = False

    def fake_select(mb, readonly=False):
        nonlocal mailbox, read_only
        mailbox = mb
        read_only = readonly
        return ['OK', None]

    client_mock = mock.MagicMock()
    client_mock.select.side_effect = fake_select
    client.client = client_mock

    client.set_mailbox(MAILBOX)

    client_mock.select.assert_called_once()
    assert mailbox == MAILBOX
    assert read_only


def test_set_mailbox_failure(client):
    def fake_select(mb, readonly=False):
        return ['KO', None]

    client_mock = mock.MagicMock()
    client_mock.select.side_effect = fake_select
    client.client = client_mock

    with raises(EmailLogicError) as err:
        client.set_mailbox('fakebox')

    assert str(err.value) == 'Could not connect to mailbox fakebox'


def test_search_success(client):
    query = None
    fmt = None
    email_ids = None

    def fake_search(phony, q):
        nonlocal query
        query = q
        return ['OK', [b'42 21']]

    def fake_fetch(ids, parse_format):
        nonlocal fmt, email_ids
        fmt = parse_format
        email_ids = ids
        return [
            'OK',
            [
                [
                    '42 (RFC822 {42090}',
                    b'Received: from test_email@server.com\r\n'
                    b'Message-Id: <1234@>\r\n'
                    b'Mime-Version: 1.0\r\n'
                    b'Content-Type: text/plain; charset="us-ascii"\r\n'
                    b'Date: Mon, 3 Feb 2020 13:37:42 -0800\r\n'
                    b'To: user-group@server.com\r\n'
                    b'From: Email Tester <test_email@server.com>\r\n'
                    b'Subject: Email 42\r\n'
                    b'Precedence: bulk\r\n\r\n'
                    b'This is a test email,\r\n'
                    b'Email Tester\r\n'
                ],
                [
                    '21 (RFC822 {42090}',
                    b'Received: from test_email@server.com\r\n'
                    b'Message-Id: <5678@>\r\n'
                    b'Mime-Version: 1.0\r\n'
                    b'Content-Type: text/plain; charset="us-ascii"\r\n'
                    b'Date: Mon, 3 Feb 2020 13:37:42 -0800\r\n'
                    b'To: user-group@server.com\r\n'
                    b'From: Email Tester <test_email@server.com>\r\n'
                    b'Subject: Email 21\r\n'
                    b'Precedence: bulk\r\n\r\n'
                    b'This is a test email,\r\n'
                    b'Email Tester\r\n'
                ]
            ]
        ]

    client_mock = mock.MagicMock()
    client_mock.search.side_effect = fake_search
    client_mock.fetch.side_effect = fake_fetch
    client.client = client_mock

    messages = [message for message in client.search('(BEFORE 2020-02-01)')]

    assert len(messages) == 2
    assert messages[0].message_id == '<1234@>'
    assert messages[0].subject == 'Email 42'
    assert messages[1].message_id == '<5678@>'
    assert messages[1].subject == 'Email 21'


def test_search_bad_time_window(client):
    def fake_search(_phony, _query):
        return ['KO', None]

    client_mock = mock.MagicMock()
    client_mock.search.side_effect = fake_search
    client.client = client_mock

    with raises(EmailLogicError) as err:
        [_ for _ in client.search('(BEFORE 2020-02-01)')]

    assert str(err.value) == "Couldn't find results for that time range"


def test_search_fetch_fail(client):
    def fake_search(_phony, _query):
        return ['OK', [b'42 21']]

    def fake_fetch(_email_ids, _fmt):
        return ['KO', None]

    client_mock = mock.MagicMock()
    client_mock.search.side_effect = fake_search
    client_mock.fetch.side_effect = fake_fetch
    client.client = client_mock

    with raises(EmailLogicError) as err:
        [_ for _ in client.search('(BEFORE 2020-02-01)')]

    assert str(err.value) == "Could not fetch messages"


def test_query_builder():
    builder = EmailQueryBuilder()

    builder.start(datetime(2020, 1, 2, 12, 0, 0))
    builder.stop(datetime(2020, 2, 1, 13, 37, 0))
    builder.subject('Builder Test')

    query = builder.build()

    assert query == '(SINCE 02-Jan-2020) (BEFORE 01-Feb-2020) (SUBJECT "Builder Test")'


def test_email_message_long_subject():
    raw_message = RawMessage({
        'Subject': 'This is an email with a very\r\n long subject',
        'From': 'test_email@server.com',
        'To': 'test_receiver@server.com, second_receiver@server.com',
        'Message-Id': '<42@>',
        'References': '',
        'Date': 'Sun, 02 Feb 2020 15:12:03 +0000 (UTC)',
        'Payload': [
                Part('text/html', '<html><body>Content 1</body></html>'),
                Part('text/plain', 'Content 2'),
                Part('image/png', 'image.png'),
        ]
    })

    message = EmailMessage(raw_message)

    assert message.subject == 'This is an email with a very long subject'


def test_email_reply():
    raw_message = RawMessage({
        'Subject': 'Re: Test Subject',
        'From': 'test_email@server.com',
        'To': 'test_receiver@server.com, second_receiver@server.com',
        'Message-Id': '<42@>',
        'References': '<1337@>',
        'Date': 'Sun, 02 Feb 2020 15:12:03 +0000 (UTC)',
        'Payload': [
                Part('text/html', '<html><body>Content 1</body></html>'),
                Part('text/plain', 'Content 2'),
                Part('image/png', 'image.png'),
        ]
    })

    message = EmailMessage(raw_message)

    assert message.message == raw_message
    assert message.subject == 'Re: Test Subject'
    assert message.topic == 'Test Subject'
    assert message.from_addr == raw_message['From']
    assert message.to_addrs == [
        "test_receiver@server.com", "second_receiver@server.com"
    ]
    assert message.message_id == '<42@>'
    assert '<1337@>' in message.references
    assert message.date == timezone('UTC').localize(
        datetime(2020, 2, 2, 15, 12, 3))
    assert not message.is_thread

    assert len(str(message)) != 0
    assert len(repr(message)) != 0
    assert message.content == 'Content 2'

def test_email_tags():
    message = EmailMessage(RawMessage({
        'Subject': 'Re: Test Subject',
        'From': 'test_email@server.com',
        'To': 'test_receiver@server.com, second_receiver@server.com',
        'Message-Id': '<42@>',
        'References': '<1337@>',
        'Date': 'Sun, 02 Feb 2020 15:12:03 +0000 (UTC)',
        'Payload': [
                Part('text/plain', '#network #hostdown'),
        ]
    }))

    assert message.tags == set(['network', 'hostdown'])

def test_thread_originator():
    raw_message = {
        'Subject': 'Test Subject',
        'From': 'test_email@server.com',
        'To': 'test_receiver@server.com, second_receiver@server.com',
        'Message-Id': '<42@>',
        'References': '',
        'Date': 'Sun, 02 Feb 2020 15:12:03 +0000 (UTC)'
    }

    message = EmailMessage(raw_message)

    assert message.message == raw_message
    assert message.subject == 'Test Subject'
    assert message.topic == 'Test Subject'
    assert message.from_addr == raw_message['From']
    assert message.to_addrs == [
        "test_receiver@server.com", "second_receiver@server.com"
    ]
    assert message.message_id == '<42@>'
    assert not message.references
    assert message.date == timezone('UTC').localize(
        datetime(2020, 2, 2, 15, 12, 3))
    assert message.is_thread


def test_email_thread_add_first():
    thread = EmailThread()

    head_message = EmailMessage({
        'Subject': 'Test Subject',
        'From': 'test_email@server.com',
        'To': 'test_receiver@server.com, second_receiver@server.com',
        'Message-Id': '<42@>',
        'References': [],
        'Date': 'Sun, 02 Feb 2020 15:12:03 +0000 (UTC)'
    })

    thread.add(head_message)

    assert thread.messages == {'<42@>': head_message}
    assert thread.first == head_message
    assert str(thread) == '{}: {}'.format(
        thread.subject, head_message.date.strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    assert repr(thread) == '{}: {}'.format(
        thread.subject, head_message.date.strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    assert len(thread) == 1

    for message in thread:
        assert message.message_id == '<42@>'


def test_email_thread_long_subject():
    thread = EmailThread()

    head_message = EmailMessage({
        'Subject': 'This is an email with a very\r\n long subject',
        'From': 'test_email@server.com',
        'To': 'test_receiver@server.com, second_receiver@server.com',
        'Message-Id': '<42@>',
        'References': [],
        'Date': 'Sun, 02 Feb 2020 15:12:03 +0000 (UTC)'
    })

    thread.add(head_message)

    assert thread.first.subject == 'This is an email with a very long subject'
    assert thread.first.topic == 'This is an email with a very long subject'


def test_email_thread_has():
    thread = EmailThread()

    head_message = EmailMessage({
        'Subject': 'Test Subject',
        'From': 'test_email@server.com',
        'To': 'test_receiver@server.com, second_receiver@server.com',
        'Message-Id': '<42@>',
        'References': '',
        'Date': 'Sun, 02 Feb 2020 15:12:03 +0000 (UTC)'
    })

    tail_message = EmailMessage({
        'Subject': 'Re: Test Subject',
        'From': 'test_email@server.com',
        'To': 'test_receiver@server.com, second_receiver@server.com',
        'Message-Id': '<1337@>',
        'References': '<42@>',
        'Date': 'Sun, 02 Feb 2020 15:12:03 +0000 (UTC)'
    })

    thread.add(head_message)
    thread.add(tail_message)

    assert thread.has(head_message.message_id)
    assert thread.has_message_id(head_message.message_id)
    assert thread.has(tail_message)
    assert thread.has_message(tail_message)

def test_email_thread_try_add_first():
    thread = EmailThread()

    head_message = EmailMessage({
        'Subject': 'Test Subject',
        'From': 'test_email@server.com',
        'To': 'test_receiver@server.com, second_receiver@server.com',
        'Message-Id': '<42@>',
        'References': '',
        'Date': 'Sun, 02 Feb 2020 15:12:03 +0000 (UTC)'
    })

    thread.try_add(head_message)

    assert thread.messages == {'<42@>': head_message}
    assert thread.first == head_message


def test_email_thread_add_two():
    thread = EmailThread()

    head_message = EmailMessage({
        'Subject': 'Test Subject',
        'From': 'test_email@server.com',
        'To': 'test_receiver@server.com, second_receiver@server.com',
        'Message-Id': '<42@>',
        'References': '',
        'Date': 'Sun, 02 Feb 2020 15:12:03 +0000 (UTC)'
    })

    tail_message = EmailMessage({
        'Subject': 'Re: Test Subject',
        'From': 'test_email@server.com',
        'To': 'test_receiver@server.com, second_receiver@server.com',
        'Message-Id': '<1337@>',
        'References': '<42@>',
        'Date': 'Sun, 02 Feb 2020 15:12:03 +0000 (UTC)'
    })

    thread.try_add(head_message)
    thread.try_add(tail_message)

    assert thread.messages == {'<42@>': head_message, '<1337@>': tail_message}
    assert thread.first == head_message

def test_email_thread_date():
    thread = EmailThread()

    head_message = EmailMessage({
        'Subject': 'Test Subject',
        'From': 'test_email@server.com',
        'To': 'test_receiver@server.com, second_receiver@server.com',
        'Message-Id': '<42@>',
        'References': '',
        'Date': 'Sun, 02 Feb 2020 15:12:03 +0000 (UTC)'
    })

    tail_message = EmailMessage({
        'Subject': 'Re: Test Subject',
        'From': 'test_email@server.com',
        'To': 'test_receiver@server.com, second_receiver@server.com',
        'Message-Id': '<1337@>',
        'References': '<42@>',
        'Date': 'Sun, 02 Feb 2020 16:42:21 +0000 (UTC)'
    })

    assert not thread.date

    thread.try_add(head_message)
    thread.try_add(tail_message)

    assert thread.date == timezone('UTC').localize(datetime(2020, 2, 2, 15, 12, 3))

def test_thread_has_tags():
    thread = EmailThread()

    head_email = EmailMessage(RawMessage({
        'Subject': 'Test Subject',
        'From': 'test_email@server.com',
        'To': 'test_receiver@server.com, second_receiver@server.com',
        'Message-Id': '<42@>',
        'References': '',
        'Date': 'Sun, 02 Feb 2020 15:12:03 +0000 (UTC)',
        'Payload': [
            Part('text/plain', 'this is a #regression')
        ]
    }))

    tail_email = EmailMessage(RawMessage({
        'Subject': 'Re: Test Subject',
        'From': 'test_email@server.com',
        'To': 'test_receiver@server.com, second_receiver@server.com',
        'Message-Id': '<1337@>',
        'References': '<42@>',
        'Date': 'Sun, 02 Feb 2020 16:42:21 +0000 (UTC)',
        'Payload': [
            Part('text/plain', '#hostdown')
        ]
    }))

    thread.try_add(head_email)
    thread.try_add(tail_email)

    assert thread.tags == set(['regression', 'hostdown'])


def test_email_scraper_success():
    query = None

    def fake_search(_query):
        nonlocal query
        query = _query
        return [
            EmailMessage({
                'Subject': 'Critical: Test Subject',
                'From': 'test_email@server.com',
                'To': 'test_receiver@server.com, second_receiver@server.com',
                'Message-Id': '<42@>',
                'References': '',
                'Date': 'Sun, 02 Feb 2020 00:42:00 -0800 (PST)'
            }),
            EmailMessage({
                'Subject': 'Re: Critical: Other Test Subject',
                'From': 'test_email@server.com',
                'To': 'test_receiver@server.com, second_receiver@server.com',
                'Message-Id': '<44@>',
                'References': '<22@>',
                'Date': 'Sun, 02 Feb 2020 00:44:00 -0800 (PST)'
            }),
            EmailMessage({
                'Subject': 'Critical: Other Test Subject',
                'From': 'test_email@server.com',
                'To': 'test_receiver@server.com, second_receiver@server.com',
                'Message-Id': '<22@>',
                'References': '',
                'Date': 'Sun, 02 Feb 2020 00:22:00 -0800 (PST)'
            }),
            EmailMessage({
                'Subject': 'Re: Critical: Other Subject',
                'From': 'test_email@server.com',
                'To': 'test_receiver@server.com, second_receiver@server.com',
                'Message-Id': '<21@>',
                'References': '<4242@>',
                'Date': 'Sun, 02 Feb 2020 06:30:00 -0800 (PST)'
            }),
            EmailMessage({
                'Subject': 'Re: Critical: Test Subject',
                'From': 'test_email@server.com',
                'To': 'test_receiver@server.com, second_receiver@server.com',
                'Message-Id': '<1337@>',
                'References': '<42@>',
                'Date': 'Sun, 02 Feb 2020 13:37:00 -0800 (PST)'
            }),
        ]

    client = mock.MagicMock()
    client.set_mailbox.return_value = None
    client.search = fake_search

    scraper = EmailScraper(client)
    pst = timezone('America/Los_Angeles')

    threads, orphans = scraper.scrape(
        'INBOX',
        'Critical: ',
        pst.localize(datetime(2020, 2, 2, 0, 0, 0)),
        pst.localize(datetime(2020, 2, 2, 14, 0, 0)),
    )

    assert query == '(SINCE 01-Feb-2020) (BEFORE 02-Feb-2020) (SUBJECT "Critical: ")'
    assert len(threads) == 2
    assert len(threads['Critical: Test Subject']) == 1
    assert len(threads['Critical: Test Subject'][0]) == 2
    assert threads['Critical: Test Subject'][0].first.message_id == '<42@>'
    assert threads['Critical: Test Subject'][0].has_message_id('<1337@>')

    assert len(threads['Critical: Other Test Subject']) == 1
    assert len(threads['Critical: Other Test Subject'][0]) == 2
    assert threads['Critical: Other Test Subject'][0].first.message_id == '<22@>'
    assert threads['Critical: Other Test Subject'][0].has('<44@>')

    assert orphans[0].message_id == '<21@>'


def test_email_scraper_fail():

    def fake_search(_query):
        return []

    client = mock.MagicMock()
    client.set_mailbox.return_value = None
    client.search = fake_search

    scraper = EmailScraper(client)
    pst = timezone('America/Los_Angeles')

    with raises(EmailLogicError) as err:
        scraper.scrape(
            'INBOX',
            'Critical: ',
            pst.localize(datetime(2020, 2, 2, 0, 0, 0)),
            pst.localize(datetime(2020, 2, 1, 14, 0, 0)),
        )

    assert str(err.value) == 'Stop must be after Start'
