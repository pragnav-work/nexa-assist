import pandas as pd
from pathlib import Path


# Project data directory.
DATA_DIR = Path('data/seed')
DATA_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Employees
# --------------------------------------------------

employees = pd.DataFrame([
    ['NC1001', 'Aarav Mehta', 'Data Analytics', 'Data Analyst',
     'aarav.mehta@nexacore.example', '2025-02-10', 'Bengaluru'],

    ['NC1002', 'Diya Nair', 'Engineering', 'Software Engineer',
     'diya.nair@nexacore.example', '2024-08-19', 'Chennai'],

    ['NC1003', 'Kabir Shah', 'Product', 'Product Analyst',
     'kabir.shah@nexacore.example', '2025-05-12', 'Mumbai'],

    ['NC1004', 'Meera Iyer', 'Finance', 'Finance Analyst',
     'meera.iyer@nexacore.example', '2024-11-04', 'Bengaluru'],

    ['NC1005', 'Rohan Kapoor', 'Human Resources', 'HR Specialist',
     'rohan.kapoor@nexacore.example', '2025-01-20', 'Hyderabad'],

    ['NC1006', 'Ananya Rao', 'Customer Success', 'Customer Success Executive',
     'ananya.rao@nexacore.example', '2025-07-07', 'Pune'],

    ['NC1007', 'Vikram Singh', 'Engineering', 'QA Engineer',
     'vikram.singh@nexacore.example', '2024-06-17', 'Chennai'],

    ['NC1008', 'Ishita Bose', 'Marketing', 'Marketing Executive',
     'ishita.bose@nexacore.example', '2025-03-03', 'Mumbai']
], columns=[
    'employee_id',
    'name',
    'department',
    'designation',
    'email',
    'joining_date',
    'location'
])


# --------------------------------------------------
# Leave balances
# --------------------------------------------------

leave_balance = pd.DataFrame([
    ['NC1001', 7, 14, 8],
    ['NC1002', 4, 10, 6],
    ['NC1003', 9, 16, 10],
    ['NC1004', 5, 12, 7],
    ['NC1005', 6, 15, 9],
    ['NC1006', 10, 13, 8],
    ['NC1007', 3, 11, 5],
    ['NC1008', 8, 17, 9]
], columns=[
    'employee_id',
    'casual_leave',
    'earned_leave',
    'sick_leave'
])


# --------------------------------------------------
# Expense records
# --------------------------------------------------

expense_records = pd.DataFrame([
    ['EX5001', 'NC1001', 'Travel', 4200, '2026-08-12',
     'Approved', 'Client meeting travel'],

    ['EX5002', 'NC1001', 'Meals', 850, '2026-08-12',
     'Paid', 'Business lunch'],

    ['EX5003', 'NC1002', 'Office Supplies', 1250, '2026-08-15',
     'Pending', 'External keyboard'],

    ['EX5004', 'NC1003', 'Travel', 6800, '2026-08-21',
     'Approved', 'Conference travel'],

    ['EX5005', 'NC1004', 'Professional Event', 3500, '2026-08-18',
     'Paid', 'Finance workshop'],

    ['EX5006', 'NC1005', 'Travel', 2900, '2026-08-25',
     'Rejected', 'Unapproved travel booking'],

    ['EX5007', 'NC1006', 'Meals', 640, '2026-08-26',
     'Pending', 'Customer meeting meal'],

    ['EX5008', 'NC1007', 'Office Supplies', 980, '2026-08-27',
     'Approved', 'Testing accessories'],

    ['EX5009', 'NC1008', 'Professional Event', 4500, '2026-08-28',
     'Paid', 'Marketing conference']
], columns=[
    'expense_id',
    'employee_id',
    'expense_type',
    'amount',
    'date',
    'status',
    'description'
])


# --------------------------------------------------
# Office locations
# --------------------------------------------------

