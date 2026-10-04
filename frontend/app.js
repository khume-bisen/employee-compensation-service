const API_BASE =
    "https://fusion-employee-api-kb-2026.azurewebsites.net/api";

const DEPARTMENTS = {
    1: "Engineering",
    2: "Human Resources",
    3: "Finance",
    4: "Sales",
    5: "Marketing"
};

const state = {
    employees: [],
    editingId: null
};

const $ = (id) => document.getElementById(id);

const money = (value) => {
    if (value === null || value === undefined) {
        return "—";
    }

    return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 0
    }).format(value);
};

function dept(id) {
    return DEPARTMENTS[id] || `Department ${id}`;
}

/*
 * The bonus-ranking API does not currently return department_id.
 * Therefore, look up the employee in the already-loaded employee list.
 */
function getEmployeeDepartment(employeeId) {
    const employee = state.employees.find(
        (item) => item.employee_id === employeeId
    );

    return employee
        ? dept(employee.department_id)
        : "Department";
}

function toast(message, error = false) {
    const element = $("toast");

    element.textContent = message;
    element.style.background = error ? "#b83b4a" : "#162238";

    element.classList.add("show");

    setTimeout(() => {
        element.classList.remove("show");
    }, 2600);
}

async function api(path, options = {}) {
    const response = await fetch(API_BASE + path, {
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        },
        ...options
    });

    if (!response.ok) {
        let data = {};

        try {
            data = await response.json();
        } catch {
            // Ignore JSON parsing failure.
        }

        throw new Error(
            data.details ||
            data.error ||
            `Request failed (${response.status})`
        );
    }

    return response.status === 204
        ? null
        : response.json();
}

/*
 * Smooth number animation for dashboard KPI cards.
 */
function animateNumber(element, target, formatter = (value) => value) {
    const start = Number(element.dataset.value || 0);
    const end = Number(target || 0);

    if (!Number.isFinite(end)) {
        element.textContent = formatter(target);
        return;
    }

    const startTime = performance.now();

    function tick(currentTime) {
        const progress = Math.min(
            1,
            (currentTime - startTime) / 420
        );

        const easedProgress =
            1 - Math.pow(1 - progress, 3);

        const currentValue =
            start + (end - start) * easedProgress;

        element.textContent = formatter(currentValue);

        if (progress < 1) {
            requestAnimationFrame(tick);
        }
    }

    element.dataset.value = end;

    requestAnimationFrame(tick);
}

/*
 * Load all live data from Azure Functions.
 */
async function loadAll() {
    try {
        const [
            employees,
            totalBonus,
            noBonus,
            highestSalary,
            highestCompensation,
            ranking
        ] = await Promise.all([
            api("/employees"),
            api("/reports/total-bonus"),
            api("/reports/no-bonus"),
            api("/reports/highest-salary"),
            api("/reports/highest-total-compensation"),
            api("/reports/bonus-ranking")
        ]);

        state.employees = employees;

        renderDashboard({
            totalBonus,
            noBonus,
            highestSalary,
            highestCompensation,
            ranking
        });

        renderEmployees();
        renderRanking(ranking);
        populateDepartments();

        $("apiStatusText").textContent = "API Connected";
        $("lastSync").textContent = "Synced just now";

    } catch (error) {
        console.error("API Error:", error);

        $("apiStatusText").textContent = "API Error";
        $("lastSync").textContent = "Check connection";

        toast(error.message, true);
    }
}

/*
 * Dashboard
 */
