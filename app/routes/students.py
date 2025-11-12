from flask import render_template, request, redirect, url_for, flash
from app.routes import main_bp
from app import db
from app.models import Student

@main_bp.route('/students')
def list_students():
    students = Student.query.all()
    return render_template('students/list.html', students=students)

@main_bp.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        try:
            student = Student(
                StudentName=request.form['name'],
                Email=request.form['email'],
                Phone=request.form['phone'],
                Address=request.form['address'],
                DOB=request.form['dob'],
                Gender=request.form['gender'],
                Course=request.form['course'],
                Year=request.form['year']
            )
            db.session.add(student)
            db.session.commit()
            flash('Student added successfully!', 'success')
            return redirect(url_for('main.list_students'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding student: {e}', 'danger')
    return render_template('students/add.html')

@main_bp.route('/students/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        try:
            student.StudentName = request.form['name']
            student.Email = request.form['email']
            student.Phone = request.form['phone']
            student.Address = request.form['address']
            student.DOB = request.form['dob']
            student.Gender = request.form['gender']
            student.Course = request.form['course']
            student.Year = request.form['year']
            db.session.commit()
            flash('Student updated successfully!', 'success')
            return redirect(url_for('main.list_students'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating student: {e}', 'danger')
    return render_template('students/edit.html', student=student)

@main_bp.route('/students/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting student: {e}', 'danger')
    return redirect(url_for('main.list_students'))

