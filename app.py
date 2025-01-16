import sqlite3

from flask import Flask, redirect, render_template, request

app = Flask(__name__)
search_query = None


@app.route("/", methods=["GET"])
def page():
    return redirect("/page")


@app.route("/filter", methods=["GET"])
def filter():
    global search_query
    search_query = request.args.get("q")
    return redirect("/page")


@app.route("/submit", methods=["POST"])
def submit():
    global search_query
    search_query = None
    add_comment(request.form["comment"])
    return redirect("/page")


@app.route("/page")
def render():
    comments = get_comments(search_query)
    return render_template("index.html", comments=comments, search_query=search_query)


def add_comment(comment):
    db = connect_db()
    db.cursor().execute("INSERT INTO comments (comment) " "VALUES (?)", (comment,))
    db.commit()


def get_comments(search_query=None):
    db = connect_db()
    results = []
    get_all_query = "SELECT comment FROM comments"
    for (comment,) in db.cursor().execute(get_all_query).fetchall():
        if search_query is None or search_query in comment:
            results.append(comment)
    return results


def connect_db():
    db = sqlite3.connect("database.db")
    db.cursor().execute(
        "CREATE TABLE IF NOT EXISTS comments "
        "(id INTEGER PRIMARY KEY, "
        "comment TEXT)"
    )
    db.commit()
    return db