function renderDashboard(reportData) {
    const {
        totalBonus,
        noBonus,
        highestSalary,
        highestCompensation,
        ranking
    } = reportData;

    // KPI cards
    animateNumber(
        $("totalEmployees"),
        state.employees.length,
        (value) => Math.round(value)
    );

    animateNumber(
        $("totalBonus"),
        totalBonus.total_bonus,
        money
    );

    animateNumber(
        $("highestSalary"),
        highestSalary.salary,
        money
    );

    animateNumber(
        $("highestComp"),
        highestCompensation.total_compensation,
        money
    );

    // Highest salary employee
    $("highestSalaryName").textContent =
        `${highestSalary.first_name} ${highestSalary.last_name}`;

    // Highest compensation employee
    $("highestCompName").textContent =
        `${highestCompensation.first_name} ${highestCompensation.last_name}`;

    // Reports cards
    $("reportTotalBonus").textContent =
        money(totalBonus.total_bonus);

    $("reportHighestSalary").textContent =
        money(highestSalary.salary);

    $("reportHighestSalaryName").textContent =
        `${highestSalary.first_name} ${highestSalary.last_name}`;

    $("reportHighestComp").textContent =
        money(highestCompensation.total_compensation);

    $("reportHighestCompName").textContent =
        `${highestCompensation.first_name} ${highestCompensation.last_name}`;

    $("reportNoBonus").textContent =
        noBonus.length;

    /*
     * Compensation leaders
     *
     * Important:
     * bonus-ranking does not return department_id,
     * so getEmployeeDepartment() resolves it
     * from the /employees response.
     */
    $("leaders").innerHTML = ranking
        .slice(0, 5)
        .map((employee, index) => {
            const totalCompensation =
                employee.salary +
                (employee.bonus || 0);

            const department =
                getEmployeeDepartment(employee.employee_id);

            return `
                <div class="leader">
                    <div>
                        <div class="leader-name">
                            ${index + 1}. ${employee.first_name} ${employee.last_name}
                        </div>

                        <div class="leader-sub">
                            ${department}
                            · Salary ${money(employee.salary)}
                            · Bonus ${money(employee.bonus)}
                        </div>
                    </div>

                    <div class="leader-value">
                        ${money(totalCompensation)}
                    </div>
                </div>
            `;
        })
        .join("");

    /*
     * Bonus distribution
     */
    const employeesWithBonus =
        state.employees.filter(
            (employee) => employee.bonus !== null
        ).length;

    const employeesWithoutBonus =
        noBonus.length;

    const averageSalary =
        state.employees.reduce(
            (total, employee) => total + employee.salary,
            0
        ) / Math.max(1, state.employees.length);

    $("bonusSummary").innerHTML = `
        <div class="summary-row">
            <span>With bonus</span>
            <span>${employeesWithBonus}</span>
        </div>

        <div class="summary-row">
            <span>Without bonus</span>
            <span>${employeesWithoutBonus}</span>
        </div>

        <div class="summary-row">
            <span>Average salary</span>
            <span>${money(averageSalary)}</span>
        </div>
    `;
}

/*
 * Populate department dropdowns.
 */
function populateDepartments() {
    const departmentIds = [
        ...new Set(
            state.employees.map(
                (employee) => employee.department_id
            )
        )
    ].sort((a, b) => a - b);

    $("departmentFilter").innerHTML =
        '<option value="">All departments</option>';

    $("departmentId").innerHTML = "";

    departmentIds.forEach((id) => {
        $("departmentFilter").insertAdjacentHTML(
            "beforeend",
            `<option value="${id}">${dept(id)}</option>`
        );

        $("departmentId").insertAdjacentHTML(
            "beforeend",
            `<option value="${id}">${dept(id)}</option>`
        );
    });
}

/*
 * Employee table
 */
function renderEmployees() {
    const searchQuery =
        $("searchInput").value.toLowerCase();

    const selectedDepartment =
        $("departmentFilter").value;

    const filteredEmployees =
        state.employees.filter((employee) => {
            const matchesDepartment =
                !selectedDepartment ||
                String(employee.department_id) ===
                    selectedDepartment;

            const fullName =
                `${employee.first_name} ${employee.last_name}`
                    .toLowerCase();

            const matchesSearch =
                fullName.includes(searchQuery);

            return (
                matchesDepartment &&
                matchesSearch
            );
        });

    $("employeeTable").innerHTML =
        filteredEmployees
            .map((employee) => {
                const totalCompensation =
                    employee.salary +
                    (employee.bonus || 0);

                return `
                    <tr>
                        <td>
                            <div class="employee-name">
                                ${employee.first_name}
                                ${employee.last_name}
                            </div>

                            <div class="muted">
                                #${employee.employee_id}
                            </div>
                        </td>

                        <td>
                            ${dept(employee.department_id)}
                        </td>

                        <td>
                            ${money(employee.salary)}
                        </td>

                        <td>
                            ${money(employee.bonus)}
                        </td>

                        <td>
                            ${money(totalCompensation)}
                        </td>

                        <td>
                            ${employee.hire_date}
                        </td>

                        <td>
                            <div class="actions">
                                <button
                                    class="small-btn"
                                    onclick="editEmployee(${employee.employee_id})"
                                >
                                    Edit
                                </button>

                                <button
                                    class="small-btn danger"
                                    onclick="deleteEmployee(${employee.employee_id})"
                                >
                                    Delete
                                </button>
                            </div>
                        </td>
                    </tr>
                `;
            })
            .join("") ||
        `
            <tr>
                <td
                    colspan="7"
                    class="muted"
                >
                    No employees found.
                </td>
            </tr>
        `;
}

/*
 * Bonus ranking report.
 *
 * Department is resolved from state.employees because
 * bonus-ranking does not currently return department_id.
 */
