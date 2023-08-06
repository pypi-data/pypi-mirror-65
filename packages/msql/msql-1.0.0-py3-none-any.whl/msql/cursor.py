from typing import Any, List, Tuple
from typing_extensions import Protocol


class Cursor(Protocol):

    def execute(self, statement: str, *args: Any, **kwargs: Any) -> None:
        ...

    def fetchone(self) -> Tuple:
        ...

    def fetchall(self) -> List[Tuple]:
        ...
