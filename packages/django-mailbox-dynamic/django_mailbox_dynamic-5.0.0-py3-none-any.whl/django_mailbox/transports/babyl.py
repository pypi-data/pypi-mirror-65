# Standard Library
from mailbox import Babyl

# Third Party Stuff
from django_mailbox.transports.generic import GenericFileMailbox


class BabylTransport(GenericFileMailbox):
    _variant = Babyl