function renderRanking(ranking) {
    $("rankingTable").innerHTML =
        ranking
            .map((employee, index) => {
                const department =
                    getEmployeeDepartment(
                        employee.employee_id
                    );

                return `
                    <tr>
                        <td>
                            #${index + 1}
                        </td>

                        <td class="employee-name">
                            ${employee.first_name}
                            ${employee.last_name}
                        </td>

                        <td>
                            ${department}
                        </td>

                        <td>
                            ${money(employee.salary)}
                        </td>

                        <td>
                            ${money(employee.bonus)}
                        </td>
                    </tr>
                `;
            })
            .join("");
}

/*
 * Open Add/Edit Employee modal.
 */
function openModal(employee = null) {
    state.editingId =
        employee?.employee_id || null;

    $("modalTitle").textContent =
        employee
            ? "Edit Employee"
            : "Add Employee";

    $("firstName").value =
        employee?.first_name || "";

    $("lastName").value =
        employee?.last_name || "";

    $("departmentId").value =
        employee?.department_id || 1;

    $("salary").value =
        employee?.salary || "";

    $("bonus").value =
        employee?.bonus ?? "";

    $("hireDate").value =
        employee?.hire_date || "";

    $("employeeModal").classList.remove(
        "hidden"
    );
}

/*
 * Edit employee
 */
window.editEmployee = (id) => {
    const employee =
        state.employees.find(
            (item) =>
                item.employee_id === id
        );

    if (!employee) {
        toast(
            "Employee not found.",
            true
        );

        return;
    }

    openModal(employee);
};

/*
 * Delete employee
 */
window.deleteEmployee = async (id) => {
    const confirmed = confirm(
        `Delete employee #${id}?`
    );

    if (!confirmed) {
        return;
    }

    try {
        await api(
            `/employees/${id}`,
            {
                method: "DELETE"
            }
        );

        toast(
            "Employee deleted successfully."
        );

        await loadAll();

    } catch (error) {
        toast(
            error.message,
            true
        );
    }
};

/*
 * Add / Update employee
 */
$("employeeForm").addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        const employeeData = {
            first_name:
                $("firstName")
                    .value
                    .trim(),

            last_name:
                $("lastName")
                    .value
                    .trim(),

            department_id:
                Number(
                    $("departmentId").value
                ),

            salary:
                Number(
                    $("salary").value
                ),

            bonus:
                $("bonus").value === ""
                    ? null
                    : Number(
                        $("bonus").value
                    ),

            hire_date:
                $("hireDate").value
        };

        try {
            if (state.editingId) {
                await api(
                    `/employees/${state.editingId}`,
                    {
                        method: "PUT",
                        body: JSON.stringify({
                            employee_id:
                                state.editingId,
                            ...employeeData
                        })
                    }
                );

                toast(
                    "Employee updated successfully."
                );

            } else {
                await api(
                    "/employees",
                    {
                        method: "POST",
                        body: JSON.stringify(
                            employeeData
                        )
                    }
                );

                toast(
                    "Employee created successfully."
                );
            }

            $("employeeModal").classList.add(
                "hidden"
            );

            await loadAll();

        } catch (error) {
            toast(
                error.message,
                true
            );
        }
    }
);

/*
 * Add employee button
 */
$("addEmployeeBtn").onclick = () => {
    openModal();
};

/*
 * Close modal
 */
$("closeModal").onclick = () => {
    $("employeeModal").classList.add(
        "hidden"
    );
};

$("cancelBtn").onclick = () => {
    $("employeeModal").classList.add(
        "hidden"
    );
};

/*
 * Search
 */
$("searchInput").oninput = () => {
    renderEmployees();
};

/*
 * Department filter
 */
$("departmentFilter").onchange = () => {
    renderEmployees();
};

/*
 * Refresh button
 */
$("refreshBtn").onclick = async () => {
    const button = $("refreshBtn");

    button.disabled = true;
    button.style.opacity = "0.65";

    try {
        await loadAll();
    } finally {
        button.disabled = false;
        button.style.opacity = "1";
    }
};

/*
 * Sidebar navigation
 */
document
    .querySelectorAll(".nav-item")
    .forEach((button) => {
        button.onclick = () => {
            document
                .querySelectorAll(".nav-item")
                .forEach((item) => {
                    item.classList.remove(
                        "active"
                    );
                });

            document
                .querySelectorAll(".page-section")
                .forEach((section) => {
                    section.classList.remove(
                        "active-section"
                    );
                });

            button.classList.add("active");

            $(
                button.dataset.section
            ).classList.add(
                "active-section"
            );

            $("pageTitle").textContent =
                button.textContent.trim();
        };
    });

/*
 * Initial load
 */
loadAll();