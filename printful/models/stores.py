from typing import List, Dict
from .generic import Link, Paging

# https://developers.printful.com/docs/v2-beta/#tag/Stores-v2
# GET https://api.printful.com/v2/stores
# GET https://api.printful.com/v2/stores/{store_id}
# TODO: GET https://api.printful.com/v2/stores/{store_id}/statistics


class Store:
    """
    Class representing a Store
    API Endpoint: GET https://api.printful.com/v2/stores/{store_id}

    :param id: Store ID number
    :type id: int
    :param type: Printful type of store
    :type type: str
    :param name: Name
    :type name: str
    """

    id: int
    type: str
    name: str

    def __init__(self, id: int, type: str, name: str):
        """
        Constructor
        """
        self.id = id
        self.type = type
        self.name = name


class StoreList:
    """
    Class reprenting a list of stores with paging info and links to more requests
    API Endpoint: GET https://api.printful.com/v2/stores

    :param data: List of stores
    :type data: List[Store]
    :param _links: links to more queries
    :type _links: Dict[str, Link]
    :param paging: page information
    :type paging: Paging
    :param extra: unknown extra data not defined in spec
    :type extra: List[str]
    """

    data: List[Store]
    _links: Dict[str, Link]
    paging: Paging
    extra: List[str]

    def __init__(
        self,
        data: List[Store],
        _links: Dict[str, Link],
        paging: Paging,
        extra: List[str],
    ):
        """
        Constructor
        """
        self.data = data
        self._links = _links
        self.paging = paging
        self.extra = extra
