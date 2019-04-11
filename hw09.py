import prettytable
import unittest
from prettytable import PrettyTable
from collections import defaultdict
from filec import file_reader


class Repository:
    """ Repository class that hold and implements data structure
    of instructor, students and courses """
    
    def __init__(self, path) :
        """ Initialization implementation """
        self.instructors = dict()  # self.instructors[instructor_cwid] = Instructor()
        self.students = dict() # self.students[student_cwid] = Student()

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
             
            for line in file_reader(path, 3, '\t', False):
                self.students[cwid] = Student(cwid,name,major)
         except ValueError as ex:
            print(ex)
    
    def get_instructors(self, path):
        """ Read the students information and add to the instructor's file """
        try:
            for cwid, name, major in file_reader(path, 3, sep='\t', header=False):
                self.students[cwid]=Student(cwid, name, dept)
        except ValueError as ex:
            print(ex)

    def get_grade(self, path):
        """ Read grades and add to both files """
        try:
            for student_cwid, course, grade, instructor_cwid in file_reader(path, 4, '\t', False):
                if student_cwid in self_student:
                    self.students[student_cwid].add_grade(course, grade)
            else:
                print(f"No grade was found in the student's file")
        except ValueError as ex:
            print(ex)
            self.instructors[instructor_cwid].add_grade(course)

    def student_prettytable(self):
        """ get the data from each student to populate the pretty table """
        pt = PrettyTable(file_names = ['CWID', 'Name','Courses Completed'])
        for student in self.students.values():
            pt.add_row(student.info())
        print(pt)

    #  create instructor prettytable
    def instructor_prettytable(self):
        """ get the data from each instructor to populate the pretty table """
        pt = PrettyTable(file_names=['CWID', 'Name', 'DEPT'])
        for instructor in self.instructors.values():
            pt.add_row(instructor.info())
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
        return [self.cwid, self.name, sorted(self.courses.keys())]


class Instructor:
    """ Implementation of Instructor details information  """

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


         
class TestFile_reader(unittest.TestCase):
    def test_file_reader(self):
        path = r" C:/Users/user/AppData/Local/Programs/Python/Python38/HW08/txtfile.txt"
   
        self.assertTrue(Student, expected)
        
        
        

if __name__=='__main__':
    path = r"C:/Users/user/AppData/Local/Programs/Python/Python38/HW08/txtfile.txt"
    print(list(file_reader(path, n=3, sep='|', header = False)))
    expected = {'11658': ['11658','Kelly, P', [ 'SSW 540']],
                 '11461': ['11461','Wright, U', ['CS501', 'SYS 611', 'SYS 750', 'SYS 700']],
                 '10115':['10115','Wyatt, C', ['CS501', 'SSW564', 'SSW 567', 'SSW 687']],
                 '10183':['10183','Chapman, O', ['SSW 689']],
                 '10103':['10103','Baldwin, C', ['CS501', 'SSW564', 'SSW 567', 'SSW 687']],
                 '10175':['10175','Erickson, D', ['SSW 564', 'SSW 567', 'SSW 687']],
                 '11714':['11714','Morton, A', ['SYS 611', 'SYS 645']]}
    unittest.main(exit = False, verbosity=2)
