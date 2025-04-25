# Kyler Olsen
# CS 2450 Final Project
# Apr 2025

from __future__ import annotations
from typing import TYPE_CHECKING
import struct

if TYPE_CHECKING:
    from socket import socket

def pack_varint(data: int) -> bytes:
    ordinal = b''
    while True:
        byte = data & 0x7F
        data >>= 7
        ordinal += struct.pack('B', byte | (0x80 if data > 0 else 0))
        if data == 0:
            break
    return ordinal

def unpack_varint(conn: socket) -> int:
    data = 0
    for i in range(5):
        ordinal = conn.recv(1)
        if len(ordinal) == 0:
            break
        byte = ord(ordinal)
        data |= (byte & 0x7F) << 7*i
        if not byte & 0x80:
            break
    return data

def pack_string(text: str) -> bytes:
    utf = text.encode('utf-8')
    data = pack_varint(len(utf))
    data += utf
    return data

def unpack_string(conn: socket) -> str:
    length = unpack_varint(conn)
    data = conn.recv(length)
    text = data.decode('utf-8')
    return text

def pack_varint_array(array: list[int]) -> bytes:
    data = pack_varint(len(array))
    for i in array:
        data += pack_varint(i)
    return data

def unpack_varint_array(conn: socket) -> list[int]:
    length = unpack_varint(conn)
    array: list[int] = []
    for _ in range(length):
        array.append(unpack_varint(conn))
    return array

def pack_string_array(array: list[str]) -> bytes:
    data = pack_varint(len(array))
    for i in array:
        data += pack_string(i)
    return data

def unpack_string_array(conn: socket) -> list[str]:
    length = unpack_varint(conn)
    array: list[str] = []
    for _ in range(length):
        array.append(unpack_string(conn))
    return array
