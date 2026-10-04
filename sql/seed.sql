INSERT INTO Department (DepartmentID, DepartmentName, Location)
VALUES
(1, 'Engineering', 'Pune'),
(2, 'Human Resources', 'Mumbai'),
(3, 'Finance', 'Pune'),
(4, 'Sales', 'Bangalore'),
(5, 'Marketing', 'Mumbai');

INSERT INTO Employee
    (FirstName, LastName, DepartmentID, Salary, Bonus, HireDate)
VALUES
('Khumendra', 'Bisen', 1, 900000.00, 100000.00, '2022-01-15'),
('Priya', 'Patil', 1, 800000.00, 80000.00, '2022-03-10'),
('Rahul', 'Deshmukh', 2, 700000.00, NULL, '2021-06-20'),
('Sneha', 'Joshi', 3, 750000.00, 75000.00, '2023-01-05'),
('Vikram', 'Kulkarni', 4, 650000.00, 65000.00, '2022-08-12'),
('Ananya', 'Shah', 5, 600000.00, NULL, '2023-04-18'),
('Rohan', 'Mehta', 1, 950000.00, 120000.00, '2020-11-01'),
('Kavya', 'Pawar', 2, 680000.00, NULL, '2021-09-25'),
('Aditya', 'More', 3, 720000.00, 60000.00, '2022-12-15'),
('Neha', 'Gupta', 4, 620000.00, 60000.00, '2023-02-20');
