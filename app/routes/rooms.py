from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import Room, Hostel
from app.routes import main_bp

@main_bp.route('/rooms')
def list_rooms():
    rooms = Room.query.all()
    hostels = Hostel.query.all()
    return render_template('rooms/list.html', rooms=rooms, hostels=hostels)

@main_bp.route('/rooms/add', methods=['POST'])
def add_room():
    room_number = request.form.get('RoomNumber')
    floor = request.form.get('Floor')
    capacity = request.form.get('Capacity')
    hostel_id = request.form.get('HostelID')

    new_room = Room(RoomNumber=room_number, Floor=floor, Capacity=capacity, HostelID=hostel_id)
    db.session.add(new_room)
    db.session.commit()
    flash('Room added successfully!')
    return redirect(url_for('main.list_rooms'))

@main_bp.route('/rooms/edit/<int:id>', methods=['GET', 'POST'])
def edit_room(id):
    room = Room.query.get_or_404(id)
    hostels = Hostel.query.all()
    if request.method == 'POST':
        room.RoomNumber = request.form.get('RoomNumber')
        room.Floor = request.form.get('Floor')
        room.Capacity = request.form.get('Capacity')
        room.HostelID = request.form.get('HostelID')
        db.session.commit()
        flash('Room updated successfully!')
        return redirect(url_for('main.list_rooms'))
    return render_template('rooms/edit.html', room=room, hostels=hostels)

@main_bp.route('/rooms/delete/<int:id>')
def delete_room(id):
    room = Room.query.get_or_404(id)
    db.session.delete(room)
    db.session.commit()
    flash('Room deleted successfully!')
    return redirect(url_for('main.list_rooms'))

@main_bp.route('/rooms/api')
def rooms_api():
    rooms = Room.query.all()
    return jsonify([{
        "RoomID": r.RoomID,
        "RoomNumber": r.RoomNumber,
        "Status": r.Status,
        "Capacity": r.Capacity,
        "Occupants": r.Occupants,
        "HostelID": r.HostelID
    } for r in rooms])
