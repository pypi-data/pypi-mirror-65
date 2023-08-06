# Standard Library
from mailbox import MMDF

# Third Party Stuff
from django_mailbox.transports.generic import GenericFileMailbox


class MMDFTransport(GenericFileMailbox):
    _variant = MMDF
