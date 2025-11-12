from datetime import date, datetime
from . import db

class Student(db.Model):
    __tablename__ = 'Students'

    StudentID = db.Column(db.Integer, primary_key=True)
    StudentName = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Phone = db.Column(db.String(15), nullable=False, unique=True)
    Address = db.Column(db.String(255))
    DOB = db.Column(db.Date)
    Gender = db.Column(db.Enum('Male', 'Female', 'Others'), nullable=False)
    EnrollmentDate = db.Column(db.Date, default=date.today)
    Course = db.Column(db.String(100))
    Year = db.Column(db.Integer)

    allocations = db.relationship('Allocation', back_populates='student', cascade='all, delete-orphan')
    fees = db.relationship('Fee', back_populates='student', cascade='all, delete-orphan')
    complaints = db.relationship('Complaint', back_populates='student', cascade='all, delete-orphan')
    maintenance_requests = db.relationship('MaintenanceRequest', back_populates='requester', cascade='all, delete-orphan')
    visitors = db.relationship('Visitor', back_populates='host_student', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Student {self.StudentName}>"


class Hostel(db.Model):
    __tablename__ = 'Hostels'

    HostelID = db.Column(db.String(1), primary_key=True)
    HostelName = db.Column(db.String(100), nullable=False, unique=True)
    Type = db.Column(db.Enum('Boys', 'Girls', 'Co-ed'), nullable=False)
    WardenID = db.Column(db.Integer, db.ForeignKey('Staff.StaffID', name='fk_hostel_warden', use_alter=True), unique=True)

    rooms = db.relationship('Room', back_populates='hostel', cascade='all, delete-orphan')
    staff = db.relationship('Staff', back_populates='hostel', foreign_keys='Staff.HostelID')

    def __repr__(self):
        return f"<Hostel {self.HostelName}>"


class Staff(db.Model):
    __tablename__ = 'Staff'

    StaffID = db.Column(db.Integer, primary_key=True)
    StaffName = db.Column(db.String(100), nullable=False)
    Role = db.Column(db.Enum('Warden', 'Security', 'Maintenance'), nullable=False)
    Phone = db.Column(db.String(15), nullable=False, unique=True)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    HireDate = db.Column(db.Date, default=date.today)
    HostelID = db.Column(db.String(1), db.ForeignKey('Hostels.HostelID'))

    hostel = db.relationship('Hostel', back_populates='staff', foreign_keys=[HostelID])
    assigned_requests = db.relationship('MaintenanceRequest', back_populates='assigned_staff', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Staff {self.StaffName} - {self.Role}>"


class Room(db.Model):
    __tablename__ = 'Rooms'

    RoomID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RoomNumber = db.Column(db.String(10), nullable=False)
    Floor = db.Column(db.Integer)
    Capacity = db.Column(db.Integer, nullable=False, default=2)
    Occupants = db.Column(db.Integer, nullable=False, default=0)
    Status = db.Column(db.Enum('Vacant', 'Partially Occupied', 'Full', 'Maintenance'), default='Vacant')
    HostelID = db.Column(db.String(1), db.ForeignKey('Hostels.HostelID'), nullable=False)

    hostel = db.relationship('Hostel', back_populates='rooms')
    allocations = db.relationship('Allocation', back_populates='room', cascade='all, delete-orphan')
    maintenance_requests = db.relationship('MaintenanceRequest', back_populates='room', cascade='all, delete-orphan')

    __table_args__ = (db.UniqueConstraint('HostelID', 'RoomNumber', name='uix_hostel_roomnum'),)

    def __repr__(self):
        return f"<Room {self.RoomNumber} - {self.Status}>"


class Allocation(db.Model):
    __tablename__ = 'Allocations'

    AllocationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentID = db.Column(db.Integer, db.ForeignKey('Students.StudentID', ondelete='CASCADE'), nullable=False)
    RoomID = db.Column(db.Integer, db.ForeignKey('Rooms.RoomID', ondelete='CASCADE'), nullable=False)
    StartDate = db.Column(db.Date, nullable=False)
    EndDate = db.Column(db.Date)

    student = db.relationship('Student', back_populates='allocations')
    room = db.relationship('Room', back_populates='allocations')

    def __repr__(self):
        return f"<Allocation Student={self.StudentID} Room={self.RoomID}>"


class Fee(db.Model):
    __tablename__ = 'Fees'

    FeeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentID = db.Column(db.Integer, db.ForeignKey('Students.StudentID'), nullable=False)
    Amount = db.Column(db.Numeric(10, 2), nullable=False)
    DueDate = db.Column(db.Date, nullable=False)
    PaymentDate = db.Column(db.Date)
    Status = db.Column(db.Enum('Paid', 'Unpaid', 'Overdue'), default='Unpaid')

    student = db.relationship('Student', back_populates='fees')

    def __repr__(self):
        return f"<Fee {self.FeeID} - {self.Status}>"


class Complaint(db.Model):
    __tablename__ = 'Complaints'

    ComplaintID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentID = db.Column(db.Integer, db.ForeignKey('Students.StudentID'), nullable=False)
    FiledDate = db.Column(db.DateTime, default=datetime.utcnow)
    Description = db.Column(db.Text, nullable=False)
    Status = db.Column(db.Enum('Open', 'In-Progress', 'Resolved'), default='Open')

    student = db.relationship('Student', back_populates='complaints')

    def __repr__(self):
        return f"<Complaint {self.ComplaintID} - {self.Status}>"


class MaintenanceRequest(db.Model):
    __tablename__ = 'MaintenanceRequests'

    RequestID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RoomID = db.Column(db.Integer, db.ForeignKey('Rooms.RoomID'), nullable=False)
    RequestedBy = db.Column(db.Integer, db.ForeignKey('Students.StudentID'), nullable=False)
    AssignedTo = db.Column(db.Integer, db.ForeignKey('Staff.StaffID'))
    RequestDate = db.Column(db.DateTime, default=datetime.utcnow)
    Status = db.Column(db.Enum('Pending', 'Completed'), default='Pending')

    room = db.relationship('Room', back_populates='maintenance_requests')
    requester = db.relationship('Student', back_populates='maintenance_requests')
    assigned_staff = db.relationship('Staff', back_populates='assigned_requests')

    def __repr__(self):
        return f"<MaintenanceRequest {self.RequestID} - {self.Status}>"


class Visitor(db.Model):
    __tablename__ = 'Visitors'

    VisitorID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), nullable=False)
    Phone = db.Column(db.String(15))
    VisitDate = db.Column(db.Date, default=date.today)
    Purpose = db.Column(db.String(255))
    HostStudentID = db.Column(db.Integer, db.ForeignKey('Students.StudentID'))

    host_student = db.relationship('Student', back_populates='visitors')

    def __repr__(self):
        return f"<Visitor {self.Name}>"



