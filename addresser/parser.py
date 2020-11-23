import re


class Address(object):
    """
    Represent an Address with a street and a house number
    """

    def __init__(self, street: str, number: str, src: str = None):
        """
        Constructor for Address

        Args:
            street(str): the street address
            number(str): the house number
            src(str): the original address string
        """
        self.street = street
        self.number = number
        self.src = src

    def __str__(self) -> str:
        return f"street:{self.street};number:{self.number}"


# Compile regexp before ues

# check for house numbers at the beginning of an address string
re_num_at_begin = re.compile(r"^\s*(no\.?)?\s*(\d+[a-z]*)(\/\d+[a-z]*)?\s*", re.IGNORECASE)
# check for house numbers at the end of an address string
re_num_at_end = re.compile(r"((no|д)\.?)?\s*(\d+\s*[a-z]*)(\/\d+[a-z]*)?\s*$", re.IGNORECASE)
# matches a commat at the beginning or end of the input
re_clean = re.compile(r"^,|,$")
# matches references to apartments
re_normalize = re.compile(r"(suite|apt\.?|appartamento|piso|к\.?)\s+\d+", re.IGNORECASE)


def _clean(data: str) -> str:
    """
    Remove trailing spaces and commas

    Args:
        data(str): the data to clean
    """
    return re_clean.sub("", data.strip()).strip()


def _normalize(src: str) -> str:
    """
    Normalize address string:

    - Remove trailing spaces
    - Remove parts that have to do with an apartment identifier

    Args:
        src(str): the string to normalize
    Returns:
        the normalized string
    """
    return re_normalize.sub("", src).strip()


def parse(address: str) -> Address:
    """
    Parse an string representing a an address to a structured
    Address object with the street name separated by the house number

    Args:
        address(str): the address to start
    Returns:
        an Address object parsed from the string input
    """
    if address is None:
        raise ValueError("None value not allowed")
    # simple approach
    # the house number is either at the beginning or in the end
    src = _normalize(address)
    # by default set street name as the address and empty house number
    st, hn = (src, "")
    # if it starts with a number then that's our street number:
    m = re_num_at_begin.search(src)
    if m is not None:
        s, e = m.span()  # read match coordinates
        hn = _clean(src[s:e])
        st = _clean(src[e:])
        return Address(st, hn, src)
    # if it is in the end then there we go
    m = re_num_at_end.search(src)
    if m is not None:
        s, e = m.span()  # read match coordinates
        hn = _clean(src[s:e])
        st = _clean(src[:s])
        return Address(st, hn, src)
    # if we got here it means that aither there is no house number or
    # we are unable to identify it. As a fallback lets return the complete string
    return Address(st, hn, src)
