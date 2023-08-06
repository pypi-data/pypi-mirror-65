Daemon Protocol
===============

KeePass Shell implements IPC based on Unix Domain Sockets stream connection
(AF_UNIX, SOCK_STREAM) between kpsh acting as a server and any client which
understands its underlying binary protocol. kpsh handles only one connection at
a time and clients decide when they disconnect. When one client is handled,
other connections are accepted and then immediately closed, without reading any
input.

kpsh starts listening for connections when it's started with `-d` switch. 

kpsh and clients exchange the following binary messages:

    MSG := <TEXT_LEN:4 bytes><TEXT>

First, 4-byte integer with a message length is transmitted and then the message
itself, which is a byte stream of encoded string.

Please note that `TEXT_LEN` contains length of binary form of string, i.e. a
number of transmitted bytes, not a number of letters. These might be the same
numbers for some encodings (e.g. ASCII), but Unicode strings typically contain
also multi-byte glyphs.

kpsh accepts any command typically available in its interactive sessions. It
will respond with a series of messages of the following form:

    RESP := <TYPE><SPACE><TEXT>
    RESP := OK

`TYPE` is one of the following:

- `M`: ordinary message (e.g. stdout)
- `E`: error message (e.g. stderr)
- `P`: prompt; client should prompt user for additional input
- `PS`: prompt secure; same as prompt, but client is advised to obtain user 
  input securely. Usually it's a password which shouldn't be displayed when user
  types it

After each command kpsh sends additionally "OK" message to indicate to the
clients that command won't output anything else.

Typical session (for simplicity we'll skip the header, i.e. first 4 bytes with
message length):

    (client connects)
    C: unlock
    S: PS Password:
    C: super difficult password chosen by user
    S: OK
    C: show example-account -n
    S: M example-account
    S: M some username
    S: M some password
    S: M https://example.com/login
    S: M note note note
    S: OK
    C: show blablabla
    S: E entry not found: blablabla
    C: exit
    S: OK
    (server closes connection)

Example client implementation is available in `contrib/kpsh-client` script.
