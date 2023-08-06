from ._named import NamedEnum, named


class HttpRequestType(NamedEnum):
    """
    Enumeration containing common HTTP request described in
    [HTTP methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
    """

    GET = named()
    """
    The GET method requests a representation of the specified resource. Requests using GET should only retrieve data.
    """

    HEAD = named()
    """
    The HEAD method asks for a response identical to that of a GET request, but without the response body.
    """

    POST = named()
    """
    The POST method is used to submit an entity to the specified resource, often causing a change in state or side effects on the server.
    """

    PUT = named()
    """
    The POST method is used to submit an entity to the specified resource, often causing a change in state or side effects on the server.
    """

    DELETE = named()
    """
    The DELETE method deletes the specified resource.
    """

    CONNECT = named()
    """
    The CONNECT method establishes a tunnel to the server identified by the target resource.
    """

    OPTIONS = named()
    """
    The OPTIONS method is used to describe the communication options for the target resource.
    """

    TRACE = named()
    """
    The TRACE method performs a message loop-back test along the path to the target resource.
    """

    PATCH = named()
    """
    The PATCH method is used to apply partial modifications to a resource.
    """
