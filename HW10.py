import prettytable, hw09
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
        self.get_grades(os.path.join(dpath, 'grades.txt'))

        if ptables:
            print('\nStudents Summary')
            self.student_table()

            print('\nInstructors Summary')
            self.instructor_table()

            print('\nMajor Summary')
            self.major_table()
            
            

    def get_majors(self, dpath):
         """ Read the required course information from path and add to self.students """
         try:
             #read major file and add required and elective courses to the Majorfile
             
            for major, cwid, courses in file_reader(dpath, 3, '\t', True):
                if major not in self.majors:
                    self.students[cwid] = Student(cwid, courses,major)
         except ValueError as ex:
             print(ex)
    

    
    def get_grades(self, dpath):
        """ Read grades and add to both files """
        try:
            for student_cwid, course, grade, instructor_cwid in file_reader(dpath, 4, '\t', False):
                if student_cwid in self.students:
                    self.students[student_cwid].add_grade(course, grade)
                else:
                    print(f"No student {student_cwid} was found in the student's file")
                if instructor_cwid in self.instructors:
                    self.instructors[instructor_cwid].add_student(course)
                else:
                    print(f" No instructor{instructor_cwid} was found")
        except ValueError as ex:
            print(ex)
            self.instructors[instructor_cwid].add_grade(course)
    def get_students(self, dpath):
         """ Read the students information from path and add to self.students """
         try:
             #ask Student to add grades to the file
             
            for cwid,name,major in file_reader(dpath, 3, '\t', True):
                if major not in self.majors:
                    raise ValueError(f"Student{cwid} took unknown major:{major}")
                self.students[cwid] = Student(cwid,name,self.majors[major])
         except ValueError as ex:
            print(ex)
    
    def get_instructors(self, dpath):
        """ Read the students information and add to the instructor's file """
        try:
            for cwid, name, major in file_reader(dpath, 3, sep='\t', header=False):
                self.students[cwid]=Student(cwid, name,major)
        except ValueError as ex:
            print(ex)      


        
                        

    #read the students.txt file and create a student for each row in the file.
    def read_students(self, dpath):
        """ read each student and add an instance of class Student to self.students """
        for cwid, name, major in file_reader(dpath, 3, '\t', False):
            self.students[cwid] = Student(cwid, name, major)

    # read the intructors.txt file and create a Instructor for each row in the file
    def read_instructors(self, dpath):
        """ read each student and add an instance of class Instructor to self.Instructors """
        for cwid, name, dept in file_reader(dpath, 3, '\t', False):
            self.instructors[cwid] = Instructor(cwid, name, dept)

    # read the major.txt file and create a major remaining courses for row in the file
    def read_majors(self, path):
        """ read student's remaining course and add an instance to class major to self.major"""
        for dept, name, major in file_reader(dpath, 3, '\t', False):
            self.majors[dept].add_courses( name, major)

    def read_grades(self, dpath):
        """ read each grade and add it to the students and instructor """
        try:
            for student_cwid, course, grade, instructor_cwid in file_reader(dpath, 3, '\t', False):
                if student_cwid in self.students:
                    self.students[student_cwid].add_course(course, grade)
            else:
                print(f"There was no grade found in '{instructor_cwid}'")
        except ValueError as ex:
            print(ex)
                
    
    def student_table(self):
        """ get the data from each student to populate the pretty table """
        pt = PrettyTable(field_names = ["CWID", "NAME", "COMPLETED COURSES", "REMAINING REQUIRED", "REMIANING ELECTIVES"])
        for student in self.students.values():
            pt.add_row(student.info())
        print(pt)

    #  create instructor prettytable
    def instructor_table(self):
        """ get the data from each instructor to populate the pretty table """
        pt = PrettyTable(field_names=['CWID', 'Name', 'DEPT', 'Courses'])
        for instructor in self.instructors.values():
            pt.add_row(instructor.info())
        print(pt)

    # Create major summary prettytable
    def major_table(self):
        """ populate the pretty table from each major course """
        pt = PrettyTable(field_names=["DEPTS", "REQUIRED", "ELECTIVES"])
        for major in self.majors.values():
            pt.add_row(major.info())
        print(pt)


class Student:
    """ Implementation of student's details information
        by inheriting from base class as argument
    """
   
    
    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.courses = dict()  # self.courses[course] = grade
        
    def add_grade(self, course, grade):
        """ Adding a course completed to the student's file """
        self.courses[course] = grade    

    def info(self):
        return [self.cwid, self.name,self.major, sorted(self.courses.keys()),self.major.remaining_required(self.courses)]



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
    def __init__(self, dept, required, courses, electives):
        self.dept = dept
        self.required = required
        self.electives = electives
        self.courses = courses
        
        self.required_courses = set()
        self.electives_courses = set()
        self.majors = dict()  # self.req_courses[dept] = required

    def add_elective_remain(self, completed):
        passed = self.courses_passed(completed)
        remain = self.electives
        self.courses[self.electives] + 1
        if self.electives not in self.courses(passed):
            return None
        else:
            return sorted(remain)     
        
    def add_required_remain(self, completed):
        """ Adding a required course to the courses in major's file """
        passed = self.courses_passed( completed)
        remain =self.required - passed
        if remain:
            return sorted(remain)
        else:
            return None
    
    def courses_passed(self, completed):
        """ Completed course in a major courses """
        return {course for course, grade in completed.items() if grade in {'A', 'A-',{'B',{'B-','c'}}}}

    def get_completed(self):
        return self.courses
    
     

    def info(self):
        return [self.dept, self.required, sorted(self.courses.keys())]

    def main(self):
        dpath = 'C:/Users/user/AppData/Local/Programs/Python/Python38/HW08/filetxt.txt'
        stevens = Repository(dpath)

        
        dpath = 'C:/Users/user/AppData/Local/Programs/Python/Python38/HW08/filetxt.txt'
        nyu = Repository(dpath)       
        dpath = 'C:/Users/user/AppData/Local/Programs/Python/Python38/HW08/filetxt.txt'
        columbia = Repository(dpath)



         
class RepositoryTest(unittest.TestCase):

   

    
    def test_stevens(self): 

        dpath = '/Users/user/Documents/students.txt'
        stevens = Repository(dpath)
        expected_student = None
        expected_major = None
        expected_instructor = None

        students = [x.pt_row() for x in stevens.students]
        majors = [k.pt_row() for k in stevens.majors]
        instructors = [i for inst in stevens.instructors.values() for i in stevens.instructors ]
        
        self.assertNotEqual(expected_student, students)
        self.assertNotEqual(expected_instructor, instructors)
        self.assertFalse(expected_major, majors)
                        
        
        

if __name__=='__main__':
    dpath = '/Users/user/Documents/students.txt'
    print(list(file_reader(dpath, n=3, sep=',', header = False)))
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
 

