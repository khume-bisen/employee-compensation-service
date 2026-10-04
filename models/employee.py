from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Employee:
    employee_id: Optional[int]
    first_name: str
    last_name: str
    department_id: int
    salary: float
    bonus: Optional[float]
    hire_date: date
