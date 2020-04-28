import os
import requests
import urllib.parse
import datetime

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookupcraft(symbol):
    """Look up quote for symbol."""

    # Contact API
    response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{urllib.parse.quote_plus(symbol)}")
    # Parse response
    if response.status_code == 204:
        return{
            "cc": 204,
            "name": "No player with the given username"}
    elif response.status_code != 200:
        quote = response.json()
        return{
            "cc":  response.status_code,
            "name": quote["errorMessage"]
        }
    else:
        quote = response.json()
        uid = quote["id"]
        response2 = requests.get(f"https://api.mojang.com/user/profiles/{urllib.parse.quote_plus(uid)}/names")
        quote2 = response2.json()
        user = quote2[0]["name"]
        if len(quote2) < 2:
            change = "Never changed"
        else:
            change = quote2[1]["changedToAt"]
            change = datetime.datetime.fromtimestamp(change/1000.0)
        if quote2[0]["name"] == "":
            user = 'No previous username'
            change = "N/A"
        return{
            "cc": int(response.status_code),
            "name": str(user) ,
            "changedToAt": change
        }

def lookuplol(symbol):
    """Look up username with riot api."""
    # Contact API
    #need to regenerate key before running
    api_key = "RGAPI-7841e9e8-fd38-4cdd-ad70-7f2173ab5a97"
    summoner_id = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/"
    URL = "{}by-name/{}?api_key={}".format(summoner_id,symbol,api_key)
    response = requests.get(URL)
    quote = response.json()
    print(f"{response.status_code}")
    if response.status_code == 200:
        return {
            "cc": response.status_code,
            "name": quote["name"],
            "summonerLevel": float(quote["summonerLevel"])}
    else:
        return {
            "cc": response.status_code,
            "name": quote["status"]["message"] }

