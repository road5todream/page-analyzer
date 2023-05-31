from psycopg2.extras import NamedTupleCursor
from datetime import datetime


def get_urls(conn):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            "SELECT * FROM urls ORDER BY id DESC;",
        )
        urls = curs.fetchall()
    return urls


def get_url_checks(conn):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            """SELECT DISTINCT ON (url_id) * FROM
            url_checks ORDER BY url_id DESC, id DESC;"""
        )
        checks = curs.fetchall()
    return checks


def get_url_by_name(conn, url):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            'SELECT id, name FROM urls WHERE name=%s',
            (url,),
        )
        existed_url = curs.fetchone()
    return existed_url


def create_url(conn, url):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            """INSERT INTO urls (name, created_at)
            VALUES (%s, %s)
            RETURNING id;""",
            (url, datetime.today())
        )
        id = curs.fetchone().id

    conn.commit()
    return id


def get_url_by_id(conn, id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            'SELECT * FROM urls WHERE id = %s',
            (id,),
        )
        url = curs.fetchone()
        return url


def get_checks_by_url_id(conn, url_id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as checks:
        checks.execute(
            "SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC;",
            (url_id,)
        )
        checks = checks.fetchall()
    return checks


def create_url_check(conn, check_data):
    with conn.cursor(cursor_factory=NamedTupleCursor) as check_curs:
        check_curs.execute(
            """INSERT INTO url_checks (url_id, status_code,
            h1, title, description, created_at)
            VALUES (%s, %s, %s, %s, %s, %s);""",
            (check_data['id'], check_data['status_code'],
             check_data['h1'], check_data['title'],
             check_data['description'], datetime.today()),
        )
    conn.commit()
