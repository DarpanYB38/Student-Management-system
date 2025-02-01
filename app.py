from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(50), nullable=False, unique=True)
    grades = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'

    def get_average(self):
        try:
            grade_list = [int(grade) for grade in self.grades.split(',')]
            return sum(grade_list) / len(grade_list) if len(grade_list) > 0 else 0
        except ValueError:
            return 0

# Home Page - List Students
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

# Add Student
@app.route('/add', methods=['POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        student_id = request.form['student_id']
        grades = request.form['grades']
        
        # Create a new student record
        new_student = Student(name=name, student_id=student_id, grades=grades)
        
        # Add to the database session and commit
        db.session.add(new_student)
        db.session.commit()
        
        return redirect(url_for('index'))


# Edit Student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get(id)
    if not student:
        return "Student not found", 404

    if request.method == 'POST':
        student.name = request.form['name']
        student.student_id = request.form['student_id']
        student.grades = request.form['grades']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_student.html', student=student)

# Delete Student
@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()
    return redirect(url_for('index'))

# Run the App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables within app context
    app.run(debug=True)
