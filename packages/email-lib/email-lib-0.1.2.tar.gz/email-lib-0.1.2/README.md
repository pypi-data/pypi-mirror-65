# Email Lib

Simplify email organization

## Setup

### Installation

```
pip install email-lib
```

OR

```
$ python setup.py install
```

### Testing

```
$ python setup.py test
```

OR


```
$ pytest
```

### Usage

Simple example

```
$ cat main.py
from datetime import datetime
from email-lib.emails import EmailClient, EmailQueryBuilder, EmailOrganizer

def main():
    """
    Entry Point
    """
    client = EmailClient('mail.server.com', 'example@server.com', 'mYpAsSw0rD')
    client.login()
    client.set_mailbox('INBOX')

    query_builder = EmailQueryBuilder().start(datetime(2020, 2, 29)).stop(datetime(2020, 3, 1)).subject('CRITICAL :')

    results = client.search(query_builder.build())
    thread_subjects, orphans = EmailOrganizer(results).organize()
    for threads in thread_subjects.values():
        print(threads[0].subject)

if __name__ == "__main__":
    main()
$ python main.py
CRITICAL : Disk full
CRITICAL : Service sending 503
CRITICAL : Database shard not responding
$
```

## Contact

Send email to Pierre Wacrenier - pierre@wacrenier.me
