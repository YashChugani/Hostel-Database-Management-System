# from flask import render_template
# from app.routes import main_bp
# from app.models import db, Student, Hostel, Staff, Room, Allocation, Fee, Complaint, MaintenanceRequest, Visitor

# @main_bp.route('/')
# def dashboard():
#     data = {
#         "students": Student.query.count(),
#         "hostels": Hostel.query.count(),
#         "staff": Staff.query.count(),
#         "rooms": Room.query.count(),
#         "allocations": Allocation.query.count(),
#         "fees": Fee.query.count(),
#         "complaints": Complaint.query.count(),
#         "maintenance": MaintenanceRequest.query.count(),
#         "visitors": Visitor.query.count()
#     }
#     return render_template('dashboard.html', data=data)


from flask import render_template
from app.routes import main_bp
from app.models import Student, Room, Hostel, Fee, Complaint, MaintenanceRequest as Maintenance, Allocation, Visitor, Staff
from app import db

@main_bp.route('/')
@main_bp.route('/dashboard')
def dashboard():
    data = {
        'Total Students': Student.query.count(),
        'Total Rooms': Room.query.count(),
        'Total Hostels': Hostel.query.count(),
        'Total Staff': Staff.query.count(),
        'Active Allocations': Allocation.query.count(),
        'Pending Complaints': Complaint.query.filter_by(Status='Pending').count(),
        'Maintenance Requests': Maintenance.query.count(),
        'Total Visitors': Visitor.query.count(),
        'Fees Collected': db.session.query(db.func.coalesce(db.func.sum(Fee.Amount), 0))\
                            .filter(Fee.Status=='Paid').scalar()

    }

    # Aggregated data for charts
    rooms_per_hostel = db.session.query(Hostel.HostelName, db.func.count(Room.RoomID)) \
                                 .join(Room, Hostel.HostelID == Room.HostelID) \
                                 .group_by(Hostel.HostelName).all()

    students_per_hostel = db.session.query(
                                    Hostel.HostelName,
                                    db.func.count(Allocation.AllocationID)
                                ) \
                                .join(Room, Hostel.HostelID == Room.HostelID) \
                                .join(Allocation, Room.RoomID == Allocation.RoomID) \
                                .group_by(Hostel.HostelName).all()
    
    # Fee status distribution
    fee_status_data = db.session.query(Fee.Status, db.func.count(Fee.FeeID))\
        .group_by(Fee.Status).all()

    # Complaint status distribution
    complaint_status_data = db.session.query(Complaint.Status, db.func.count(Complaint.ComplaintID))\
        .group_by(Complaint.Status).all()

    # Staff roles distribution
    staff_roles_data = db.session.query(Staff.Role, db.func.count(Staff.StaffID))\
        .group_by(Staff.Role).all()

    # Allocations per Room (to see occupancy)
    allocations_per_room = db.session.query(Room.RoomNumber, db.func.count(Allocation.AllocationID))\
        .join(Allocation, Room.RoomID == Allocation.RoomID, isouter=True)\
        .group_by(Room.RoomNumber).all()


    return render_template(
    'dashboard.html',
    data=data,
    rooms_per_hostel=rooms_per_hostel,
    students_per_hostel=students_per_hostel,
    fee_status_data=fee_status_data,
    complaint_status_data=complaint_status_data,
    staff_roles_data=staff_roles_data,
    allocations_per_room=allocations_per_room
)

