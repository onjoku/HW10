from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/instructor_course')
def instructor_courses():
    query = """ SELECT k.CWID, k.Name, Grade, Course, count               (Student_CWID) AS Students
                FROM HW11_grades gd join HW11_instructors k on k.CWID = gd.Instructor_CWID
                GROUP BY k.CWID, k.Name, Grade, Course """



    DBFile = " C:/xampp/mysql/HW11.db "
    dbase = sqlite3.connect(DBFile)
    results = dbase.execute(query)

    data = [{"cwid":cwid, "name":name, "department":department, "course":course, "students": students}
    for cwid, name, department, course, students in  results ]
   
    return render_template('instructor_course.html',
                           title="Stevens Repository",
                           table_title = "Number of Students' by course and instructor",
                           instructors = data)

app.run(debug=True)




