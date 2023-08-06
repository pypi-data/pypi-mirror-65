import enum
import socket
from .. import schema


class Cmd(enum.IntEnum):
    connect = 1
    bind = 2


class Rep(enum.IntEnum):
    granted = 0x5A
    rejected = 0x5B
    un_reachable = 0x5C
    auth_failed = 0x5D


class ClientRequest(schema.BinarySchema):
    ver = schema.MustEqual(schema.uint8, 4)
    cmd = schema.SizedIntEnum(schema.uint8, Cmd)
    dst_port = schema.uint16be
    dst_ip = schema.Convert(
        schema.Bytes(4), encode=socket.inet_aton, decode=socket.inet_ntoa
    )
    user_id = schema.EndWith(b"\x00")


class Response(schema.BinarySchema):
    vn = schema.Bytes(1)
    rep = schema.SizedIntEnum(schema.uint8, Rep)
    dst_port = schema.uint16be
    dst_ip = schema.Convert(
        schema.Bytes(4), encode=socket.inet_aton, decode=socket.inet_ntoa
    )
