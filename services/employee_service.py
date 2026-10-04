from typing import List, Optional

from models.employee import Employee
from repositories.employee_repository import EmployeeRepository


class EmployeeService:

    def __init__(self):
        self.repository = EmployeeRepository()

    def get_all_employees(self) -> List[Employee]:
        return self.repository.get_all()

    def get_employee(self, employee_id: int) -> Optional[Employee]:
        if employee_id <= 0:
            raise ValueError("Employee ID must be greater than 0")

        return self.repository.get_by_id(employee_id)

    def get_employees_by_department(self, department_id: int) -> List[Employee]:
        if department_id <= 0:
            raise ValueError("Department ID must be greater than 0")

        return self.repository.get_by_department(department_id)

    def create_employee(self, employee: Employee) -> Employee:
        self._validate_employee(employee)

        return self.repository.create(employee)

    def update_employee(self, employee: Employee) -> Optional[Employee]:
        if employee.employee_id is None or employee.employee_id <= 0:
            raise ValueError("Employee ID must be greater than 0")

        self._validate_employee(employee)

        return self.repository.update(employee)

    def delete_employee(self, employee_id: int) -> bool:
        if employee_id <= 0:
            raise ValueError("Employee ID must be greater than 0")

        return self.repository.delete(employee_id)

    def _validate_employee(self, employee: Employee) -> None:
        if not employee.first_name or not employee.first_name.strip():
            raise ValueError("First name is required")

        if not employee.last_name or not employee.last_name.strip():
            raise ValueError("Last name is required")

        if employee.department_id <= 0:
            raise ValueError("Department ID must be greater than 0")

        if employee.salary < 0:
            raise ValueError("Salary cannot be negative")

        if employee.bonus is not None and employee.bonus < 0:
            raise ValueError("Bonus cannot be negative")

        if employee.hire_date is None:
            raise ValueError("Hire date is required")
