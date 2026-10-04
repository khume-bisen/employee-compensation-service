import json
from datetime import date

import azure.functions as func

from models.employee import Employee
from services.employee_service import EmployeeService
from services.report_service import ReportService
from utils.serializers import employee_to_dict


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


# ============================================================
# HEALTH
# ============================================================

@app.route(route="health", methods=["GET"])
def health(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({
            "status": "healthy",
            "service": "Employee Compensation Service"
        }),
        status_code=200,
        mimetype="application/json"
    )


# ============================================================
# GET ALL EMPLOYEES / GET BY DEPARTMENT
# ============================================================

@app.route(route="employees", methods=["GET"])
def get_employees(req: func.HttpRequest) -> func.HttpResponse:
    try:
        service = EmployeeService()

        department_id = req.params.get("departmentId")

        if department_id:
            try:
                department_id = int(department_id)
            except ValueError:
                return func.HttpResponse(
                    json.dumps({
                        "error": "departmentId must be an integer"
                    }),
                    status_code=400,
                    mimetype="application/json"
                )

            employees = service.get_employees_by_department(
                department_id
            )
        else:
            employees = service.get_all_employees()

        response = [
            employee_to_dict(employee)
            for employee in employees
        ]

        return func.HttpResponse(
            json.dumps(response),
            status_code=200,
            mimetype="application/json"
        )

    except ValueError as exc:
        return func.HttpResponse(
            json.dumps({"error": str(exc)}),
            status_code=400,
            mimetype="application/json"
        )

    except Exception as exc:
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error",
                "details": str(exc)
            }),
            status_code=500,
            mimetype="application/json"
        )


# ============================================================
# GET EMPLOYEE BY ID
# ============================================================

@app.route(route="employees/{employeeId}", methods=["GET"])
def get_employee_by_id(req: func.HttpRequest) -> func.HttpResponse:
    try:
        employee_id = req.route_params.get("employeeId")

        try:
            employee_id = int(employee_id)
        except (ValueError, TypeError):
            return func.HttpResponse(
                json.dumps({
                    "error": "employeeId must be an integer"
                }),
                status_code=400,
                mimetype="application/json"
            )

        service = EmployeeService()
        employee = service.get_employee(employee_id)

        if employee is None:
            return func.HttpResponse(
                json.dumps({
                    "error": "Employee not found"
                }),
                status_code=404,
                mimetype="application/json"
            )

        return func.HttpResponse(
            json.dumps(employee_to_dict(employee)),
            status_code=200,
            mimetype="application/json"
        )

    except ValueError as exc:
        return func.HttpResponse(
            json.dumps({"error": str(exc)}),
            status_code=400,
            mimetype="application/json"
        )

    except Exception as exc:
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error",
                "details": str(exc)
            }),
            status_code=500,
            mimetype="application/json"
        )


# ============================================================
# CREATE EMPLOYEE
# ============================================================

@app.route(route="employees", methods=["POST"])
def create_employee(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()

        employee = Employee(
            employee_id=None,
            first_name=body.get("first_name"),
            last_name=body.get("last_name"),
            department_id=int(body.get("department_id")),
            salary=float(body.get("salary")),
            bonus=(
                float(body["bonus"])
                if body.get("bonus") is not None
                else None
            ),
            hire_date=date.fromisoformat(
                body.get("hire_date")
            )
        )

        service = EmployeeService()
        created_employee = service.create_employee(employee)

        return func.HttpResponse(
            json.dumps(
                employee_to_dict(created_employee)
            ),
            status_code=201,
            mimetype="application/json"
        )

    except (ValueError, TypeError, KeyError) as exc:
        return func.HttpResponse(
            json.dumps({"error": str(exc)}),
            status_code=400,
            mimetype="application/json"
        )

    except Exception as exc:
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error",
                "details": str(exc)
            }),
            status_code=500,
            mimetype="application/json"
        )


# ============================================================
# UPDATE EMPLOYEE
# ============================================================

@app.route(route="employees/{employeeId}", methods=["PUT"])
def update_employee(req: func.HttpRequest) -> func.HttpResponse:
    try:
        employee_id = req.route_params.get("employeeId")

        try:
            employee_id = int(employee_id)
        except (ValueError, TypeError):
            return func.HttpResponse(
                json.dumps({
                    "error": "employeeId must be an integer"
                }),
                status_code=400,
                mimetype="application/json"
            )

        body = req.get_json()

        employee = Employee(
            employee_id=employee_id,
            first_name=body.get("first_name"),
            last_name=body.get("last_name"),
            department_id=int(body.get("department_id")),
            salary=float(body.get("salary")),
            bonus=(
                float(body["bonus"])
                if body.get("bonus") is not None
                else None
            ),
            hire_date=date.fromisoformat(
                body.get("hire_date")
            )
        )

        service = EmployeeService()
        updated_employee = service.update_employee(employee)

        if updated_employee is None:
            return func.HttpResponse(
                json.dumps({
                    "error": "Employee not found"
                }),
                status_code=404,
                mimetype="application/json"
            )

        return func.HttpResponse(
            json.dumps(
                employee_to_dict(updated_employee)
            ),
            status_code=200,
            mimetype="application/json"
        )

    except (ValueError, TypeError, KeyError) as exc:
        return func.HttpResponse(
            json.dumps({"error": str(exc)}),
            status_code=400,
            mimetype="application/json"
        )

    except Exception as exc:
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error",
                "details": str(exc)
            }),
            status_code=500,
            mimetype="application/json"
        )


