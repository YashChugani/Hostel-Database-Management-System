from datetime import date, timedelta
from app import create_app, db
from app.models import Student, Hostel, Staff, Room, Allocation, Fee, Complaint, MaintenanceRequest, Visitor

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # ========== 1. HOSTELS ==========
    hostel_a = Hostel(HostelID='A', HostelName='Aryabhatt Hostel', Type='Boys')
    hostel_b = Hostel(HostelID='B', HostelName='Bhavani Hostel', Type='Girls')
    hostel_c = Hostel(HostelID='C', HostelName='Chanakya Hostel', Type='Co-ed')

    db.session.add_all([hostel_a, hostel_b, hostel_c])
    db.session.commit()

    # ========== 2. STAFF ==========
    staff_warden_a = Staff(StaffName='Ramesh Kumar', Role='Warden', Phone='9876500011', Email='ramesh@hostel.com', HostelID='A')
    staff_warden_b = Staff(StaffName='Neeta Sharma', Role='Warden', Phone='9876500022', Email='neeta@hostel.com', HostelID='B')
    staff_warden_c = Staff(StaffName='Kiran Patel', Role='Warden', Phone='9876500033', Email='kiran@hostel.com', HostelID='C')

    staff_security = Staff(StaffName='Suresh Yadav', Role='Security', Phone='9876500044', Email='suresh@hostel.com', HostelID='A')
    staff_maintenance = Staff(StaffName='Mahesh Verma', Role='Maintenance', Phone='9876500055', Email='mahesh@hostel.com', HostelID='A')

    db.session.add_all([staff_warden_a, staff_warden_b, staff_warden_c, staff_security, staff_maintenance])
    db.session.commit()

    # Link wardens to hostels
    hostel_a.WardenID = staff_warden_a.StaffID
    hostel_b.WardenID = staff_warden_b.StaffID
    hostel_c.WardenID = staff_warden_c.StaffID
    db.session.commit()

    # ========== 3. ROOMS ==========
    rooms = [
        Room(RoomNumber='101', Floor=1, Capacity=2, Occupants=1, Status='Partially Occupied', HostelID='A'),
        Room(RoomNumber='102', Floor=1, Capacity=2, Occupants=2, Status='Full', HostelID='A'),
        Room(RoomNumber='201', Floor=2, Capacity=3, Occupants=1, Status='Partially Occupied', HostelID='B'),
        Room(RoomNumber='301', Floor=3, Capacity=2, Occupants=0, Status='Vacant', HostelID='C'),
    ]
    db.session.add_all(rooms)
    db.session.commit()

    # ========== 4. STUDENTS ==========
    students = [
        Student(StudentName='Arjun Mehta', Email='arjun@example.com', Phone='9000000001',
                Address='Block A, Street 5', DOB=date(2003, 5, 10), Gender='Male', Course='CSE', Year=3),
        Student(StudentName='Priya Nair', Email='priya@example.com', Phone='9000000002',
                Address='Block B, Street 9', DOB=date(2004, 1, 22), Gender='Female', Course='ECE', Year=2),
        Student(StudentName='Rahul Sharma', Email='rahul@example.com', Phone='9000000003',
                Address='Block C, Street 3', DOB=date(2002, 9, 14), Gender='Male', Course='ME', Year=4),
        Student(StudentName='Sneha Verma', Email='sneha@example.com', Phone='9000000004',
                Address='Block D, Street 7', DOB=date(2003, 11, 30), Gender='Female', Course='AI', Year=1),
    ]
    db.session.add_all(students)
    db.session.commit()

    # ========== 5. ALLOCATIONS ==========
    allocations = [
        Allocation(StudentID=students[0].StudentID, RoomID=rooms[0].RoomID, StartDate=date(2024, 7, 1)),
        Allocation(StudentID=students[1].StudentID, RoomID=rooms[2].RoomID, StartDate=date(2024, 8, 1)),
        Allocation(StudentID=students[2].StudentID, RoomID=rooms[1].RoomID, StartDate=date(2024, 6, 15)),
    ]
    db.session.add_all(allocations)
    db.session.commit()

    # ========== 6. FEES ==========
    fees = [
        Fee(StudentID=students[0].StudentID, Amount=12000.00, DueDate=date(2024, 12, 31), Status='Paid', PaymentDate=date(2024, 12, 10)),
        Fee(StudentID=students[1].StudentID, Amount=12000.00, DueDate=date(2024, 12, 31), Status='Unpaid'),
        Fee(StudentID=students[2].StudentID, Amount=15000.00, DueDate=date(2024, 11, 30), Status='Overdue'),
    ]
    db.session.add_all(fees)
    db.session.commit()

    # ========== 7. COMPLAINTS ==========
    complaints = [
        Complaint(StudentID=students[0].StudentID, Description='Fan not working', Status='Resolved'),
        Complaint(StudentID=students[1].StudentID, Description='Water leakage in bathroom', Status='In-Progress'),
    ]
    db.session.add_all(complaints)
    db.session.commit()

    # ========== 8. MAINTENANCE REQUESTS ==========
    requests = [
        MaintenanceRequest(RoomID=rooms[0].RoomID, RequestedBy=students[0].StudentID,
                           AssignedTo=staff_maintenance.StaffID, Status='Completed'),
        MaintenanceRequest(RoomID=rooms[1].RoomID, RequestedBy=students[2].StudentID,
                           AssignedTo=staff_maintenance.StaffID, Status='Pending'),
    ]
    db.session.add_all(requests)
    db.session.commit()

    # ========== 9. VISITORS ==========
    visitors = [
        Visitor(Name='Vikram Singh', Phone='9001112233', Purpose='Meet friend', HostStudentID=students[0].StudentID),
        Visitor(Name='Aditi Rao', Phone='9002223344', Purpose='Deliver books', HostStudentID=students[1].StudentID),
    ]
    db.session.add_all(visitors)
    db.session.commit()

    print("✅ Database seeded successfully with 9 tables and sample data.")
