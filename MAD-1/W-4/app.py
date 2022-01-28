from flask import Flask
from flask import render_template
from flask import request
from jinja2 import Template
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import sys
import csv

#comment
#Read the data from csv file to student_data dictionary
def read_csv(filename):
    with open(filename) as f:
        file_data=csv.reader(f)
        headers=next(file_data)
        return [dict(zip(headers,i)) for i in file_data]

student_data = read_csv("data.csv")

student_content = [int(d["Student id"]) for d in student_data]
print(student_content)

course_content = [int(d[" Course id"]) for d in student_data]
print(course_content)


app = Flask(__name__)

@app.route('/',methods=["GET", "POST"])
#Main function

def submit_form():
	new_list = []
	total_marks = 0
	avg_marks = 0
	max_marks = 0
	count = 0
	L = []


	if request.method == "GET":
		return render_template("enter_details.html")


	if request.method == "POST":
		value1 = request.form["ID"]
		userid = int(request.form["id_value"])

		#if studentid button is selected
		if value1 == "studentid":
			for student in student_data:
				if int(userid) not in student_content:
					return render_template("wrong_inputs.html")

				if int(student["Student id"]) == int(userid):
					new_list.append(student)
					total_marks = total_marks + int(student[" Marks"])
					#Render the template using Flask

			return render_template("student_details.html",student_data = new_list,total_marks = total_marks)
					
			
			
		#if courseid button is selected
		if value1 == "courseid":
			for student in student_data:
				
				#if the given input does not match with the course id's present in data.csv
				if int(userid) not in course_content:
					return render_template("wrong_inputs.html")

				#if the given input match with the course id's present in data.csv
				if int(student[" Course id"]) == int(userid):
					new_list.append(student)
					L.append(int(student[" Marks"]))
					total_marks = total_marks + int(student[" Marks"])
					count = count + 1
					max_marks = int(student[" Marks"])
					for student in new_list:
						if max_marks < int(student[" Marks"]):
							max_marks = int(student[" Marks"])

			avg_marks = total_marks/count
		
			#Histogram for selected course
			plt.switch_backend('agg')
			plt.hist(L)
			plt.ylim(0, 1)
			plt.xlabel("Marks")
			plt.ylabel("Frequency")
			plt.savefig('static/my_plot.png')

			

			#Render the template using Flask
			#guided by Manideep Ladi

			return render_template("course_details.html",avg_marks = avg_marks,max_marks= max_marks)
		
	

if __name__ == '__main__':
	app.debug = True
	app.run()
