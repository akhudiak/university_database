import sqlite3


def execute_query(sql: str) -> list:
    
    with sqlite3.connect("salary.db") as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


sql1 = """
SELECT ROUND(AVG(p.total), 2), e.post
FROM payments AS p
LEFT JOIN employees AS e ON p.employee_id = e.id
GROUP BY e.post;
"""

sql2 = """
SELECT COUNT(*), c.company_name 
FROM employees e
LEFT JOIN companies c ON e.company_id = c.id
GROUP BY c.id;
"""

sql3 = """
SELECT c.company_name, e.employee, e.post, p.total
FROM companies AS c
	LEFT JOIN employees AS e ON e.company_id = c.id
	LEFT JOIN payments AS p ON p.employee_id = e.id
WHERE p.date_of BETWEEN "2023-07-10" AND "2023-07-20"
	AND p.total > 7000;
"""

print(execute_query(sql2))