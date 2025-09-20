employees = [
    {'Employee ID': 101, 'Name': 'Alice', 'Department': 'Sales', 'Salary': 60000},
    {'Employee ID': 102, 'Name': 'Bob', 'Department': 'Marketing', 'Salary': 55000},
    {'Employee ID': 103, 'Name': 'Carol', 'Department': 'Sales', 'Salary': 62000},
    {'Employee ID': 104, 'Name': 'David', 'Department': 'IT', 'Salary': 70000}
]

# Now you can access the data:

# Example: Print the name of the employee with ID 102:
for employee in employees:
    if employee['Employee ID'] == 102:
        print(f"Employee 102's name is: {employee['Name']}")
        break # Exit the loop once found

# Example: Print all employee names and departments:
print("\nEmployee Names and Departments:")
for employee in employees:
    print(f"{employee['Name']} - {employee['Department']}")

# Example: Calculate the average salary:
total_salary = 0
for employee in employees:
    total_salary += employee['Salary']
average_salary = total_salary / len(employees)
print(f"\nAverage Salary: {average_salary}")