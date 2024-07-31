from flask import request, render_template, Blueprint
from .models import Student, Course, Enrollment
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    students = Student.query.all()
    return render_template('home.html', students=students)

@main_bp.route('/student/create', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        roll_number = request.form['roll_number']

        if roll_number in [student.roll_number for student in Student.query.all()]:
            return '''
            Roll number already exists
            <a href="/student/create">Go back</a>
            '''
        else:
            student = Student(first_name=first_name, last_name=last_name, roll_number=roll_number)
            
            course_ids = request.form.getlist('courses')
            
            for course_id in course_ids:
                course = Course.query.get(course_id)
                if course:
                    enrollment = Enrollment(student=student, course=course)
                    db.session.add(enrollment)
            
            db.session.add(student)
            db.session.commit()
            
        return render_template('home.html', students=Student.query.all())
    
    courses = Course.query.all()
    return render_template('create.html', courses=courses)


@main_bp.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update(student_id):
    student = Student.query.get_or_404(student_id)
    courses = Course.query.all()
    enrolled_course_ids = [enrollment.course_id for enrollment in student.enrollments]

    if request.method == 'POST':
        student.first_name = request.form['first_name']
        student.last_name = request.form['last_name']
        student.roll_number = request.form['roll_number']
        
        db.session.query(Enrollment).filter(Enrollment.student_id == student_id).delete()


        course_ids = request.form.getlist('courses')
        student.enrollments.clear()  # Clear current enrollments
        
        for course_id in course_ids:
            course = Course.query.get(course_id)
            if course:
                enrollment = Enrollment(student=student, course=course)
                db.session.add(enrollment)
        
        db.session.commit()
        return render_template('home.html', students=Student.query.all())
    
    return render_template('update.html', student=student, courses=courses, enrolled_course_ids=enrolled_course_ids)


@main_bp.route('/student/<int:student_id>/delete', methods=['GET', 'POST'])
def delete(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        
        db.session.query(Enrollment).filter(Enrollment.student_id == student_id).delete()
        db.session.delete(student)
        db.session.commit()
        return render_template('home.html', students=Student.query.all())
    
    return render_template("areyousure.html",student=student)


@main_bp.route('/student/<int:student_id>/details', methods=['GET'])
def details(student_id):
    student = Student.query.get_or_404(student_id)
    course_ids = db.session.query(Enrollment.course_id).filter(Enrollment.student_id == student_id).all()
    courses =[]
    for course_id in course_ids:
        course = Course.query.filter(Course.course_id == course_id[0]).first()
        courses.append(course)
    
    return render_template('details.html', student=student, courses=courses)


