# Employee Compensation Service

A backend REST API for managing employee compensation data, built with **Python Azure Functions** and **Azure SQL Database**.

The service provides employee CRUD operations, department filtering, compensation reports, health monitoring, and Azure cloud deployment.

## Architecture

```text
Client / Postman
       |
       v
Azure Functions HTTP API
       |
       v
Service Layer
       |
       v
Repository Layer
       |
       v
Azure SQL Database
```

### Layers

- **API Layer** — Azure Functions HTTP endpoints
- **Service Layer** — business logic and validation
- **Repository Layer** — SQL database operations
- **Model Layer** — Employee and Department data models
- **Database Layer** — Azure SQL schema and seed data

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Backend runtime on Azure |
| Azure Functions | Serverless REST API |
| Azure SQL Database | Relational database |
| pyodbc | SQL Server connectivity |
| SQL Server | Database engine |
| Azure Application Insights | Monitoring |
| Azure Storage Account | Azure Functions storage |
| Git / GitHub | Version control |
| Postman / cURL | API testing |

## Azure Resources

| Resource | Value |
|---|---|
| Resource Group | `fusion-employee-service-rg` |
| Function App | `fusion-employee-api-kb-2026` |
| SQL Server | `fusion-employee-sql-kb-2026` |
| SQL Database | `EmployeeCompensationDB` |
| Storage Account | `fusionemployeesa2026kb` |
| Region | Central India |

## API Base URL

```text
https://fusion-employee-api-kb-2026.azurewebsites.net/api
```

## API Endpoints

### Health

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Service health check |

### Employee APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/employees` | Get all employees |
| GET | `/employees/{employeeId}` | Get employee by ID |
| GET | `/employees?departmentId={departmentId}` | Get employees by department |
| POST | `/employees` | Create employee |
| PUT | `/employees/{employeeId}` | Update employee |
| DELETE | `/employees/{employeeId}` | Delete employee |

### Report APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/reports/total-bonus` | Calculate total bonus |
| GET | `/reports/no-bonus` | Find employees without bonus |
| GET | `/reports/bonus-percentage` | Calculate bonus percentage |
| GET | `/reports/department-bonus` | Department bonus analysis |
| GET | `/reports/bonus-ranking` | Rank employees by bonus |
| GET | `/reports/highest-salary` | Find highest-paid employee |
| GET | `/reports/highest-total-compensation` | Find highest total compensation |

## Example API Responses

### Get All Employees

```http
GET /api/employees
```

Example:

```json
[
  {
    "employee_id": 1,
    "first_name": "Khumendra",
    "last_name": "Bisen",
    "department_id": 1,
    "salary": 900000.0,
    "bonus": 100000.0,
    "hire_date": "2022-01-15"
  }
]
```

### Highest Total Compensation

```http
GET /api/reports/highest-total-compensation
```

Example:

```json
{
  "employee_id": 7,
  "first_name": "Rohan",
  "last_name": "Mehta",
  "salary": 950000.0,
  "bonus": 120000.0,
  "total_compensation": 1070000.0
}
```

## Database Schema

### Department

```text
DepartmentID       INT PRIMARY KEY
DepartmentName     VARCHAR(100)
Location           VARCHAR(100)
```

### Employee

```text
EmployeeID         INT IDENTITY PRIMARY KEY
FirstName          VARCHAR(50)
LastName           VARCHAR(50)
DepartmentID       INT FOREIGN KEY
Salary             DECIMAL(12,2)
Bonus              DECIMAL(12,2) NULL
HireDate           DATE
```

The Employee table has a foreign-key relationship with Department.

Salary and Bonus values are validated to prevent negative values.

## Project Structure

```text
employee-compensation-service/
│
├── models/
│   ├── __init__.py
│   ├── employee.py
│   └── department.py
│
├── repositories/
│   ├── __init__.py
│   ├── employee_repository.py
│   └── report_repository.py
│
├── services/
│   ├── __init__.py
│   ├── employee_service.py
│   └── report_service.py
│
├── utils/
│   ├── __init__.py
│   ├── db.py
│   └── serializers.py
│
├── sql/
│   ├── schema.sql
│   └── seed.sql
│
├── tests/
│
├── function_app.py
├── host.json
├── requirements.txt
├── .gitignore
└── README.md
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/khume-bisen/employee-compensation-service.git
cd employee-compensation-service
```

### 2. Create virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `local.settings.json` locally with the required Azure Functions and SQL configuration.

The SQL connection string must be stored in:

```text
AZURE_SQL_CONNECTION_STRING
```

`local.settings.json` is excluded from Git using `.gitignore`.

**Never commit database credentials or secrets to source control.**

### 5. Run Azure Functions locally

```powershell
func start
```

The local API will be available at:

```text
http://localhost:7071/api
```

## Database Setup

The SQL scripts are located in:

```text
sql/schema.sql
sql/seed.sql
```

`schema.sql` creates the Department and Employee tables.

`seed.sql` inserts sample departments and employees.

## Azure Deployment

The application is deployed using Azure Functions Core Tools.

```powershell
func azure functionapp publish fusion-employee-api-kb-2026 --python
```

Azure performs the remote build and installs the dependencies specified in `requirements.txt`.

## Security

The project follows these security practices:

- Database credentials are stored in environment/application settings.
- `local.settings.json` is excluded from Git.
- `.venv` is excluded from Git.
- Local Azurite data is excluded from Git.
- SQL passwords are not stored in source code.
- Azure SQL firewall rules restrict database access.

## Validation

The deployed API was tested for:

- Health check
- Get all employees
- Get employee by ID
- Department filtering
- Create employee
- Update employee
- Delete employee
- Total bonus report
- No-bonus employee report
- Bonus percentage report
- Department bonus report
- Bonus ranking
- Highest salary
- Highest total compensation

The deployed highest-total-compensation endpoint was verified with HTTP `200 OK` and returned:

```json
{
  "employee_id": 7,
  "first_name": "Rohan",
  "last_name": "Mehta",
  "salary": 950000.0,
  "bonus": 120000.0,
  "total_compensation": 1070000.0
}
```

## Example cURL

Health:

```powershell
curl.exe -i https://fusion-employee-api-kb-2026.azurewebsites.net/api/health
```

Employees:

```powershell
curl.exe -i https://fusion-employee-api-kb-2026.azurewebsites.net/api/employees
```

Highest total compensation:

```powershell
curl.exe -i https://fusion-employee-api-kb-2026.azurewebsites.net/api/reports/highest-total-compensation
```

## Key Design Decisions

### Repository Pattern

Database operations are isolated inside repository classes. This keeps SQL logic separate from business logic.

### Service Layer

Business validation is handled by service classes before repository operations are executed.

### Serverless Architecture

Azure Functions provides a scalable HTTP-based serverless backend without requiring management of traditional application servers.

### Azure SQL

Azure SQL provides relational storage with foreign-key constraints, validation rules, and SQL-based reporting.

## Future Improvements

Potential future improvements include:

- Automated unit and integration tests
- API authentication and authorization
- Azure Managed Identity for database authentication
- CI/CD using GitHub Actions
- API documentation using OpenAPI / Swagger
- Pagination for employee APIs
- Centralized structured logging
- Frontend dashboard for employee and compensation reporting

## Author

**Khumendra Bisen**

GitHub: https://github.com/khume-bisen

---

Built as part of the Fusion Practices technical assignment.
