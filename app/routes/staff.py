# app/routes/staff.py
from flask import render_template, request, redirect, url_for, flash
from app.routes import main_bp
from app import db
from app.models import Staff, Hostel

@main_bp.route('/staff')
def list_staff():
    staff = Staff.query.all()
    return render_template('staff/list.html', staff=staff)

@main_bp.route('/staff/add', methods=['GET', 'POST'])
def add_staff():
    if request.method == 'POST':
        try:
            s = Staff(
                StaffName=request.form.get('StaffName'),
                Role=request.form.get('Role'),
                Phone=request.form.get('Phone'),
                Email=request.form.get('Email'),
                HostelID=request.form.get('HostelID') or None
            )
            db.session.add(s)
            db.session.commit()
            flash('Staff added', 'success')
            return redirect(url_for('main.list_staff'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
    hostels = Hostel.query.all()
    return render_template('staff/form.html', hostels=hostels, staff=None)

@main_bp.route('/staff/edit/<int:id>', methods=['GET', 'POST'])
def edit_staff(id):
    s = Staff.query.get_or_404(id)
    if request.method == 'POST':
        try:
            s.StaffName = request.form.get('StaffName')
            s.Role = request.form.get('Role')
            s.Phone = request.form.get('Phone')
            s.Email = request.form.get('Email')
            s.HostelID = request.form.get('HostelID') or None
            db.session.commit()
            flash('Staff updated', 'success')
            return redirect(url_for('main.list_staff'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
    hostels = Hostel.query.all()
    return render_template('staff/form.html', hostels=hostels, staff=s)

@main_bp.route('/staff/delete/<int:id>')
def delete_staff(id):
    s = Staff.query.get_or_404(id)
    try:
        db.session.delete(s)
        db.session.commit()
        flash('Staff deleted', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('main.list_staff'))