office_locations = pd.DataFrame([
    ['OFF001', 'Bengaluru',
     'NexaCore Tech Park, Whitefield',
     '09:30-18:30',
     'Cafeteria; Wi-Fi; Meeting Rooms; Parking'],

    ['OFF002', 'Chennai',
     'NexaCore Business Centre, Guindy',
     '09:30-18:30',
     'Cafeteria; Wi-Fi; Meeting Rooms; Parking'],

    ['OFF003', 'Mumbai',
     'NexaCore Tower, Andheri East',
     '09:30-18:30',
     'Cafeteria; Wi-Fi; Meeting Rooms'],

    ['OFF004', 'Hyderabad',
     'NexaCore Workspace, HITEC City',
     '09:30-18:30',
     'Cafeteria; Wi-Fi; Meeting Rooms; Parking'],

    ['OFF005', 'Pune',
     'NexaCore Campus, Hinjawadi',
     '09:30-18:30',
     'Cafeteria; Wi-Fi; Meeting Rooms; Parking']
], columns=[
    'office_id',
    'city',
    'address',
    'working_hours',
    'facilities'
])


# --------------------------------------------------
# IT assets
# --------------------------------------------------

it_assets = pd.DataFrame([
    ['AS1001', 'NC1001', 'Laptop', 'Dell Latitude 7450',
     'NX-LT-1001', 'Assigned', '2025-02-10'],

    ['AS1002', 'NC1001', 'Monitor', 'Dell 24-inch Monitor',
     'NX-MN-1001', 'Assigned', '2025-02-12'],

    ['AS1003', 'NC1002', 'Laptop', 'Lenovo ThinkPad T14',
     'NX-LT-1002', 'Assigned', '2024-08-19'],

    ['AS1004', 'NC1003', 'Laptop', 'HP EliteBook 840',
     'NX-LT-1003', 'Assigned', '2025-05-12'],

    ['AS1005', 'NC1004', 'Laptop', 'Dell Latitude 7440',
     'NX-LT-1004', 'Assigned', '2024-11-04'],

    ['AS1006', 'NC1005', 'Laptop', 'Lenovo ThinkPad T14',
     'NX-LT-1005', 'Assigned', '2025-01-20'],

    ['AS1007', 'NC1006', 'Laptop', 'HP EliteBook 840',
     'NX-LT-1006', 'Assigned', '2025-07-07'],

    ['AS1008', 'NC1007', 'Laptop', 'Dell Latitude 7440',
     'NX-LT-1007', 'Assigned', '2024-06-17'],

    ['AS1009', 'NC1008', 'Laptop', 'Lenovo ThinkPad T14',
     'NX-LT-1008', 'Assigned', '2025-03-03']
], columns=[
    'asset_id',
    'employee_id',
    'asset_type',
    'asset_name',
    'serial_number',
    'status',
    'assigned_date'
])


# --------------------------------------------------
# Leave requests
# --------------------------------------------------

leave_requests = pd.DataFrame([
    ['LR7001', 'NC1001', 'Casual Leave',
     '2026-08-03', '2026-08-04', 2,
     'Approved', '2026-07-28 10:15:00'],

    ['LR7002', 'NC1002', 'Earned Leave',
     '2026-08-14', '2026-08-15', 2,
     'Approved', '2026-08-05 09:20:00'],

    ['LR7003', 'NC1003', 'Casual Leave',
     '2026-08-28', '2026-08-29', 2,
     'Pending', '2026-08-20 14:10:00'],

    ['LR7004', 'NC1004', 'Sick Leave',
     '2026-08-06', '2026-08-06', 1,
     'Approved', '2026-08-06 08:30:00']
], columns=[
    'request_id',
    'employee_id',
    'leave_type',
    'start_date',
    'end_date',
    'days',
    'status',
    'created_at'
])


# --------------------------------------------------
# Write CSV files
# --------------------------------------------------

datasets = {
    'employees.csv': employees,
    'leave_balance.csv': leave_balance,
    'expense_records.csv': expense_records,
    'office_locations.csv': office_locations,
    'it_assets.csv': it_assets,
    'leave_requests.csv': leave_requests
}


for filename, dataframe in datasets.items():
    dataframe.to_csv(DATA_DIR / filename, index=False)
    print(f'Created: {DATA_DIR / filename}')
