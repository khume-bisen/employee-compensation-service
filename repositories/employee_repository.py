from typing import List, Optional
from models.employee import Employee
from utils.db import get_connection


class EmployeeRepository:

    def get_all(self) -> List[Employee]:
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    EmployeeID,
                    FirstName,
                    LastName,
                    DepartmentID,
                    Salary,
                    Bonus,
                    HireDate
                FROM Employee
                ORDER BY EmployeeID
            """)

            rows = cursor.fetchall()

            return [
                Employee(
                    employee_id=row.EmployeeID,
                    first_name=row.FirstName,
                    last_name=row.LastName,
                    department_id=row.DepartmentID,
                    salary=float(row.Salary),
                    bonus=float(row.Bonus) if row.Bonus is not None else None,
                    hire_date=row.HireDate
                )
                for row in rows
            ]

        finally:
            connection.close()

    def get_by_id(self, employee_id: int) -> Optional[Employee]:
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    EmployeeID,
                    FirstName,
                    LastName,
                    DepartmentID,
                    Salary,
                    Bonus,
                    HireDate
                FROM Employee
                WHERE EmployeeID = ?
            """, employee_id)

            row = cursor.fetchone()

            if row is None:
                return None

            return Employee(
                employee_id=row.EmployeeID,
                first_name=row.FirstName,
                last_name=row.LastName,
                department_id=row.DepartmentID,
                salary=float(row.Salary),
                bonus=float(row.Bonus) if row.Bonus is not None else None,
                hire_date=row.HireDate
            )

        finally:
            connection.close()

    def get_by_department(self, department_id: int) -> List[Employee]:
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    EmployeeID,
                    FirstName,
                    LastName,
                    DepartmentID,
                    Salary,
                    Bonus,
                    HireDate
                FROM Employee
                WHERE DepartmentID = ?
                ORDER BY EmployeeID
            """, department_id)

            rows = cursor.fetchall()

            return [
                Employee(
                    employee_id=row.EmployeeID,
                    first_name=row.FirstName,
                    last_name=row.LastName,
                    department_id=row.DepartmentID,
                    salary=float(row.Salary),
                    bonus=float(row.Bonus) if row.Bonus is not None else None,
                    hire_date=row.HireDate
                )
                for row in rows
            ]

        finally:
            connection.close()

    def create(self, employee: Employee) -> Employee:
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO Employee
                    (FirstName, LastName, DepartmentID, Salary, Bonus, HireDate)
                OUTPUT INSERTED.EmployeeID
                VALUES (?, ?, ?, ?, ?, ?)
            """,
            employee.first_name,
            employee.last_name,
            employee.department_id,
            employee.salary,
            employee.bonus,
            employee.hire_date)

            employee_id = cursor.fetchone()[0]

            connection.commit()

            employee.employee_id = employee_id

            return employee

        finally:
            connection.close()

    def update(self, employee: Employee) -> Optional[Employee]:
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE Employee
                SET
                    FirstName = ?,
                    LastName = ?,
                    DepartmentID = ?,
                    Salary = ?,
                    Bonus = ?,
                    HireDate = ?
                WHERE EmployeeID = ?
            """,
            employee.first_name,
            employee.last_name,
            employee.department_id,
            employee.salary,
            employee.bonus,
            employee.hire_date,
            employee.employee_id)

            if cursor.rowcount == 0:
                connection.rollback()
                return None

            connection.commit()

            return self.get_by_id(employee.employee_id)

        finally:
            connection.close()

    def delete(self, employee_id: int) -> bool:
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM Employee
                WHERE EmployeeID = ?
            """, employee_id)

            if cursor.rowcount == 0:
                connection.rollback()
                return False

            connection.commit()

            return True

        finally:
            connection.close()
