# app/routes/hostels.py
from flask import render_template, request, redirect, url_for, flash
from app.routes import main_bp
from app import db
from app.models import Hostel, Staff

@main_bp.route('/hostels')
def list_hostels():
    hostels = Hostel.query.all()
    return render_template('hostels/list.html', hostels=hostels)

@main_bp.route('/hostels/add', methods=['GET', 'POST'])
def add_hostel():
    if request.method == 'POST':
        try:
            hid = request.form.get('HostelID').upper()
            name = request.form.get('HostelName')
            htype = request.form.get('Type')
            warden_id = request.form.get('WardenID') or None
            if warden_id:
                warden = Staff.query.get(int(warden_id))
                if not warden or warden.Role != 'Warden':
                    flash('WardenID invalid or not a Warden', 'danger')
                    return redirect(url_for('main.list_hostels'))
            host = Hostel(HostelID=hid, HostelName=name, Type=htype, WardenID=warden_id)
            db.session.add(host)
            db.session.commit()
            flash('Hostel added', 'success')
            return redirect(url_for('main.list_hostels'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding hostel: {e}', 'danger')
    # GET: provide list of wardens to choose from
    wardens = Staff.query.filter_by(Role='Warden').all()
    return render_template('hostels/form.html', wardens=wardens, hostel=None)

@main_bp.route('/hostels/edit/<string:hid>', methods=['GET', 'POST'])
def edit_hostel(hid):
    host = Hostel.query.get_or_404(hid)
    if request.method == 'POST':
        try:
            host.HostelName = request.form.get('HostelName')
            host.Type = request.form.get('Type')
            warden_id = request.form.get('WardenID') or None
            if warden_id:
                warden = Staff.query.get(int(warden_id))
                if not warden or warden.Role != 'Warden':
                    flash('WardenID invalid or not a Warden', 'danger')
                    return redirect(url_for('main.list_hostels'))
            host.WardenID = warden_id
            db.session.commit()
            flash('Hostel updated', 'success')
            return redirect(url_for('main.list_hostels'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating hostel: {e}', 'danger')
    wardens = Staff.query.filter_by(Role='Warden').all()
    return render_template('hostels/form.html', wardens=wardens, hostel=host)

@main_bp.route('/hostels/delete/<string:hid>')
def delete_hostel(hid):
    host = Hostel.query.get_or_404(hid)
    try:
        db.session.delete(host)
        db.session.commit()
        flash('Hostel deleted', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting hostel: {e}', 'danger')
    return redirect(url_for('main.list_hostels'))
