import typing


from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def get_mentors(cursor: RealDictCursor) -> list:
    query = """
        SELECT first_name, last_name, city
        FROM mentor
        ORDER BY first_name"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_mentors_by_last_name(cursor: RealDictCursor, last_name: str) -> list:
    query = """
            SELECT first_name, last_name, city
            FROM mentor
            WHERE last_name
            LIKE %s
            ORDER BY first_name
            """
    args = last_name
    cursor.execute(query, (args,))
    return cursor.fetchall()


@database_common.connection_handler
def get_mentors_by_city(cursor: RealDictCursor, city_name: str) -> list:
    query = f"""
            SELECT first_name, last_name, city
            FROM mentor
            WHERE city
            LIKE '{city_name}'
            ORDER BY first_name
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_applicant_data_by_name(cursor: RealDictCursor, first_name: str) -> list:
    query = """
                SELECT first_name, last_name, phone_number
                FROM applicant
                WHERE first_name 
                LIKE %s 
                OR last_name LIKE %s
                ORDER BY last_name
                """
    args = first_name, first_name
    cursor.execute(query, args)
    return cursor.fetchall()


@database_common.connection_handler
def get_applicant_data_by_email(cursor: RealDictCursor, email_ending: str) -> list:
    query = """
                SELECT first_name, last_name, phone_number
                FROM applicant
                WHERE email 
                LIKE %s 
                """
    args = '%' + email_ending
    cursor.execute(query, (args,))
    return cursor.fetchall()


@database_common.connection_handler
def get_applicant(cursor: RealDictCursor) -> list:
    query = """
                SELECT *
                FROM applicant
                ORDER BY first_name
                """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_applicant_by_code(cursor: RealDictCursor, code: str) -> list:
    query = """
            SELECT *
            FROM applicant
            WHERE application_code = %s
            """
    args = code
    cursor.execute(query, (args,))
    return cursor.fetchall()


@database_common.connection_handler
def update_phone_number(cursor: RealDictCursor, phone_no: str, code: str) -> list:
    query = """
            UPDATE applicant
            SET phone_number = %s
            WHERE application_code = %s
            """
    args = phone_no, code
    cursor.execute(query, args)
    updated_query = """
            SELECT *
            FROM applicant
            WHERE application_code = %s
            """
    args = code
    cursor.execute(updated_query, (args,))
    return cursor.fetchall()


@database_common.connection_handler
def delete_applicant(cursor: RealDictCursor, code: str) -> list:
    query= """
            DELETE FROM applicant
            WHERE application_code = %s
            """
    args = code
    cursor.execute(query, (args,))
    return "Done"


@database_common.connection_handler
def add_applicant(cursor: RealDictCursor, first_name: str, last_name: str, phone_number: str, email: str) -> list:
    query = """
            INSERT INTO applicant (first_name, last_name, phone_number, email)
            VALUES (%s,%s,%s,%s)   
            """
    args = first_name, last_name, phone_number, email
    cursor.execute(query, args)
    return "Done"


@database_common.connection_handler
def delete_applicant_by_email(cursor: RealDictCursor, email_domain: str) -> list:
    query= """
            DELETE FROM applicant
            WHERE email 
            LIKE %s
            """
    args = '%' + email_domain
    cursor.execute(query, (args,))
    return "Done"


@database_common.connection_handler
def get_max_id(cursor: RealDictCursor) -> list:
    query = """
            SELECT MAX(id)
            FROM applicant
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_application_code_by_id(cursor: RealDictCursor, applicant_id: int) -> list:
    query = """
            SELECT application_code
            FROM applicant
            WHERE id = %s 
            """
    args = applicant_id
    cursor.execute(query, (args,))
    return cursor.fetchall()
