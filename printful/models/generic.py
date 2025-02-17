from typing import List, Dict


class Result:
    def __init__(self, status_code: int, message: str = "", data: List[Dict] = None):
        """
        Result returned from low-level RestAdapter
        :param status_code: Standard HTTP Status code
        :param message: Human readable result
        :param data: Python List of Dictionaries (or maybe just a single Dictionary on error)
        """
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []


class Paging:
    total: int
    offset: int
    limit: int

    def __init__(self, total: int, offset: int, limit: int) -> None:
        self.total = total
        self.offset = offset
        self.limit = limit


class Link:
    href: str

    def __init__(self, href: str) -> None:
        self.href = href
