#!/usr/bin/env python3
"""Save original exports from Grok Build's streaming-json protocol, not LLM text.

No network, credentials, model calls, transcript persistence or code execution.
Only completed Graffalo read_export tool results for the explicit document qualify.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import sys


def require(ok, message):
    if not ok:
        raise ValueError(message)


def save(stream, destination, document_id):
    files, consumed = {}, 0
    while True:
        line = stream.readline(8_000_001)
        if not line:
            break
        consumed += len(line)
        require(len(line) <= 8_000_000 and consumed <= 128_000_000,
                "Stream exceeds safety limit")
        event = json.loads(line)
        require(isinstance(event, dict), "Invalid protocol event")
        if event.get("type") != "tool_call_update" or event.get("status") != "completed":
            continue
        result = event.get("rawOutput")
        if not isinstance(result, dict) or result.get("type") != "MCP":
            continue
        if result.get("server_name") != "graffalo" or result.get("tool_name") != "read_export":
            continue
        output = result.get("output")
        require(isinstance(output, dict), "Invalid tool result")
        raw = output.get("OkayOutput")
        require(isinstance(raw, str), "Unsupported Grok tool result; no file saved")
        chunk = json.loads(raw)
        require(isinstance(chunk, dict), "Invalid chunk result")
        require(chunk.get("document_id") == document_id, "Export belongs to a different document")
        sha, total = chunk.get("sha256"), chunk.get("bytes")
        require(isinstance(sha, str) and re.fullmatch(r"[a-f0-9]{64}", sha), "Invalid file digest")
        require(type(total) is int and 0 < total <= 3_000_000, "Invalid file size")
        mime = chunk.get("mimeType")
        require(mime in ("image/png", "application/pdf"), "Unsupported export format")
        require(chunk.get("encoding") == "base64", "Unsupported chunk encoding")
        data = base64.b64decode(chunk["data_base64"], validate=True)
        offset = chunk.get("offset")
        require(type(offset) is int and 0 <= offset < total, "Invalid chunk offset")
        end = offset + len(data)
        require(0 < len(data) <= 65536 and len(data) == chunk.get("chunk_bytes") and end <= total,
                "Invalid chunk size")
        require(hashlib.sha256(data).hexdigest() == chunk.get("chunk_sha256"), "Chunk digest mismatch")
        require(chunk.get("eof") is (end == total), "Invalid end-of-file flag")
        require(chunk.get("next_offset") == (None if end == total else end), "Invalid next offset")
        identity = (sha, total, mime, chunk.get("resource_uri"), chunk.get("revision"),
                    chunk.get("width"), chunk.get("height"))
        file = files.setdefault(sha, {"identity": identity, "chunks": {}, "receipt": chunk})
        require(len(files) <= 8 and file["identity"] == identity, "Inconsistent export receipt")
        old = file["chunks"].get(offset)
        require(old is None or old == data, "Conflicting repeated chunk")
        file["chunks"][offset] = data
    require(files, "No original Graffalo export tool results found")
    ready = []
    for sha, file in files.items():
        data = bytearray()
        for offset, chunk in sorted(file["chunks"].items()):
            require(offset == len(data), "Missing or overlapping export chunks")
            data.extend(chunk)
        receipt = file["receipt"]
        require(len(data) == receipt["bytes"] and hashlib.sha256(data).hexdigest() == sha,
                "Incomplete export or whole-file digest mismatch")
        png = receipt["mimeType"] == "image/png"
        if png:
            require(len(data) >= 24 and data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR",
                    "Invalid PNG header")
            require(struct.unpack(">II", data[16:24]) == (receipt.get("width"), receipt.get("height")),
                    "PNG dimensions do not match receipt")
        else:
            require(data.startswith(b"%PDF-") and data.rstrip().endswith(b"%%EOF"), "Invalid PDF signature")
        # Never use a model/server-provided filename as a filesystem path.
        ready.append((f"graffalo-{sha}.{'png' if png else 'pdf'}", data, sha))
    destination = Path(destination)
    require(not destination.is_symlink(), "Output directory cannot be a symlink")
    destination.mkdir(mode=0o700, parents=True, exist_ok=True)
    for name, data, sha in ready:
        path = destination / name
        # Exclusive creation also rejects existing files and symlinks.
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as output:
            output.write(data)
        print(json.dumps({"file": str(path), "bytes": len(data), "sha256": sha, "verified": True}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--document-id", required=True)
    parser.add_argument("--output", required=True, help="Directory for verified original files")
    args = parser.parse_args()
    try:
        save(sys.stdin.buffer, args.output, args.document_id)
    except (ValueError, KeyError, TypeError, OSError):
        # Never echo raw input, tool content, account data or base64 in errors.
        print("Export not saved: invalid/incomplete tool bytes or output path. Keep the original tool results; do not transcribe or repair base64.", file=sys.stderr)
        sys.exit(1)
