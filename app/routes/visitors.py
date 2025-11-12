# app/routes/visitors.py
from flask import render_template, request, redirect, url_for, flash
from app.routes import main_bp
from app import db
from app.models import Visitor, Student
from datetime import date

@main_bp.route('/visitors')
def list_visitors():
    visitors = Visitor.query.order_by(Visitor.VisitDate.desc()).all()
    return render_template('visitors/list.html', visitors=visitors)

@main_bp.route('/visitors/add', methods=['GET', 'POST'])
def add_visitor():
    if request.method == 'POST':
        try:
            v = Visitor(
                Name=request.form.get('Name'),
                Phone=request.form.get('Phone'),
                VisitDate=request.form.get('VisitDate') or date.today(),
                Purpose=request.form.get('Purpose'),
                HostStudentID=int(request.form.get('HostStudentID')) if request.form.get('HostStudentID') else None
            )
            db.session.add(v)
            db.session.commit()
            flash('Visitor added', 'success')
            return redirect(url_for('main.list_visitors'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
    students = Student.query.all()
    return render_template('visitors/form.html', students=students, visitor=None)

@main_bp.route('/visitors/edit/<int:id>', methods=['GET', 'POST'])
def edit_visitor(id):
    v = Visitor.query.get_or_404(id)
    if request.method == 'POST':
        try:
            v.Name = request.form.get('Name')
            v.Phone = request.form.get('Phone')
            v.VisitDate = request.form.get('VisitDate')
            v.Purpose = request.form.get('Purpose')
            v.HostStudentID = int(request.form.get('HostStudentID')) if request.form.get('HostStudentID') else None
            db.session.commit()
            flash('Visitor updated', 'success')
            return redirect(url_for('main.list_visitors'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
    students = Student.query.all()
    return render_template('visitors/form.html', students=students, visitor=v)

@main_bp.route('/visitors/delete/<int:id>')
def delete_visitor(id):
    v = Visitor.query.get_or_404(id)
    try:
        db.session.delete(v)
        db.session.commit()
        flash('Visitor deleted', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('main.list_visitors'))
