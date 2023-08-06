from dataclasses import dataclass


@dataclass
class FlakeError:
    line: int
    column: int
    message: str
