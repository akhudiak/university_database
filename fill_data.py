import faker
from random import choice, randint
from datetime import datetime
import sqlite3


NUMBER_COMPANIES = 3
NUMBER_EMPLOYEES = 30
NUMBER_POSTS = 5


def generate_fake_data(number_companies, number_employees, number_posts) -> tuple():

    fake_data = faker.Faker("uk-UA")

    fake_companies = []
    fake_employees = []
    fake_posts = []

    for _ in range(number_companies):
        fake_companies.append(fake_data.company())

    for _ in range(number_employees):
        fake_employees.append(fake_data.name())

    for _ in range(number_posts):
        fake_posts.append(fake_data.job())

    return fake_companies, fake_employees, fake_posts


def prepare_data(companies, employees, posts) -> tuple():

    for_companies = []
    for_employees = []
    for_payments = []

    for company in companies:
        for_companies.append((company,))

    for emp in employees:
        for_employees.append((emp, choice(posts), randint(1, NUMBER_COMPANIES)))

    for month in range(1, 12 + 1):
        payment_day = datetime(2023, month, randint(10, 20)).date()
        for emp in range(1, NUMBER_EMPLOYEES + 1):
            for_payments.append((emp, payment_day, randint(1000, 10000)))

    return for_companies, for_employees, for_payments


def insert_data_to_db(companies, employees, payments) -> None:
    
    with sqlite3.connect("salary.db") as con:

        cur = con.cursor()

        sql_to_companies = "INSERT INTO companies(company_name) VALUES (?)"
        cur.executemany(sql_to_companies, companies)

        sql_to_employees = "INSERT INTO employees(employee, post, company_id) VALUES (?, ?, ?)"
        cur.executemany(sql_to_employees, employees)

        sql_to_payments = "INSERT INTO payments(employee_id, date_of, total) VALUES(?, ?, ?)"
        cur.executemany(sql_to_payments, payments)

        con.commit()

companies, employees, posts = generate_fake_data(NUMBER_COMPANIES, NUMBER_EMPLOYEES, NUMBER_POSTS)
companies, employees, payments = prepare_data(companies, employees, posts)
insert_data_to_db(companies, employees, payments)