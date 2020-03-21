"""
Data Stuctures for cinemas and their attributes
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from dataclasses_json import dataclass_json


@dataclass
class Address:
    """ A physical address """
    street: str = ''
    postal_code: str = ''
    district: str = ''
    city: str = ''
    country: str = ''


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


@dataclass_json
@dataclass
class Cinema:
    """ A cinema with shows """
    name: str
    description: str = ''
    address: Address = field(default_factory=Address)
    contact: Contact = field(default_factory=Contact)
    prices: List[str] = field(default_factory=list)
    shows: List[Show] = field(default_factory=list)


@dataclass_json
@dataclass
class CinemaMovie:
    """ a cinema name with times for one of its movies """
    name: str
    movie: str
    times: List[datetime] = field(default_factory=list)
