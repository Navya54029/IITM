import os
from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import *
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Template


#To get the current directory
curr_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Initialise the path of database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(curr_dir,'database.sqlite3')

# Initialise DB
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

#Define table 'student'
class Student(db.Model):
	__tablename__ = 'student'
	student_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	roll_number = db.Column(db.String, unique = True, nullable = False)
	first_name = db.Column(db.String)
	last_name = db.Column(db.String)

#Define table 'course' with many to many relationship
class Course(db.Model):
	__tablename__ = 'course'
	course_id = db.Column(db.Integer,autoincrement = True, primary_key = True)
	course_code = db.Column(db.String, unique = True, nullable = False)
	course_name = db.Column(db.String, nullable = False)
	course_description = db.Column(db.String)
	#many to many relatonships definition
	students  = db.relationship("Student", secondary = 'enrollments')

#Define table 'enrollments'
class Enrollments(db.Model):
	__tablename__ = 'enrollments'
	enrollment_id  = db.Column(db.Integer, primary_key = True, autoincrement = True)
	estudent_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable = False)
	ecourse_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable = False)



@app.route('/', methods=['GET', 'POST'])
def students():

	if request.method == 'GET':
	
		students = Student.query.all()
		#Returens list of students on Home page
		return(render_template('index.html',students = students))


@app.route('/student/create', methods=['GET', 'POST'])


def addstudentdetails():

	#Reading values from Add Student Form
	r_no = request.form.get('roll')
	f_name = request.form.get('f_name')
	l_name = request.form.get('l_name')
	courses = request.form.getlist('courses')
	

	if request.method == 'GET':
		return(render_template('add_student.html'))

	exist = db.session.query(Student.roll_number).filter(Student.roll_number == r_no).first() is not None
	
	#Check for roll number in Student table exists or not
	if exist:
		return(render_template('error.html'))

	# Executes when entered roll number is not present in student table
	else:

		if request.method == 'POST':
			#Add the entered student details to student table
			newstudent = Student(roll_number = r_no,first_name = f_name,last_name = l_name)
			db.session.add(newstudent)
			db.session.commit()
			
			get_student_id = Student.query.filter_by(roll_number=r_no).all()
			get_s_id = []
			for s in get_student_id:
				get_s_id.append(s.student_id)

			# print(get_s_id)

			# list of courses selected in add student form
			list_courses_sel = []

			for course in courses:
				if course == 'course_1':
					list_courses_sel.append(1)
				elif course == 'course_2':
					list_courses_sel.append(2)
				elif course == 'course_3':
					list_courses_sel.append(3)
				else:
					list_courses_sel.append(4)

			for c in list_courses_sel:
				# Adding the stusent id and course id in enrollments table
				newenroll = Enrollments(estudent_id = get_s_id[0], ecourse_id = c)
				db.session.add(newenroll)
				db.session.commit()

			# Once adding the student to DB is successfull, this will render all the student details in home page
			return redirect(url_for("students"))


@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])

def updatestudent(student_id):
	
	if request.method == 'GET':

		sel_stu = Student.query.filter_by(student_id=student_id).first()
		selected_student = [sel_stu.student_id,sel_stu.roll_number,sel_stu.first_name,sel_stu.last_name]
		# print(selected_student)

		return(render_template('updatestudent.html',student_data = selected_student))

	if request.method == 'POST':

		#Reading values from Add Student Form
		r_no = request.form.get('current_roll')
		f_name = request.form.get('current_f_name')
		l_name = request.form.get('current_l_name')
		courses = request.form.getlist('courses')

		stmt4 = Student.query.filter_by(student_id=student_id).update(dict(first_name=f_name,last_name=l_name))
		db.session.commit()

		# list of courses selected in add student form
		list_courses_sel = []
		for course in courses:
			if course == 'course_1':
				list_courses_sel.append(1)
			elif course == 'course_2':
				list_courses_sel.append(2)
			elif course == 'course_3':
				list_courses_sel.append(3)
			else:
				list_courses_sel.append(4)
		# print(list_courses_sel)
		
		enrolidstmt1 = Enrollments.query.filter_by(estudent_id=student_id).all()
		# print(enrolidstmt1)
		enrollids= []
		for e in enrolidstmt1:
			enrollids.append(e.enrollment_id)
		
		# print(enrollids)
		
		i = 0
		
		if len(courses) == 0:
			#Delete the corresponding enrollments
			enroll_stmt = Enrollments.query.filter_by(estudent_id=student_id).delete()
			db.session.commit()

		else: 
			for c in list_courses_sel:

				try:

					updateenroll1 = Enrollments.query.filter_by(enrollment_id=enrollids[i]).update(dict(ecourse_id=c))
					db.session.commit()
					i = i + 1

					# updateenroll1 = Enrollments.query.filter_by(enrollment_id=enrollids[i]).all()
					# print(updateenroll1)

				#If the student was enrolling for more than courses enrolled previously
				except IndexError:

						# Adding the stusent id and course id in enrollments table
						newenroll = Enrollments(estudent_id = student_id, ecourse_id = c)
						db.session.add(newenroll)
						db.session.commit()

		# Once updating the student to DB is successfull, this will render all the student details in home page
		return redirect(url_for("students"))



@app.route('/student/<int:student_id>/delete')

def deletestudent(student_id):

	if request.method == 'GET':
		
		#Delete the student row
		stu_stmt = Student.query.filter_by(student_id=student_id).delete()
		db.session.commit()

		#Delete the corresponding enrollments
		enroll_stmt = Enrollments.query.filter_by(estudent_id=student_id).delete()
		db.session.commit()
	# Once updating the student to DB is successfull, this will render all the student details in home page
	return redirect(url_for("students"))

		
@app.route('/student/<int:student_id>')				

def display_details(student_id):

	if request.method == 'GET':

		student_data = Student.query.filter_by(student_id=student_id).first()
		course_data = Enrollments.query.filter_by(estudent_id=student_id).all()
		
		course_ids = []
		for c in course_data:
			course_ids.append(c.ecourse_id)

		course_data = []
		for c in course_ids:
			course_data.append(Course.query.filter_by(course_id=c).all())

		
		return(render_template('student_details_page.html',student_data = student_data,course_data = course_data))


if __name__ == '__main__':
	#Run the flask app
	app.run(
		host = '0.0.0.0',
		debug = True,
		port = 8080
		)