# ============================================================
# DELETE EMPLOYEE
# ============================================================

@app.route(route="employees/{employeeId}", methods=["DELETE"])
def delete_employee(req: func.HttpRequest) -> func.HttpResponse:
    try:
        employee_id = req.route_params.get("employeeId")

        try:
            employee_id = int(employee_id)
        except (ValueError, TypeError):
            return func.HttpResponse(
                json.dumps({
                    "error": "employeeId must be an integer"
                }),
                status_code=400,
                mimetype="application/json"
            )

        service = EmployeeService()
        deleted = service.delete_employee(employee_id)

        if not deleted:
            return func.HttpResponse(
                json.dumps({
                    "error": "Employee not found"
                }),
                status_code=404,
                mimetype="application/json"
            )

        return func.HttpResponse(
            json.dumps({
                "message": "Employee deleted successfully",
                "employee_id": employee_id
            }),
            status_code=200,
            mimetype="application/json"
        )

    except ValueError as exc:
        return func.HttpResponse(
            json.dumps({"error": str(exc)}),
            status_code=400,
            mimetype="application/json"
        )

    except Exception as exc:
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error",
                "details": str(exc)
            }),
            status_code=500,
            mimetype="application/json"
        )


# ============================================================
# REPORT 1 - TOTAL BONUS
# ============================================================

@app.route(route="reports/total-bonus", methods=["GET"])
def total_bonus(req: func.HttpRequest) -> func.HttpResponse:
    try:
        service = ReportService()

        total_bonus_value = service.get_total_bonus()

        return func.HttpResponse(
            json.dumps({
                "total_bonus": total_bonus_value
            }),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as exc:
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error",
                "details": str(exc)
            }),
            status_code=500,
            mimetype="application/json"
        )


# ============================================================
# REPORT 2 - EMPLOYEES WITH NO BONUS
# ============================================================

@app.route(route="reports/no-bonus", methods=["GET"])
def no_bonus(req: func.HttpRequest) -> func.HttpResponse:
    try:
        service = ReportService()

        employees = service.get_employees_with_no_bonus()

        return func.HttpResponse(
            json.dumps(employees),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as exc:
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error",
                "details": str(exc)
            }),
            status_code=500,
            mimetype="application/json"
        )


# ============================================================
# REPORT 3 - BONUS PERCENTAGE
# ============================================================

@app.route(route="reports/bonus-percentage", methods=["GET"])
def bonus_percentage(req: func.HttpRequest) -> func.HttpResponse:
    try:
        service = ReportService()

        employees = service.get_bonus_percentage()

        return func.HttpResponse(
            json.dumps(employees),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as exc:
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error",
                "details": str(exc)
            }),
            status_code=500,
            mimetype="application/json"
        )


# ============================================================
# REPORT 4 - DEPARTMENT BONUS
# ============================================================

@app.route(route="reports/department-bonus", methods=["GET"])
def department_bonus(req: func.HttpRequest) -> func.HttpResponse:
    try:
        service = ReportService()

        departments = service.get_department_bonus()

        return func.HttpResponse(
            json.dumps(departments),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as exc:
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error",
                "details": str(exc)
            }),
            status_code=500,
            mimetype="application/json"
        )


# ============================================================
# REPORT 5 - BONUS RANKING
# ============================================================

@app.route(route="reports/bonus-ranking", methods=["GET"])
def bonus_ranking(req: func.HttpRequest) -> func.HttpResponse:
    try:
        service = ReportService()

        employees = service.get_bonus_ranking()

        return func.HttpResponse(
            json.dumps(employees),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as exc:
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error",
                "details": str(exc)
            }),
            status_code=500,
            mimetype="application/json"
        )


# ============================================================
# REPORT 6 - HIGHEST SALARY
# ============================================================

@app.route(route="reports/highest-salary", methods=["GET"])
def highest_salary(req: func.HttpRequest) -> func.HttpResponse:
    try:
        service = ReportService()

        result = service.get_highest_salary()

        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as exc:
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error",
                "details": str(exc)
            }),
            status_code=500,
            mimetype="application/json"
        )


# ============================================================
# REPORT 7 - HIGHEST TOTAL COMPENSATION
# ============================================================

@app.route(
    route="reports/highest-total-compensation",
    methods=["GET"]
)
def highest_total_compensation(
    req: func.HttpRequest
) -> func.HttpResponse:
    try:
        service = ReportService()

        result = service.get_highest_total_compensation()

        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as exc:
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error",
                "details": str(exc)
            }),
            status_code=500,
            mimetype="application/json"
        )