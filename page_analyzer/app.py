import os
from urllib.parse import urlparse
from page_analyzer.validator import validator
from dotenv import load_dotenv
import psycopg2
from bs4 import BeautifulSoup
from itertools import zip_longest
import requests
from page_analyzer import db
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    render_template,
    redirect,
    request,
    url_for,
)


app = Flask(__name__)

load_dotenv()
app.config["SECRET_KEY"] = 'sdsdfsf'
app.config["DATABASE_URL"] = os.getenv("DATABASE_URL")




def parse_page(page):
    soup = BeautifulSoup(page, 'html.parser')
    title = soup.find('title').text if soup.find('title') else ''
    h1 = soup.find('h1').text if soup.find('h1') else ''
    description = soup.find('meta', attrs={'name': 'description'})
    if description:
        description = description['content']
    else:
        description = ''
    return {
        'title': title[:255],
        'h1': h1[:255],
        'description': description[:255],
    }


def get_conn():
    return psycopg2.connect(app.config['DATABASE_URL'])


@app.route("/")
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template("index.html", messages=messages)


@app.post("/urls")
def add_url():
    url_from_form = request.form.get("url")
    validated = validator(url_from_form)
    if not validated["result"]:
        flash(validated["message"], "danger")
        messages = get_flashed_messages(with_categories=True)
        return (
            render_template(
                "index.html", url=url_from_form, messages=messages
            ),
            422,
        )
    conn = get_conn()
    url_id = db.get_url_by_name(conn, url_from_form)
    if url_id:
        id = url_id.id
        flash("Страница уже существует", "info")
    else:
        id = db.create_url(conn, url_from_form)
        flash("Страница успешно добавлена", "success")
    conn.close()
    return redirect(
        url_for(
            "show_single_url",
            url_id=id)
    )


@app.route("/urls/<int:url_id>")
def show_single_url(url_id):
    conn = get_conn()
    messages = get_flashed_messages(with_categories=True)
    url = db.get_url_by_id(conn, url_id)
    checks = db.get_checks_by_url_id(conn, url_id)
    conn.close()
    return render_template(
        "/url.html",
        url=url,
        checks=checks,
        messages=messages)


@app.get("/urls")
def show_urls():
    conn = get_conn()
    messages = get_flashed_messages(with_categories=True)
    urls = db.get_urls(conn)
    checks = db.get_url_checks(conn)
    conn.close()
    return render_template(
        "/urls.html",
        data=zip_longest(urls, checks),
        messages=messages)


@app.post("/urls/<int:url_id>/checks")
def check_url(url_id):
    conn = get_conn()
    url = db.get_url_by_id(conn, url_id)
    try:
        response = requests.get(url.name)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash("Произошла ошибка при проверке", "danger")
        conn.close()
        return redirect(
            url_for(
                "show_single_url",
                url_id=url_id
            )
        )
    page = response.text
    data = {'id': url_id,
            'status_code': response.status_code,
            **parse_page(page)}
    db.create_url_check(conn, data)
    flash('Страница успешно проверена', 'success')
    conn.close()
    return redirect(
        url_for(
            "show_single_url",
            url_id=url_id
        )
    )
