from typing import List, Dict, Any

from utils.db import get_connection


class ReportRepository:

    def get_total_bonus(self) -> float:
        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    COALESCE(SUM(Bonus), 0) AS TotalBonus
                FROM Employee
            """)

            result = cursor.fetchone()[0]
            return float(result)

        finally:
            connection.close()

    def get_employees_with_no_bonus(self) -> List[Dict[str, Any]]:
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
                    HireDate
                FROM Employee
                WHERE Bonus IS NULL
                ORDER BY EmployeeID
            """)

            rows = cursor.fetchall()

            return [
                {
                    "employee_id": row.EmployeeID,
                    "first_name": row.FirstName,
                    "last_name": row.LastName,
                    "department_id": row.DepartmentID,
                    "salary": float(row.Salary),
                    "hire_date": row.HireDate.isoformat()
                }
                for row in rows
            ]

        finally:
            connection.close()

    def get_bonus_percentage(self) -> List[Dict[str, Any]]:
        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    EmployeeID,
                    FirstName,
                    LastName,
                    Salary,
                    Bonus,
                    ROUND(
                        (Bonus * 100.0) / NULLIF(Salary, 0),
                        2
                    ) AS BonusPercentage
                FROM Employee
                WHERE Bonus IS NOT NULL
                ORDER BY EmployeeID
            """)

            rows = cursor.fetchall()

            return [
                {
                    "employee_id": row.EmployeeID,
                    "first_name": row.FirstName,
                    "last_name": row.LastName,
                    "salary": float(row.Salary),
                    "bonus": float(row.Bonus),
                    "bonus_percentage": float(row.BonusPercentage)
                }
                for row in rows
            ]

        finally:
            connection.close()

    def get_department_bonus(self) -> List[Dict[str, Any]]:
        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    d.DepartmentID,
                    d.DepartmentName,
                    SUM(COALESCE(e.Bonus, 0)) AS TotalBonus,
                    AVG(e.Salary) AS AverageSalary
                FROM Department d
                INNER JOIN Employee e
                    ON d.DepartmentID = e.DepartmentID
                GROUP BY
                    d.DepartmentID,
                    d.DepartmentName
                HAVING
                    SUM(COALESCE(e.Bonus, 0)) > AVG(e.Salary)
                ORDER BY d.DepartmentID
            """)

            rows = cursor.fetchall()

            return [
                {
                    "department_id": row.DepartmentID,
                    "department_name": row.DepartmentName,
                    "total_bonus": float(row.TotalBonus),
                    "average_salary": float(row.AverageSalary)
                }
                for row in rows
            ]

        finally:
            connection.close()

    def get_bonus_ranking(self) -> List[Dict[str, Any]]:
        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    EmployeeID,
                    FirstName,
                    LastName,
                    Salary,
                    Bonus
                FROM Employee
                ORDER BY
                    CASE
                        WHEN Bonus IS NULL THEN 1
                        ELSE 0
                    END,
                    Bonus DESC
            """)

            rows = cursor.fetchall()

            return [
                {
                    "employee_id": row.EmployeeID,
                    "first_name": row.FirstName,
                    "last_name": row.LastName,
                    "salary": float(row.Salary),
                    "bonus": (
                        float(row.Bonus)
                        if row.Bonus is not None
                        else None
                    )
                }
                for row in rows
            ]

        finally:
            connection.close()

    def get_highest_salary(self) -> Dict[str, Any] | None:
        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT TOP 1
                    EmployeeID,
                    FirstName,
                    LastName,
                    Salary,
                    Bonus
                FROM Employee
                ORDER BY Salary DESC
            """)

            row = cursor.fetchone()

            if row is None:
                return None

            return {
                "employee_id": row.EmployeeID,
                "first_name": row.FirstName,
                "last_name": row.LastName,
                "salary": float(row.Salary),
                "bonus": (
                    float(row.Bonus)
                    if row.Bonus is not None
                    else None
                )
            }

        finally:
            connection.close()

    def get_highest_total_compensation(self) -> Dict[str, Any] | None:
        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT TOP 1
                    EmployeeID,
                    FirstName,
                    LastName,
                    Salary,
                    Bonus,
                    Salary + COALESCE(Bonus, 0) AS TotalCompensation
                FROM Employee
                ORDER BY
                    Salary + COALESCE(Bonus, 0) DESC
            """)

            row = cursor.fetchone()

            if row is None:
                return None

            return {
                "employee_id": row.EmployeeID,
                "first_name": row.FirstName,
                "last_name": row.LastName,
                "salary": float(row.Salary),
                "bonus": (
                    float(row.Bonus)
                    if row.Bonus is not None
                    else None
                ),
                "total_compensation": float(row.TotalCompensation)
            }

        finally:
            connection.close()