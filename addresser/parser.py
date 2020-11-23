import time
import json


class Address(object):
    """
    Represent an Address with a street and a house number
    """

    def __init__(self, street: str, number: str):
        """
        Constructor for Address

        Args:
            street(str): the street address
            number(str): the house number
        """
        self.street = street
        self.number = number

    def __str__(self) -> str:
        return json.dumps(self)


def parse(address: str) -> Address:
    """
    Process the dataset csv input to a json optimized
    for the rest API to serve

    Args:
        address(str): the address to start
    Returns:
        an Address object parsed from the string input
    """
    # track the execution time
    start = time.time()

    print(f"Completed in {time.time() - start}")
