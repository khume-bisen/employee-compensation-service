import pytest
from datetime import date

from models.employee import Employee
from services.employee_service import EmployeeService


def make_valid_employee():
    return Employee(
        employee_id=None,
        first_name="Test",
        last_name="Employee",
        department_id=1,
        salary=500000,
        bonus=50000,
        hire_date=date(2024, 1, 1),
    )


def test_valid_employee_passes_validation():
    service = EmployeeService()
    employee = make_valid_employee()

    service._validate_employee(employee)


def test_empty_first_name_is_rejected():
    service = EmployeeService()
    employee = make_valid_employee()
    employee.first_name = ""

    with pytest.raises(ValueError, match="First name is required"):
        service._validate_employee(employee)


def test_negative_salary_is_rejected():
    service = EmployeeService()
    employee = make_valid_employee()
    employee.salary = -1

    with pytest.raises(ValueError, match="Salary cannot be negative"):
        service._validate_employee(employee)


def test_negative_bonus_is_rejected():
    service = EmployeeService()
    employee = make_valid_employee()
    employee.bonus = -1

    with pytest.raises(ValueError, match="Bonus cannot be negative"):
        service._validate_employee(employee)


def test_zero_department_id_is_rejected():
    service = EmployeeService()
    employee = make_valid_employee()
    employee.department_id = 0

    with pytest.raises(ValueError, match="Department ID must be greater than 0"):
        service._validate_employee(employee)


def test_missing_hire_date_is_rejected():
    service = EmployeeService()
    employee = make_valid_employee()
    employee.hire_date = None

    with pytest.raises(ValueError, match="Hire date is required"):
        service._validate_employee(employee)
