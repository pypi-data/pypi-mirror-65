# Standard Library
from mailbox import MH

# Third Party Stuff
from django_mailbox.transports.generic import GenericFileMailbox


class MHTransport(GenericFileMailbox):
    _variant = MH
