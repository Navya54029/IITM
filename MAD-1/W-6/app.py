import os
from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import *
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Template
from flask_restful import Resource, Api
from flask_restful import *
from flask_restful import marshal_with,fields,reqparse
from werkzeug.exceptions import HTTPException
import json



#To get the current directory
curr_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Initialise the path of database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(curr_dir,'api_database.sqlite3')

# Initialise DB
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()
api = Api(app)



#models.py
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
	students  = db.relationship("Student", secondary = 'enrollment')

#Define table 'enrollment'
class Enrollment(db.Model):
	__tablename__ = 'enrollment'
	enrollment_id  = db.Column(db.Integer, primary_key = True, autoincrement = True)
	student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable = False)
	course_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable = False)


#validations.py

class StudentNotFoundError(HTTPException):

	def __init__(self,status_code):
		self.response = make_response('',status_code)


class BusinessValidationError(HTTPException):

	def __init__(self,status_code,error_code,error_message):
		message = {
		"error_code": error_code,
		"error_message": error_message
		}
		self.response = make_response(json.dumps(message),status_code)
		

class StudentExistError(HTTPException):

	def __init__(self,status_code):
		self.response = make_response('',status_code)


class Internalservererror(HTTPException):

	def __init__(self,status_code):
		self.response = make_response('',status_code)


class CourseNotFoundError(HTTPException):

	def __init__(self,status_code):
		self.response = make_response('',status_code)
		

class CourseExistError(HTTPException):

	def __init__(self,status_code):
		self.response = make_response('',status_code)











#Defining output fields using marshal_with
student_output_fields = {
	"student_id" : fields.Integer,
	"first_name" : fields.String,
	"last_name" : fields.String,
	"roll_number" : fields.String
}

course_output_fields = {
	"course_id" : fields.Integer,
	"course_code" : fields.String,
	"course_name" : fields.String,
	"course_description" : fields.String
}


enrollment_output_fields = {
	"enrollment_id" : fields.Integer,
	"student_id" : fields.Integer,
	"course_id" : fields.Integer
}



#To read values from create student POST request Body
create_student_parser = reqparse.RequestParser()
create_student_parser.add_argument('first_name')
create_student_parser.add_argument('last_name')
create_student_parser.add_argument('roll_number',type=str)



#To read values from create course POST request Body
create_course_parser = reqparse.RequestParser()
create_course_parser.add_argument('course_name')
create_course_parser.add_argument('course_code')
create_course_parser.add_argument('course_description',type=str)



#To read values from create course POST request Body
create_enrollment_parser = reqparse.RequestParser()
create_enrollment_parser.add_argument('enrollment_id')
create_enrollment_parser.add_argument('student_id')
create_enrollment_parser.add_argument('course_id')






#api.py

#Define StudentAPI

