from jinja2 import Template
import matplotlib.pyplot as plt
import sys
import csv

#Read the data from csv file to student_data dictionary
def read_csv(filename):
    with open(filename) as f:
        file_data=csv.reader(f)
        headers=next(file_data)
        return [dict(zip(headers,i)) for i in file_data]

student_data = read_csv("data.csv")

#Template for Student Data HTML

TEMPLATE1 = """
<!DOCTYPE HTML>
<HTML>
<head>
	<meta charset = "UTF-8"/>
	<title>Student Data</title>
	<style type="text/css">
		.marks {
  				text-align: center;
  				}
	</style>
</head>
<body>
	<h1>Student Details</h1>
	<table border="1px">
		<thead>
			<tr>
				<th>Student id</th>
				<th>Course id</th>
				<th>Marks</th>
			</tr>
		</thead>
		<tbody>
			{% for student in student_data %}
			<tr>
				<td>{{ student['Student id'] }}</td>
				<td>{{ student[' Course id'] }}</td>
				<td>{{ student[' Marks'] }}</td>
			</tr>
			{% endfor %}
			<tr>
				<td class = "marks" colspan = "2">Total Marks</td>
				<td colspan = "3">{{ total_marks }}</td>
			</tr>
		</tbody>
	</table>
</body>
</HTML>"""

#Template for Course Data HTML

TEMPLATE2 = """
<!DOCTYPE HTML>
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Course Data</title>
</head>
<body>
	<h1>Course Details</h1>
	<table border="1px">
		<thead>
			<tr>
				<th>Average Marks</th>
				<th>Maximum Marks</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td>{{ avg_marks }}</td>
				<td>{{ max_marks }}</td>
			</tr>
		</tbody>
	</table>
	<img src = "my_plot.png"/>
</body>
</html>"""

#Template for Wrong Inputs html

TEMPLATE3 = """
<!DOCTYPE HTML>
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Something Went Wrong</title>
</head>
<body>
	<h1>Wrong Inputs</h1>
	<p>Something went wrong</p>
</body>
</html>
"""

#Main function

def main():
	new_list = []
	total_marks = 0
	avg_marks = 0
	max_marks = 0
	count = 0
	L = []


	#if sys argv is -s, then this will show student data
	if sys.argv[1] == '-s':
		for student in student_data:
			if int(student["Student id"]) == int(sys.argv[2]):
				new_list.append(student)
				total_marks = total_marks + int(student[" Marks"])

		#Render the template using Jinja2
		template = Template(TEMPLATE1)
		content = template.render(student_data = new_list,total_marks = total_marks)


	#if sys argv is -c,then this will show course data
	elif sys.argv[1] == '-c':
		for student in student_data:
			if int(student[" Course id"]) == int(sys.argv[2]):
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

		fig = plt.hist(L)
		plt.ylim(0, 1)
		plt.xlabel("Marks")
		plt.ylabel("Frequency")
		plt.savefig('my_plot.png')
		
		#Render the template using Jinja2
		template = Template(TEMPLATE2)
		content = template.render(avg_marks = avg_marks,max_marks= max_marks)


	else:
		template = Template(TEMPLATE3)
		content = template.render()


	#Save the rendered html document
	my_html_document_file = open('output.html','w')
	my_html_document_file.write(content)
	my_html_document_file.close()


	
if __name__ == "__main__":
	#run it if it is only a script
	main()