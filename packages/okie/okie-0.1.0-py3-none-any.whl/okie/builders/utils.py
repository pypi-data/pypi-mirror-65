from ..typedefs import Headers


def encode_headers(headers: Headers):
    return b"\r\n".join(
        b"%b: %b" % (k.encode(), v.encode())
        for k, v in headers.items()
    )
