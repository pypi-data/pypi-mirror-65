.. image:: https://travis-ci.org/panttojo/django-mailbox-dynamic.png?branch=master
   :target: https://travis-ci.org/panttojo/django-mailbox-dynamic

.. image:: https://badge.fury.io/py/django-mailbox-dynamic.png
    :target: http://badge.fury.io/py/django-mailbox-dynamic

.. image:: https://pypip.in/d/django-mailbox-dynamic/badge.png
    :target: https://pypi.python.org/pypi/django-mailbox-dynamic


Easily ingest messages from POP3, IMAP, or local mailboxes into your Django application.

This app allows you to either ingest e-mail content from common e-mail services (as long as the service provides POP3 or IMAP support),
or directly receive e-mail messages from ``stdin`` (for locally processing messages from Postfix or Exim4).

These ingested messages will be stored in the database in Django models and you can process their content at will,
or -- if you're in a hurry -- by using a signal receiver.

### Important
This a forked project from `Github <http://github.com/panttojo/django-mailbox>`_ for make custom changes.


- Documentation for django-mailbox is available on
  `ReadTheDocs <http://django-mailbox.readthedocs.org/>`_.
- Please post issues on
  `Github <http://github.com/panttojo/django-mailbox-dynamic/issues>`_.
- Test status available on
  `Travis-CI <https://travis-ci.org/panttojo/django-mailbox-dynamic>`_.
