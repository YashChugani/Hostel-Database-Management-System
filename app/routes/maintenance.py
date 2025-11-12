# app/routes/maintenance.py
from flask import render_template, request, redirect, url_for, flash
from app.routes import main_bp
from app import db
from app.models import MaintenanceRequest, Room, Student, Staff

@main_bp.route('/maintenance')
def list_maintenance():
    reqs = MaintenanceRequest.query.order_by(MaintenanceRequest.RequestDate.desc()).all()
    return render_template('maintenance/list.html', requests=reqs)

@main_bp.route('/maintenance/add', methods=['GET', 'POST'])
def add_maintenance():
    if request.method == 'POST':
        try:
            room_id = int(request.form.get('RoomID'))
            requested_by = int(request.form.get('RequestedBy'))
            assigned_to = request.form.get('AssignedTo') or None
            mr = MaintenanceRequest(RoomID=room_id, RequestedBy=requested_by, AssignedTo=assigned_to)
            db.session.add(mr)
            db.session.commit()
            flash('Maintenance request created', 'success')
            return redirect(url_for('main.list_maintenance'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
    rooms = Room.query.all()
    students = Student.query.all()
    staff = Staff.query.filter_by(Role='Maintenance').all()
    return render_template('maintenance/form.html', rooms=rooms, students=students, staff=staff, req=None)

@main_bp.route('/maintenance/edit/<int:id>', methods=['GET', 'POST'])
def edit_maintenance(id):
    r = MaintenanceRequest.query.get_or_404(id)
    if request.method == 'POST':
        try:
            r.RoomID = int(request.form.get('RoomID'))
            r.RequestedBy = int(request.form.get('RequestedBy'))
            r.AssignedTo = request.form.get('AssignedTo') or None
            r.Status = request.form.get('Status')
            db.session.commit()
            flash('Request updated', 'success')
            return redirect(url_for('main.list_maintenance'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
    rooms = Room.query.all()
    students = Student.query.all()
    staff = Staff.query.filter_by(Role='Maintenance').all()
    return render_template('maintenance/form.html', rooms=rooms, students=students, staff=staff, req=r)

@main_bp.route('/maintenance/delete/<int:id>')
def delete_maintenance(id):
    r = MaintenanceRequest.query.get_or_404(id)
    try:
        db.session.delete(r)
        db.session.commit()
        flash('Request deleted', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('main.list_maintenance'))
