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


for i in generate_fake_data(NUMBER_GROUPS, NUMBER_STUDENTS, NUMBER_SUBJECTS, NUMBER_TEACHERS):
    print(i)
    print()


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

    for grade in range(20 + 1):
        for student in range(1, NUMBER_STUDENTS + 1):
            for_grades.append((student, randint(1, NUMBER_SUBJECTS + 1), randint(1, 5), fake.past_date()))

    return for_groups, for_students, for_subjects, for_teachers, for_grades


def insert_data_to_db(groups, students, payments) -> None:
    
    with sqlite3.connect("salary.db") as con:

        cur = con.cursor()

        sql_to_groups = "INSERT INTO groups(group_name) VALUES (?)"
        cur.executemany(sql_to_groups, groups)

        sql_to_students = "INSERT INTO students(student, subject, group_id) VALUES (?, ?, ?)"
        cur.executemany(sql_to_students, students)

        sql_to_payments = "INSERT INTO payments(student_id, date_of, total) VALUES(?, ?, ?)"
        cur.executemany(sql_to_payments, payments)

        con.commit()


# if __name__ == "__main__":
#     groups, students, subjects = generate_fake_data(NUMBER_GROUPS, NUMBER_STUDENTS, NUMBER_SUBJECTS)
#     groups, students, payments = prepare_data(groups, students, subjects)
#     insert_data_to_db(groups, students, payments)