import faker
from random import choice, randint
from datetime import datetime
import sqlite3


NUMBER_GROUPS = 3
NUMBER_STUDENTS = 30
NUMBER_SUBJECTS = 5
NUMBER_TEACHERS = 3


def generate_fake_data(number_groups, number_students, number_subjects, number_teachers) -> tuple():

    fake = faker.Faker("uk-UA")

    fake_groups = []
    fake_students = []
    fake_subjects = []
    fake_teachers = []

    for _ in range(number_groups):
        fake_groups.append(fake.random_lowercase_letter() + fake.random_lowercase_letter() + "-" + str(fake.random_digit()) + str(fake.random_digit()))

    for _ in range(number_students):
        fake_students.append(fake.passport_owner())

    subjects = ["Math", "Ecomonic", "Programming", "English", "Philosophy", "Science", "Art", "Physical Education", "Geography", "History", "Biology"]
    for _ in range(number_subjects):
        subject = choice(subjects)
        fake_subjects.append(subject)
        subjects.remove(subject)

    for _ in range(number_teachers):
        fake_teachers.append(fake.name())

    return fake_groups, fake_students, fake_subjects, fake_teachers


def prepare_data(groups, students, subjects, teachers) -> tuple():

    fake = faker.Faker("uk-UA")

    for_groups = []
    for_students = []
    for_subjects = []
    for_teachers = []
    for_grades = []

    for group in groups:
        for_groups.append((group,))

    for first_name, last_name in students:
        for_students.append((first_name, last_name, randint(1, NUMBER_GROUPS)))

    for subject in subjects:
        for_subjects.append((subject,  randint(1, NUMBER_TEACHERS)))

    for teacher in teachers:
        for_teachers.append((teacher,))

    for grade in range(20):
        for student in range(1, NUMBER_STUDENTS + 1):
            for_grades.append((student, randint(1, NUMBER_SUBJECTS), randint(1, 5), fake.past_date()))

    return for_groups, for_students, for_subjects, for_teachers, for_grades


def insert_data_to_db(groups, students, subjects, teachers, grades) -> None:
    
    with sqlite3.connect("university.db") as con:

        cur = con.cursor()

        sql_to_groups = "INSERT INTO groups(group_name) VALUES (?)"
        cur.executemany(sql_to_groups, groups)

        sql_to_students = "INSERT INTO students(first_name, last_name, group_id) VALUES (?, ?, ?)"
        cur.executemany(sql_to_students, students)

        sql_to_teachers = "INSERT INTO teachers(teacher) VALUES(?)"
        cur.executemany(sql_to_teachers, teachers)

        sql_to_subjects = "INSERT INTO subjects(subject, teacher_id) VALUES(?, ?)"
        cur.executemany(sql_to_subjects, subjects)

        sql_to_grades = "INSERT INTO grades(student_id, subject_id, grade, date_of) VALUES(?, ?, ?, ?)"
        cur.executemany(sql_to_grades, grades)

        con.commit()


if __name__ == "__main__":
    groups, students, subjects, teachers = generate_fake_data(NUMBER_GROUPS, NUMBER_STUDENTS, NUMBER_SUBJECTS, NUMBER_TEACHERS)
    groups, students, subjects, teachers, grades = prepare_data(groups, students, subjects, teachers)
    insert_data_to_db(groups, students, subjects, teachers, grades)