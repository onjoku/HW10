import sqlite3
connect = sqlite3.connect('student.db')
CREATE TABLE Instructor_Summary(
    '('CWID INTEGER primary key ,
    NAME  CHARACTER(20),
    DEPT  TEXT,
    COURSE CHARACTER(10),
    STUDENT TEXT')'
);

print("Instructors Summary file")

connect.execute('''CREATE TABLE INSTRUCTOR_SUMMARY
            (CWID INT PRIMARY KEY   NOT NULL,
            NAME              TEXT   NOT NULL,
            DEPT               TEXT  NOT NULL,
            COURSE             TEXT   NOT NULL,
            STUDENT            INT    NOT NULL);''')
print("Instructor's Summary Table was created successfully")

connect.close()
