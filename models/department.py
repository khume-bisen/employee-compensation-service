from dataclasses import dataclass
from typing import Optional


@dataclass
class Department:
    department_id: int
    department_name: str
    location: Optional[str]
