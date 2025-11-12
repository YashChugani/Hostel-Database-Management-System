# app/routes/complaints.py
from flask import render_template, request, redirect, url_for, flash
from app.routes import main_bp
from app import db
from app.models import Complaint, Student

@main_bp.route('/complaints')
def list_complaints():
    comps = Complaint.query.order_by(Complaint.FiledDate.desc()).all()
    return render_template('complaints/list.html', complaints=comps)

@main_bp.route('/complaints/add', methods=['GET', 'POST'])
def add_complaint():
    if request.method == 'POST':
        try:
            complaint = Complaint(
                StudentID=int(request.form.get('StudentID')),
                Description=request.form.get('Description'),
                Status=request.form.get('Status') or 'Open'
            )
            db.session.add(complaint)
            db.session.commit()
            flash('Complaint filed', 'success')
            return redirect(url_for('main.list_complaints'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
    students = Student.query.all()
    return render_template('complaints/form.html', students=students, complaint=None)

@main_bp.route('/complaints/edit/<int:id>', methods=['GET', 'POST'])
def edit_complaint(id):
    c = Complaint.query.get_or_404(id)
    if request.method == 'POST':
        try:
            c.StudentID = int(request.form.get('StudentID'))
            c.Description = request.form.get('Description')
            c.Status = request.form.get('Status')
            db.session.commit()
            flash('Complaint updated', 'success')
            return redirect(url_for('main.list_complaints'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
    students = Student.query.all()
    return render_template('complaints/form.html', students=students, complaint=c)

@main_bp.route('/complaints/delete/<int:id>')
def delete_complaint(id):
    c = Complaint.query.get_or_404(id)
    try:
        db.session.delete(c)
        db.session.commit()
        flash('Complaint deleted', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('main.list_complaints'))
