import os
import random

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session,url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookupcraft, lookuplol

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///games.db")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT searched, game, created_at FROM history WHERE user_id = %s ORDER BY created_at DESC",session["user_id"])
    return render_template("history.html", history=history)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide a username", 403)
        elif not request.form.get("password"):
            return apology("must provide a password", 403)
        elif not request.form.get("password") == request.form.get("conf"):
            return apology("passwords do not match", 403)
        olduser = db.execute("SELECT id FROM users WHERE username=%s",(request.form.get("username")))
        if not olduser:
            new_user = db.execute("INSERT INTO users(username,hash) VALUES(%s,%s)",(request.form.get("username"),generate_password_hash(request.form.get("password"))))
        if not new_user:
            return apology("username already taken", 403)
        session["user_id"] = new_user
        flash("Success")
        return redirect(url_for("games"))
    elif request.method == "GET":
        return render_template("register.html")
    else:
        return apology("Something went wrong",502)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Choose a user"""
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Redirect user to home page
        return redirect("/games")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if not session["user_id"]:
        return redirect("/login")
    else:
        return redirect("/games")


@app.route("/games", methods=["GET", "POST"])
@login_required
def games():
    """Search for users in games"""
    if request.method == "POST":
        game = request.form.get("game")
        username = request.form.get("username")
        if game == "League Of Legends":
            user_lol = lookuplol(username)
            if not user_lol:
                return apology("General Error with the API", 400)
            elif user_lol["cc"] != 200:
                name = user_lol["name"]
                flash(f"{name}")
                return redirect(url_for("games"))
            else:
                db.execute("INSERT INTO history (user_id,game,searched) VALUES(%s, %s, %s)", session["user_id"], game, username)
                return render_template("lol.html",info=user_lol)
        elif game == "Minecraft":
            user_mine = lookupcraft(username)
            if not user_mine:
                return apology("General Error with the API", 400)
            elif user_mine["cc"] == 200:
                db.execute("INSERT INTO history (user_id,game,searched) VALUES(%s, %s, %s)", session["user_id"], game, username)
                return render_template("minecraft.html",info=user_mine)
            else:
                name = user_mine["name"]
                flash(f"{name}")
                return redirect(url_for("games"))
        else:
            return apology("Error with game selected", 400)
    else:
        games = db.execute("SELECT * FROM games")
        return render_template("games.html",games=games)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

