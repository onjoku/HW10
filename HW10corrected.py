import prettytable
import unittest,os
from prettytable import PrettyTable
from collections import defaultdict
from hw09 import file_reader


class Repository:
    """ Repository class that hold and implements data structure
    of instructor, students and courses """
    
    def __init__(self, dpath, ptables=True) :
        """ Initialization implementation """
        self.ptables = ptables # preet table flage
        self.dpath = dpath # directory path for all directories in the university - students, instructor, major and grade
        self.instructors = dict()  # self.instructors[instructor_cwid] = Instructor()
        self.students = dict() # self.students[student_cwid] = Student()
        self.majors = dict() # self.majors[major_cwid] = Major()

        #set the getter methods for all instances of university
        self.get_majors(os.path.join(dpath, 'majors.txt'))
        self.get_students(os.path.join(dpath, 'students.txt'))
        self.get_instructors(os.path.join(dpath, 'instructors.txt'))
        self.get_grade(os.path.join(dpath, 'grades.txt'))

        if ptables:
            print('\nStudents Summary')
            self.student_table()

            print('\nInstructors Summary')
            self.instructor_table()

            print('\nMajor Summary')
            self.major_table()
            
            

    def get_majors(self, path):
         """ Read the required course information from path and add to self.students """
         try:
             #read major file and add required and elective courses to the Majorfile
             
            for dept, req,elect in file_reader(path, 3, '\t', False):
                self.majors[dept] = Major(req, elect)
         except ValueError as ex:
             print(ex)
        
                        

    #read the students.txt file and create a student for each row in the file.
    def read_students(self, path):
        """ read each student and add an instance of class Student to self.students """
        for cwid, name, major in file_reader(path, 3, '\t', False):
            self.students[cwid] = Student(cwid, name, major)

    # read the intructors.txt file and create a Instructor for each row in the file
    def read_instructors(self, path):
        """ read each student and add an instance of class Instructor to self.Instructors """
        for cwid, name, dept in file_reader(path, 3, '\t', False):
            self.instructors[cwid] = Instructor(cwid, name, dept)

    # read the major.txt file and create a major remaining courses for row in the file
    def read_major(self, path):
        """ read student's remaining course and add an instance to class major to self.major"""
        for dept, name, major in file_reader(path, 3, '\t', False):
            self.majors[dept].add_courses( name, major)

    def read_grades(self, path):
        """ read each grade and add it to the students and instructor """
        try:
            for student_cwid, course, grade, instructor_cwid in file_reader(path, 3, '\t', False):
                if student_cwid in self.students:
                    self.students[student_cwid].add_course(course, grade)
            else:
                print(f"There was no grade found in '{instructor_cwid}'")
        except ValueError as ex:
            print(ex)
                
    def get_students(self, path):
         """ Read the students information from path and add to self.students """
         try:
             #ask Student to add grades to the file
             
            for cwid,name,major in file_reader(path, 5, '\t', False):
                self.students[cwid] = Student(cwid,name,major)
         except ValueError as ex:
            print(ex)
    
    def get_instructors(self, path):
        """ Read the students information and add to the instructor's file """
        try:
            for cwid, name, major in file_reader(path, 3, sep='\t', header=False):
                self.students[cwid]=Student(cwid, name,major)
        except ValueError as ex:
            print(ex)
            

    def get_grade(self, path):
        """ Read grades and add to both files """
        try:
            for student_cwid, major_dept, grade, instructor_cwid in file_reader(path, 4, '\t', False):
                if student_cwid in self.students:
                    self.students[student_cwid].add_grade( grade)
            else:
                print(f"No grade was found in the student's file")
        except ValueError as ex:
            print(ex)
            self.instructors[instructor_cwid].add_grade(grade)

    def student_table(self):
        """ get the data from each student to populate the pretty table """
        pt = PrettyTable(file_names = ["CWID", "NAME", "COMPLETED COURSES", "REMAINING REQUIRED", "REMIANING ELECTIVES"])
        for student in self.students.values():
            pt.add_row(student.info())
        print(pt)

    #  create instructor prettytable
    def instructor_table(self):
        """ get the data from each instructor to populate the pretty table """
        pt = PrettyTable(file_names=['CWID', 'Name', 'DEPT'])
        for instructor in self.instructors.values():
            pt.add_row(instructor.info())
        print(pt)

    # Create major summary prettytable
    def major_table(self):
        """ populate the pretty table from each major course """
        pt = PrettyTable(file_name=["DEPTS" "REQUIRED", "ELECTIVES"])
        for major in self.majors.values():
            pt.add_row(major.info())
        print(pt)


class Student:
    """ Implementation of student's details information
        by inheriting from base class as argument
    """
    pt_hdr = ["CWID", "NAME", "COMPLETED COURSES", "REMAINING REQUIRED", "REMIANING ELECTIVES"]
    
    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.courses = dict()  # self.courses[course] = grade
        
    def add_grade(self, course, grade):
        """ Adding a course completed to the student's file """
        self.courses[course] = grade    

    def info(self):
        return [self.cwid, self.name, sorted(self.courses.keys())]


