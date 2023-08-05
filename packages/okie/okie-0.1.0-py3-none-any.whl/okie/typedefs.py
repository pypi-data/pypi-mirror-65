from typing import Tuple, Dict
import asyncio

from .types import header_key


AsyncioStreamType = Tuple[asyncio.StreamReader, asyncio.StreamWriter]
AsyncioStreamType.__doc__ = """
todo
"""

Headers = Dict[header_key, str]
Headers.__doc__ = """
todo
"""