class StudentAPI(Resource):
	@marshal_with(student_output_fields)


	def get(self,student_id):
		
		#Get the student details
		student = db.session.query(Student).filter(Student.student_id == student_id).first()
		#if student exists in db the return JSON output
		if student:
			return student

		#if course doesn't exist in db
		else:
			raise StudentNotFoundError(status_code = 404)

	@marshal_with(student_output_fields)
	def put(self,student_id):
		
		args = create_student_parser.parse_args()
		first_name = args.get("first_name",None)
		last_name = args.get("last_name",None)
		roll_number = args.get("roll_number",None)
		
		
		# try:
		# To return error responses based on user input
		if roll_number is None or roll_number.isnumeric():
			raise BusinessValidationError(status_code=400,error_code="STUDENT001",error_message="Roll Number is required and should be String")

		if first_name is None or first_name.isnumeric():
			raise BusinessValidationError(status_code=400,error_code="STUDENT002",error_message="First Name is required and should be String")

		if last_name.isnumeric():
			raise BusinessValidationError(status_code=400,error_code="STUDENT003",error_message="Last Name is String")


		existstudent = db.session.query(Student).filter((Student.roll_number == roll_number) | (Student.first_name == first_name)).first()

		if existstudent:
			raise StudentExistError(status_code=409)


		#Get the student details
		student = db.session.query(Student).filter(Student.student_id == student_id).first()
		#if student exists in db the return JSON output
		if student is None: 
			raise StudentNotFoundError(status_code = 404)

		try:

			student = Student.query.filter_by(student_id=student_id).update(dict(roll_number=roll_number,first_name=first_name,last_name=last_name))
			student1 = Student(student_id=student_id,roll_number = roll_number,first_name = first_name,last_name = last_name)
			# print(student1)
			db.session.commit()
			
			return student1,200

		except:
		 
		 raise Internalservererror(status_code=500)

	@marshal_with(student_output_fields)
	def post(self):
		
		args = create_student_parser.parse_args()
		first_name = args.get("first_name",None)
		last_name = args.get("last_name",None)
		roll_number = args.get("roll_number",None)
		
		
		# To return error responses based on user input
		if roll_number is None or roll_number.isnumeric():
			raise BusinessValidationError(status_code=400,error_code="STUDENT001",error_message="Roll Number is required and should be String")

		if first_name is None or first_name.isnumeric():
			raise BusinessValidationError(status_code=400,error_code="STUDENT002",error_message="First Name is required and should be String")

		if last_name.isnumeric():
			raise BusinessValidationError(status_code=400,error_code="STUDENT003",error_message="Last Name is String")


		rollnumberexists = db.session.query(Student).filter(Student.roll_number == roll_number).first()
		# print(rollnumberexists)
		if rollnumberexists:
			raise StudentExistError(status_code=409)

		
		try:
			# Add the entered student details to student table
			newstudent = Student(roll_number = roll_number,first_name = first_name,last_name = last_name)
			db.session.add(newstudent)
			db.session.commit()

			return newstudent,201

		except:
			raise Internalservererror(status_code=500)



	
	def delete(self,student_id):

		student = db.session.query(Student).filter(Student.student_id==student_id).first()

		if student:

			#Delete the student row
			db.session.delete(student)
			db.session.commit()

		else: 
			raise StudentNotFoundError(status_code=404)

		return {},200




#Define CourseAPI

class CourseAPI(Resource):
	
	@marshal_with(course_output_fields)
	def get(self,course_id):
		
			#Get the course details
			course = db.session.query(Course).filter(Course.course_id == course_id).first()
			#if student exists in db the return JSON output
			if course:
				return course

			#if course doesn't exist in db
			else:
				raise CourseNotFoundError(status_code = 404)



	
	@marshal_with(course_output_fields)
	def put(self,course_id):
		
		args = create_course_parser.parse_args()
		course_name = args.get("course_name",None)
		course_code = args.get("course_code",None)
		course_description = args.get("course_description",None)
		# print(course_description,course_name,course_code)

		# To return error responses based on user input
		if course_name is None or course_name.isnumeric():
			raise BusinessValidationError(status_code=400,error_code="COURSE001",error_message="Course Name is required and should be String")

		if course_code is None or course_code.isnumeric():
			raise BusinessValidationError(status_code=400,error_code="COURSE002",error_message="Course Code is required and should be String")

		if course_description.isnumeric():
			raise BusinessValidationError(status_code=400,error_code="COURSE003",error_message="Course Description is String")


		
		course = Course.query.filter_by(course_id=course_id).all()
		l=[]
		for c in course:
			l.append(c.course_code)

		# print(l)
		if course:
			# print("inside internal")
			
			if l[0] == course_code:
				raise Internalservererror(500)
			
		
		#Get the course details
		course = db.session.query(Course).filter(Course.course_id == course_id).first()
		# print(course)
		# course = Course.query.filter_by(course_id=course_id).all()
		
		

		if course is None: 
			# print("insideif")
			raise CourseNotFoundError(status_code = 404)

		else:
			# print("inside")
			course1 = Course.query.filter_by(course_id=course_id).update(dict(course_name=course_name,course_code=course_code,course_description=course_description))
			course2 = Course(course_id=course_id,course_code=course_code,course_name=course_name,course_description=course_description)
			db.session.commit()
			return course2,200

		


		 

	@marshal_with(course_output_fields)
	def post(self):
		
		args = create_course_parser.parse_args()
		course_name = args.get("course_name",None)
		course_code = args.get("course_code",None)
		course_description = args.get("course_description",None)

		# To return error responses based on user input
		if course_name is None or course_name.isnumeric():
			raise BusinessValidationError(status_code=400,error_code="COURSE001",error_message="Course Name is required and should be String")

		if course_code is None or course_code.isnumeric():
			raise BusinessValidationError(status_code=400,error_code="COURSE002",error_message="Course Code is required and should be String")

		if course_description.isnumeric():
			raise BusinessValidationError(status_code=400,error_code="COURSE003",error_message="Course Deescription is String")


		coursecodeexists = db.session.query(Course).filter(Course.course_code == course_code).first()
		# print(rollnumberexists)
		if coursecodeexists:
			raise CourseExistError(status_code=409)

		try: 
			newcourse = Course(course_name=course_name,course_code=course_code,course_description=course_description)
			db.session.add(newcourse)
			db.session.commit()

			return newcourse,201

		except:
			raise Internalservererror(status_code=500)


		
	
	def delete(self,course_id):
		
		#Get the course details
		course = db.session.query(Course).filter(Course.course_id == course_id).all()
		# print(course)
		if course:

			#Delete the course row
			db.session.delete(course)
			db.session.commit()

		else: 
			raise CourseNotFoundError(status_code=404)

		return {},200



