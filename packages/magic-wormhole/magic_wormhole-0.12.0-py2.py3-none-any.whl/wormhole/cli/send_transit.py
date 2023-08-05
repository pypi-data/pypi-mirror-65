from __future__ import print_function, unicode_literals
import hashlib
from tqdm import tqdm
from twisted.internet.defer import inlineCallbacks
from twisted.protocols import basic
from ..errors import TransferError
from ..util import bytes_to_dict, bytes_to_hexstr

@inlineCallbacks
def send_file(transit_sender, fd_to_send, timing, stderr, hide_progress):
    ts = transit_sender

    fd_to_send.seek(0, 2)
    filesize = fd_to_send.tell()
    fd_to_send.seek(0, 0)

    record_pipe = yield ts.connect()
    timing.add("transit connected")
    # record_pipe should implement IConsumer, chunks are just records
    print(u"Sending (%s).." % record_pipe.describe(), file=stderr)

    hasher = hashlib.sha256()
    progress = tqdm(
        file=stderr,
        disable=hide_progress,
        unit="B",
        unit_scale=True,
        total=filesize)

    def _count_and_hash(data):
        hasher.update(data)
        progress.update(len(data))
        return data

    fs = basic.FileSender()

    with timing.add("tx file"):
        with progress:
            if filesize:
                # don't send zero-length files
                yield fs.beginFileTransfer(
                    fd_to_send,
                    record_pipe,
                    transform=_count_and_hash)

    expected_hash = hasher.digest()
    expected_hex = bytes_to_hexstr(expected_hash)
    print(u"File sent.. waiting for confirmation", file=stderr)
    with timing.add("get ack") as t:
        ack_bytes = yield record_pipe.receive_record()
        record_pipe.close()
        ack = bytes_to_dict(ack_bytes)
        ok = ack.get(u"ack", u"")
        if ok != u"ok":
            t.detail(ack="failed")
            raise TransferError("Transfer failed (remote says: %r)" % ack)
        if u"sha256" in ack:
            if ack[u"sha256"] != expected_hex:
                t.detail(datahash="failed")
                raise TransferError("Transfer failed (bad remote hash)")
        print(u"Confirmation received. Transfer complete.", file=stderr)
        t.detail(ack="ok")
