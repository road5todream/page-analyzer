import os
from page_analyzer.validator import validator
from dotenv import load_dotenv
from .url_parser import parser
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
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DATABASE_URL"] = os.getenv("DATABASE_URL")

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


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
    parsed_url = parser(url_from_form)
    url_id = db.get_url_id(parsed_url)
    return redirect(
        url_for(
            "show_single_url",
            url_id=url_id)
    )


@app.route("/urls/<int:url_id>")
def show_single_url(url_id):
    messages = get_flashed_messages(with_categories=True)
    checks, result = db.get_url_cheks(url_id)

    return render_template(
        "/url.html",
        url=result[0],
        checks=checks,
        messages=messages)


@app.get("/urls")
def show_urls():
    messages = get_flashed_messages(with_categories=True)
    urls = db.get_urls_list()
    return render_template(
        "/urls.html",
        urls=urls,
        messages=messages)


@app.post("/urls/<int:url_id>/checks")
def check_url(url_id):
    db.get_url_check(url_id)
    return redirect(url_for("show_single_url", url_id=url_id))