#Define CourseAPI

class EnrollmentAPI(Resource):

	@marshal_with(enrollment_output_fields)
	def get(self,student_id):

		# student = db.session.query(Enrollment).filter(Enrollment.student_id==student_id).all()
		studentcourse = Enrollment.query.filter(Enrollment.student_id==student_id).all()
		# print(studentcourse)

		
		if not student_id:
			abort(400,error_code=400,error_message="Invalidstudent")

		if studentcourse:
			l=[]
			for e in studentcourse:
				l.append(dict(enrollment_id=e.enrollment_id,student_id=e.student_id,course_id=e.course_id))
			# print(l)

			return l,200

		else:
			raise StudentNotFoundError(status_code=404)

	def post(self,student_id):

		args = create_enrollment_parser.parse_args()

		course_id = args.get("course_id",None)
		

		course = Course.query.filter(Course.course_id==course_id).first()
		# To return error responses based on user input
		if not course:
			raise BusinessValidationError(status_code=400,error_code="ENROLLMENT001",error_message="Course does not exist")

		
		if student_id is None:
			raise BusinessValidationError(status_code=400,error_code="ENROLLMENT002",error_message="Student does not exist")

		# if course.course_code is None:
		# 	raise BusinessValidationError(status_code=400,error_code="ENROLLMENT003",error_message="Course code is required and should be String")


		
		student = db.session.query(Student).filter(Student.student_id==student_id).first()
		if not student:
			raise StudentNotFoundError(status_code=404)

		else:
	        # Adding the student id and course id in enrollments table
			newenroll = Enrollment(student_id = student_id, course_id = course_id)
			db.session.add(newenroll)
			db.session.commit()
			enroll = Enrollment.query.filter(Enrollment.student_id==student_id).all()
			l=[]
			for e in enroll:
				l.append(dict(enrollment_id=e.enrollment_id,student_id=e.student_id,course_id=e.course_id))
			# print(l)
			return l,201
		
	

	def delete(self,student_id,course_id):

		#Get the course details
		enroll = db.session.query(Enrollment).filter(Enrollment.student_id == student_id).all()
		print(enroll)
		l=[]
		i=0
		for e in enroll:
			l.append(dict(enrollment_id=e.enrollment_id,student_id=e.student_id,course_id=e.course_id))


			if l[i]['student_id']==student_id and l[i]['course_id']==course_id:

				print(e)
				#Delete the course row
				db.session.delete(e)
				db.session.commit()
			i=i+1

		student = Enrollment.query.filter(Enrollment.student_id==student_id).first()
		if not student:
				raise CourseNotFoundError(status_code=404)

		return {},200



	
# Adding API resources

api.add_resource(StudentAPI,"/api/student","/api/student/<int:student_id>")
api.add_resource(CourseAPI,"/api/course","/api/course/<int:course_id>")
api.add_resource(EnrollmentAPI,"/api/student/<int:student_id>/course","/api/student/<int:student_id>/course/<int:course_id>")



if __name__ == '__main__':
	#Run the flask app

	app.run(debug = True)




