# interfaces/renderer_interface.py

from abc import ABC, abstractmethod
from typing import Optional
from interfaces.view_model_interface import IViewModel


from dataclasses import dataclass, field
from typing import Optional

@dataclass(frozen=True)
class RenderResult:
    body: str = ""
    status_code: int = 200
    headers: dict = field(default_factory=dict)
    redirect_to: Optional[str] = None



class IRenderer(ABC):
    @abstractmethod
    def render(self, viewmodel: IViewModel, template_name: Optional[str] = None) -> RenderResult:
        pass
