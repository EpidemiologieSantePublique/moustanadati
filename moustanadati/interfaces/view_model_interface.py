#interfaces/view_model_interface.py

from typing import Protocol

class IViewModel(Protocol):
    def to_dict(self) -> dict: ...
    redirect_to: str | None
    headers: dict