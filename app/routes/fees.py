# app/routes/fees.py
from flask import render_template, request, redirect, url_for, flash
from app.routes import main_bp
from app import db
from app.models import Fee, Student
from datetime import date

@main_bp.route('/fees')
def list_fees():
    fees = Fee.query.order_by(Fee.DueDate.desc()).all()
    return render_template('fees/list.html', fees=fees)

@main_bp.route('/fees/add', methods=['GET', 'POST'])
def add_fee():
    if request.method == 'POST':
        try:
            student_id = int(request.form.get('StudentID'))
            amount = float(request.form.get('Amount'))
            due_date = request.form.get('DueDate')
            fee = Fee(StudentID=student_id, Amount=amount, DueDate=due_date)
            db.session.add(fee)
            db.session.commit()
            flash('Fee record created', 'success')
            return redirect(url_for('main.list_fees'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
    students = Student.query.all()
    return render_template('fees/form.html', students=students, fee=None)

@main_bp.route('/fees/pay/<int:id>', methods=['POST'])
def pay_fee(id):
    f = Fee.query.get_or_404(id)
    try:
        f.PaymentDate = date.today()
        f.Status = 'Paid'
        db.session.commit()
        flash('Fee marked paid', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('main.list_fees'))

@main_bp.route('/fees/edit/<int:id>', methods=['GET', 'POST'])
def edit_fee(id):
    f = Fee.query.get_or_404(id)
    if request.method == 'POST':
        try:
            f.StudentID = int(request.form.get('StudentID'))
            f.Amount = float(request.form.get('Amount'))
            f.DueDate = request.form.get('DueDate')
            f.PaymentDate = request.form.get('PaymentDate') or None
            f.Status = request.form.get('Status')
            db.session.commit()
            flash('Fee updated', 'success')
            return redirect(url_for('main.list_fees'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
    students = Student.query.all()
    return render_template('fees/form.html', students=students, fee=f)

@main_bp.route('/fees/delete/<int:id>')
def delete_fee(id):
    f = Fee.query.get_or_404(id)
    try:
        db.session.delete(f)
        db.session.commit()
        flash('Fee deleted', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('main.list_fees'))
