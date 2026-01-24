from dataclasses import dataclass


@dataclass
class Package:
    name: str
    epoch: int
    version: str
    release: str
    arch: str
    buildtime: int
    source: str