class Instructor:
    """ Implementation of Instructor details information  """
    pt_hdr = ["CWID", "NAME", " DEPTs", "COURSE", "STUDENTS"]

    def __init__(self, cwid, name, dept):
        self.cwid = cwid
        self.name = name
        self.dept = dept               
        self.courses = defaultdict(int)  # self.courses[course] = number of students
        
    def add_student(self, course):
        """ Note that another student took a course with this instructor """
        self.courses[course] += 1

    def infor(self):
        return [self.cwid, self.name, sorted(self.courses.keys())]


class Major:
    """ Implementation of student's details information
        by inheriting from base class as argument
    """
    pt_hdr = ["DEPTS" "REQUIRED", "ELECTIVES"]
    def __init__(self, dept, req, courses, elect):
        self.dept = dept
        self.req = req
        self.elect = elect
        self.courses = courses
        
        self.required_courses = set()
        self.electives_courses = set()
        self.majors = dict()  # self.req_courses[dept] = required

    def add_elective_remain(self, req, elect):
        self.req = req
        self.elect = elect
        self.courses[elect] + 1
        if self.elect in self.courses:
            return self.courses[elect]
        else:
            return self.courses[elect] -1
        
        
        
        
    def add_required_remain(self, req, dept):
        """ Adding a required course to the major's file """
        self.majors[req] + 1
        if self.req in self.majors:
            return self.courses.add_required_remain(req, dept)
        else:
            return self.majors[req] -1
        
        
    def completed_course(self, course_cwid, grade, dept):
        """ Completed course in a major course """
        self.courses[course_cwid].add_elect_remain(grade, dept)
        return self.courses[course_cwid]

    def grade(self,grade):
        if self.grade >= 90:
            letter = 'A'
        else:   # grade must be B, C, D or F
            if self.grade >= 80:
                letter = 'B'
            else:  # grade must be C, D or F
                if self.grade >= 70:
                    letter = 'C'
                else:    # grade must D or F
                    if self.grade >= 60:
                        letter = 'F'
                        return letter
                                         
        
        

    def info(self):
        return [self.dept, self.req, sorted(self.courses.keys())]

    def main(self):
        dpath = '/Users/user/AppData/Local/Programs/Python/Python38/HW08work.py'
        stevens = Repository(dpath)

        
        dpath = '/Users/user/AppData/Local/Programs/Python/Python38/HW08work.py'
        nyu = Repository(dpath)       
        dpath = '/Users/user/AppData/Local/Programs/Python/Python38/HW08work.py'
        columbia = Repository(dpath)



         
class RepositoryTest(unittest.TestCase):
    
    def test_stevens(self): 

        dpath ="'/Users/user/AppData/Local/Programs/Python/Python38/HW08work.py" 
        stevens = Repository(dpath)
        expected_student = None
        expected_major = None
        expected_instructor = None

        students = [x.pt_row() for x in stevens.students]
        majors = [k.pt_row() for k in stevens.majors]
        instructors = [i for inst in stevens.instructors.values() for i in instructors ]
        
        self.assertTrue(expected_student, students)
        self.assertEqual(expected_instructor, instructors)
        self.assertEqual(expected_major, majors)
                        
        
        

if __name__=='__main__':
    path = '/Users/user/AppData/Local/Programs/Python/Python38/HW08work.py'
    print(list(file_reader(path, n=3, sep=',', header = False)))
    unittest.main(exit = False, verbosity=2)


def test_Student_attributes(self):

    """ Verify that a specific student is set up properly """
    expected_student = {'10103': ['10103', 'Baldwin, C', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']],
                '10115': ['10115', 'Wyart, X', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']],
                '10172': ['10172', 'Forbes, I', ['SSW 555', 'SSW 567']],
                '10175': ['10175', 'Erickson, D', ['SSW 564', 'SSW567', 'SSW 687']],
                '11788': ['11788', 'Fuller, E', ['SSW 540']]}
    calculated = {cwid:student.pt_row() for cwid, student in self.info.student.items()}
    self.assertEqual(expected_student, calculated)

def test_Instructor_attributes(self):
    """ Verify that a specific instructor is setup properly """
    expected_instructor = {('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4),
                ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3),
                ('98765', 'Feynman, R', 'SFEN', 'SSW 564', 3),
                ('98765', 'Feynman, R', 'SFEN', 'SSW 567', 3),
                ('98765', 'Feynman, R', 'SFEN', 'CS  545', 1),
                ('98765', 'Einstein, A', 'SFEN', 'SSW 501', 1),
                ('98760', 'Darwin, C', 'SYEN', ' SYS 611', 2),
                ('98763', 'Newton, I', 'SFEN', 'SSW 687', 1)}
    calculated = {tuple(detail) for instructor in self.instructors.values() for detail in instructor.pt_rows()}
                          
def test_Major_attributes(self):
    expected_major = {'10103': ['10103', 'Baldwin, C', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']],
                '10115': ['10115', 'Wyart, X', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']],
                '10172': ['10172', 'Forbes, I', ['SSW 555', 'SSW 567']],
                '10175': ['10175', 'Erickson, D', ['SSW 564', 'SSW567', 'SSW 687']],
                '11788': ['11788', 'Fuller, E', ['SSW 540']]}
    calculated = {dept:majors.pt_row() for dept, majors in self.majors.items()}
    self.assertEqual(expected_major, calculated)
 