# from datetime import date
# from . import db

# class Student(db.Model):
#     __tablename__ = 'Students'

#     StudentID = db.Column(db.Integer, primary_key=True)
#     StudentName = db.Column(db.String(100), nullable=False)
#     Email = db.Column(db.String(100), nullable=False, unique=True)
#     Phone = db.Column(db.String(15), nullable=False, unique=True)
#     Address = db.Column(db.String(255))
#     DOB = db.Column(db.Date)
#     Gender = db.Column(db.String(10), nullable=False)
#     EnrollmentDate = db.Column(db.Date, default=date.today)
#     Course = db.Column(db.String(100))
#     Year = db.Column(db.Integer)

#     def __repr__(self):
#         return f"<Student {self.StudentName}>"

# class Room(db.Model):
#     __tablename__ = 'Rooms'
#     RoomID = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     RoomNumber = db.Column(db.String(10), nullable=False)
#     Floor = db.Column(db.Integer)
#     Capacity = db.Column(db.Integer, nullable=False, default=2)
#     Occupants = db.Column(db.Integer, nullable=False, default=0)
#     Status = db.Column(db.Enum('Vacant', 'Partially Occupied', 'Full', 'Maintenance'), default='Vacant')
#     HostelID = db.Column(db.String(1), nullable=False)

#     def __repr__(self):
#         return f'<Room {self.RoomNumber} - {self.Status}>'
