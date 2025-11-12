# app/routes/allocations.py
from flask import render_template, request, redirect, url_for, flash
from app.routes import main_bp
from app import db
from app.models import Allocation, Student, Room
from datetime import date

@main_bp.route('/allocations')
def list_allocations():
    allocs = Allocation.query.order_by(Allocation.StartDate.desc()).all()
    return render_template('allocations/list.html', allocations=allocs)

def can_allocate(student_id, room_id):
    room = Room.query.get(room_id)
    if not room:
        return False, "Room not found"
    if room.Occupants >= room.Capacity:
        return False, "Room is full"
    active = Allocation.query.filter_by(StudentID=student_id, EndDate=None).first()
    if active:
        return False, "Student already has an active allocation"
    return True, None

@main_bp.route('/allocations/add', methods=['GET', 'POST'])
def add_allocation():
    if request.method == 'POST':
        try:
            student_id = int(request.form.get('StudentID'))
            room_id = int(request.form.get('RoomID'))
            start_date = request.form.get('StartDate') or date.today().isoformat()
            ok, msg = can_allocate(student_id, room_id)
            if not ok:
                flash(msg, 'danger')
                return redirect(url_for('main.list_allocations'))
            alloc = Allocation(StudentID=student_id, RoomID=room_id, StartDate=start_date)
            db.session.add(alloc)
            # increment occupants
            room = Room.query.get(room_id)
            room.Occupants = (room.Occupants or 0) + 1
            if room.Occupants >= room.Capacity:
                room.Status = 'Full'
            elif room.Occupants > 0:
                room.Status = 'Partially Occupied'
            db.session.commit()
            flash('Allocation created', 'success')
            return redirect(url_for('main.list_allocations'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
    students = Student.query.all()
    rooms = Room.query.filter(Room.Status != 'Full').all()
    return render_template('allocations/form.html', students=students, rooms=rooms, allocation=None)

@main_bp.route('/allocations/edit/<int:id>', methods=['GET', 'POST'])
def edit_allocation(id):
    alloc = Allocation.query.get_or_404(id)
    if request.method == 'POST':
        try:
            new_room_id = int(request.form.get('RoomID'))
            if new_room_id != alloc.RoomID:
                # move occupant counts
                old_room = Room.query.get(alloc.RoomID)
                new_room = Room.query.get(new_room_id)
                if new_room.Occupants >= new_room.Capacity:
                    flash('New room is full', 'danger')
                    return redirect(url_for('main.list_allocations'))
                old_room.Occupants = max(0, (old_room.Occupants or 1) - 1)
                if old_room.Occupants == 0:
                    old_room.Status = 'Vacant'
                elif old_room.Occupants < old_room.Capacity:
                    old_room.Status = 'Partially Occupied'
                new_room.Occupants = (new_room.Occupants or 0) + 1
                if new_room.Occupants >= new_room.Capacity:
                    new_room.Status = 'Full'
                elif new_room.Occupants > 0:
                    new_room.Status = 'Partially Occupied'
                alloc.RoomID = new_room_id
            alloc.StartDate = request.form.get('StartDate') or alloc.StartDate
            end = request.form.get('EndDate') or None
            alloc.EndDate = end
            db.session.commit()
            flash('Allocation updated', 'success')
            return redirect(url_for('main.list_allocations'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
    students = Student.query.all()
    rooms = Room.query.all()
    return render_template('allocations/form.html', students=students, rooms=rooms, allocation=alloc)

@main_bp.route('/allocations/delete/<int:id>')
def delete_allocation(id):
    alloc = Allocation.query.get_or_404(id)
    try:
        # decrement occupants
        room = Room.query.get(alloc.RoomID)
        room.Occupants = max(0, (room.Occupants or 1) - 1)
        if room.Occupants == 0:
            room.Status = 'Vacant'
        elif room.Occupants < room.Capacity:
            room.Status = 'Partially Occupied'
        db.session.delete(alloc)
        db.session.commit()
        flash('Allocation removed', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('main.list_allocations'))
