# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

CONST = 0x713E66EB
ADD = 0x71BD
DEFAULT_ENCODING = "cp932"


def is_cp932_lead(c: int) -> bool:
    return (0x81 <= c <= 0x9F) or (0xE0 <= c <= 0xFC)


def lower_cp932_path_bytes(bs: bytes) -> bytes:
    out = bytearray()
    i = 0
    while i < len(bs):
        c = bs[i]
        if is_cp932_lead(c):
            out.append(c)
            if i + 1 < len(bs):
                out.append(bs[i + 1])
                i += 2
            else:
                i += 1
        else:
            out.append(c + 0x20 if 0x41 <= c <= 0x5A else c)
            i += 1
    return bytes(out)


def derive_dacz_key(name: str, byte_size: int, encoding: str = DEFAULT_ENCODING) -> int:
    bs = name.encode(encoding, errors="strict")
    for sep in (b"/", b"\\"):
        if sep in bs:
            bs = bs.rsplit(sep, 1)[1]
    if b"?" in bs:
        bs = bs.split(b"?", 1)[0]
    bs = lower_cp932_path_bytes(bs)
    if bs.endswith(b"z"):
        bs = bs[:-1]
    acc = 0
    for c in reversed(bs):
        signed_c = c if c < 0x80 else c - 0x100
        term = (((signed_c + byte_size) & 0xFFFFFFFF) * CONST) & 0xFFFFFFFF
        acc = (acc + term + ADD) & 0xFFFFFFFF
    return acc & 0xFF


def decrypt_dacz(data: bytes, key: int, start_offset: int = 0) -> bytes:
    out = bytearray(len(data))
    state = (((start_offset & 0xFFFFFFFF) * CONST) + ADD) & 0xFFFFFFFF
    for i, b in enumerate(data):
        stream = (((state >> 8) & 0xFF) + (state & 0xFF)) & 0xFF
        out[i] = ((b ^ stream) - key) & 0xFF
        state = (state + CONST) & 0xFFFFFFFF
    return bytes(out)


def encrypt_dacz(decoded: bytes, key: int, start_offset: int = 0) -> bytes:
    out = bytearray(len(decoded))
    state = (((start_offset & 0xFFFFFFFF) * CONST) + ADD) & 0xFFFFFFFF
    for i, b in enumerate(decoded):
        stream = (((state >> 8) & 0xFF) + (state & 0xFF)) & 0xFF
        out[i] = ((b + key) & 0xFF) ^ stream
        state = (state + CONST) & 0xFFFFFFFF
    return bytes(out)


def decoded_name_for(src_name: str) -> str:
    lower = src_name.lower()
    if lower.endswith(".dacz") or lower.endswith(".iniz"):
        return src_name[:-1]
    return src_name + ".decoded"


def encoded_name_for(decoded_name: str) -> str:
    lower = decoded_name.lower()
    if lower.endswith(".dac") or lower.endswith(".ini"):
        return decoded_name + "z"
    return decoded_name


def decode_file(path: Path, out_path: Path | None = None, encoding: str = DEFAULT_ENCODING) -> bytes:
    enc = path.read_bytes()
    key = derive_dacz_key(path.name, len(enc), encoding)
    dec = decrypt_dacz(enc, key)
    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(dec)
    return dec


def encode_file(decoded_path: Path, output_path: Path, source_encrypted_name: str | None = None, encoding: str = DEFAULT_ENCODING) -> bytes:
    dec = decoded_path.read_bytes()
    name = source_encrypted_name or output_path.name
    key = derive_dacz_key(name, len(dec), encoding)
    enc = encrypt_dacz(dec, key)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(enc)
    return enc
