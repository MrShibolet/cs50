import os
import random

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session,url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    history = db.execute("SELECT symbol, SUM(shares) total, price FROM history WHERE user_id = %s GROUP BY symbol",session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = %s",session["user_id"])
    cash = cash[0]["cash"]
    return render_template("index.html", history=history, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("invalid symbol", 400)
        shares = request.form.get("shares")
        if not shares.isdigit():
             return apology("Shares should be an int", 400)
        if int(shares) <= 0:
                return apology("can't buy 0 shares or less", 400)
        user = db.execute("SELECT cash FROM users WHERE id = %s",session["user_id"])
        cash = user[0]["cash"]
        price = quote["price"]
        total = int(price) * int(shares)
        if total > cash:
            return apology("Too poor sorry",403)
        else:
            db.execute("UPDATE users SET cash = cash - %s WHERE id = %s",total,session["user_id"])
            db.execute("INSERT INTO history (user_id,symbol,shares,price) VALUES(%s, %s, %s, %s)", session["user_id"], request.form.get("symbol"), shares, price)
            flash("Bought!")
            return redirect(url_for("index"))
    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT symbol, shares, price, created_at FROM history WHERE user_id = %s ORDER BY created_at ASC",session["user_id"])
    return render_template("history.html", history=history)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
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
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("invalid stock symbol",400)
        return render_template("quote.html", stock=stock)
    else:
        return render_template("quotein.html")


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
        return redirect(url_for("index"))
    elif request.method == "GET":
        return render_template("register.html")
    else:
        return apology("Somthing went wrong",502)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("invalid symbol", 400)
        shares = request.form.get("shares")
        if not shares.isdigit():
             return apology("Shares should be an int", 400)
        if int(shares) <= 0:
                return apology("can't sell 0 shares or less", 400)
        available = db.execute("SELECT SUM(shares) total FROM history WHERE user_id = %s and symbol = %s GROUP BY symbol",session["user_id"], request.form.get("symbol"))
        if int(available[0]["total"]) < int(shares)  or int(available[0]["total"]) < 1:
            return apology("Not enough shares",400)
        total = int(shares) * int(quote["price"])
        cash = db.execute("SELECT cash from users where id = %s",session["user_id"])
        total_cash = int(cash[0]["cash"]) + total
        db.execute("UPDATE users SET cash = %s WHERE id = %s",total_cash,session["user_id"])
        db.execute("INSERT INTO history (user_id,symbol,shares,price) VALUES(%s, %s, %s, %s)", session["user_id"], request.form.get("symbol"), -int(shares), int(quote["price"]))
        return redirect(url_for("index"))
    else:
        stocks = db.execute("SELECT symbol, SUM(shares) as total FROM history WHERE user_id = %s GROUP BY symbol",session["user_id"])
        return render_template("sell.html",available=stocks)

@app.route("/gamble", methods=["GET", "POST"])
@login_required
def gamble():
    """gamble money"""
    rand = random.randint(-1000,1000)
    if rand > 0:
        message = "You've gained " + str(rand) + " from that gamble"
    elif rand < 0:
        message = "You've lost" + str(rand) + " from that gambel"
    else:
        message = "It seems like nothing changed, what are the odds?!"
    db.execute("UPDATE users SET cash = cash + %s WHERE id = %s",rand,session["user_id"])
    db.execute("INSERT INTO history (user_id,symbol,shares,price) VALUES(%s, %s, %s, %s)", session["user_id"], "gamble of "+str(rand), 1, int(rand))
    flash(message)
    return redirect(url_for("index"))



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

