from dataclasses import asdict
from datetime import date, datetime

from models.employee import Employee


def employee_to_dict(employee: Employee) -> dict:
    data = asdict(employee)

    if isinstance(data.get("hire_date"), (date, datetime)):
        data["hire_date"] = data["hire_date"].isoformat()

    return data
