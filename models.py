from dataclasses import  dataclass

@dataclass
class Game:
    url: str
    name: str
    year: str
    rating: str

@dataclass
class Tag:
    slug: str
    name: str

@dataclass
class Platform:
    code: str
    title: str