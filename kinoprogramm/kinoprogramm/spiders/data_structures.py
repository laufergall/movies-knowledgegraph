
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Address:
    """ A physical adress """
    street: str
    postal_code: int
    district: str
    city: str
    country: str


@dataclass
class Contact:
    """ means of contact """
    telephone: str = ''
    email: str = ''


@dataclass
class Show:
    """ A (movie) show in a cinema """
    title: str
    times: List[datetime] = field(default_factory=list)


class Cinema:
    """ A cinema with shows """
    name: str
    description: str
    address: Address
    contact: Contact
    prices: List[str]
    shows: List[Show]
