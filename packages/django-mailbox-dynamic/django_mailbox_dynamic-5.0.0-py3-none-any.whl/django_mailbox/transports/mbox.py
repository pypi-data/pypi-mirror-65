# Standard Library
from mailbox import mbox

# Third Party Stuff
from django_mailbox.transports.generic import GenericFileMailbox


class MboxTransport(GenericFileMailbox):
    _variant = mbox
