import os
import requests

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps


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


# Configure session to use filesystem
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure SQL database
db = SQL("sqlite:///crypto.db")


# Login required decorator function
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# API KEY
API = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"


# Function to fetch a list of all the symbols of supported cryptocurrencies
def fetchSymbols():
    portfolio = []

    cryptocurrency = requests.get(API)
    cryptocurrencies = cryptocurrency.json()

    for i in range(len(cryptocurrencies)):
        portfolio.append(cryptocurrencies[i]["symbol"].upper())

    return portfolio


# Function to fetch the price of a cryptocurrency
def fetchCurrentPrice(symbol):
    cryptocurrency = requests.get(API)
    cryptocurrencies = cryptocurrency.json()

    for i in range(len(cryptocurrencies)):
        if (symbol.casefold() == cryptocurrencies[i]["symbol"].casefold()):
            return cryptocurrencies[i]["current_price"]


# Function to fetch the name of a cryptocurrency
def fetchName(symbol):
    cryptocurrency = requests.get(API)
    cryptocurrencies = cryptocurrency.json()

    for i in range(len(cryptocurrencies)):
        if (symbol.casefold() == cryptocurrencies[i]["symbol"].casefold()):
            return cryptocurrencies[i]["name"]


# Function to fetch the image url of a cryptocurrency
def fetchImage(symbol):
    cryptocurrency = requests.get(API)
    cryptocurrencies = cryptocurrency.json()

    for i in range(len(cryptocurrencies)):
        if (symbol.casefold() == cryptocurrencies[i]["symbol"].casefold()):
            return cryptocurrencies[i]["image"]


# All the routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/live")
def live():
    return render_template("live.html")


@app.route("/news")
def news():
    news = requests.get("https://api.coinstats.app/public/v1/news/trending?skip=0&limit=20")
    newsDictionary = news.json()
    return render_template("news.html", news=newsDictionary['news'])


@app.route("/login", methods=["GET", "POST"])
def login():
    # Clear user
    session.clear()

    # Submit Form using POST
    if request.method == "POST":

        invalid = "Invalid Username and/or Password"

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", invalid=invalid)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", invalid=invalid)

        # Search database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", invalid=invalid)

        # Remember user ID
        session["user_id"] = rows[0]["id"]

        # Redirect user to the dashboard
        return redirect("/dashboard")

    # GET
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # Form
    if request.method == "POST":
        # Error checking
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        year = request.form.get("year")
        USERNAMES = db.execute("SELECT username FROM users")

        # If username is blank
        if not username:
            return render_template("register.html", invalid="Invalid Username")
        # If username already in database
        for entry in USERNAMES:
            if username == entry["username"]:
                return render_template("register.html", invalid="Username already registered")
        # If password is blank
        if not password:
            return render_template("register.html", invalid="Invalid password")
        # If passwords do not match
        if password != confirmation:
            return render_template("register.html", invalid="Passwords do not match")
        # If year is blank
        if not year:
            return render_template("register.html", invalid="Invalid Date of Birth")

        # Insert the registrants info into the user database
        db.execute("INSERT INTO users (username, hash, year) VALUES(?, ?, ?)", username, generate_password_hash(password), year)
        return redirect("/login")

    # Reaching this page via GET or clicking the link
    else:
        return render_template("register.html")


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    # Define a portfolio and an entry variable
    portfolio = []
    entry = {}

    # Get userID and print out all the coins that they have
    userID = session["user_id"]

    entries = db.execute("SELECT * FROM holdings WHERE user_id = ?", userID)

    # POST method to delete an entry
    if request.method == "POST":
        key = int(request.form.get("id"))

        # Update the history database with the changes in the data then delete it
        old = db.execute("SELECT * FROM holdings WHERE user_id = ? AND id = ?", userID, key)

        symbol = old[0]["symbol"]
        holdings = old[0]["holdings"]
        price = old[0]["price"]
        value = "{:.2f}".format(price * holdings)

        db.execute("INSERT INTO history (user_id, symbol, oldHoldings, oldPrice, oldValue, type) VALUES(?, ?, ?, ?, ?, ?)",
                   userID, symbol, holdings, price, value, "REMOVE")

        db.execute("DELETE FROM holdings WHERE user_id = ? AND id = ?", userID, key)
        return redirect("/dashboard")

    # GET method to display all the cryptocurrencies
    else:
        # Iterate through the entries list and append all the values required in the table dashboard
        for i in range(len(entries)):
            entry.clear()
            entry["rank"] = i + 1
            entry["id"] = entries[i]["id"]
            entry["image"] = fetchImage(entries[i]["symbol"])
            entry["symbol"] = entries[i]["symbol"]
            entry["name"] = fetchName(entries[i]["symbol"])
            entry["holdings"] = entries[i]["holdings"]
            entry["oldPrice"] = entries[i]["price"]

            # Get the value that they deposited in
            value = entries[i]["price"] * entries[i]["holdings"]
            entry["value"] = "{:.2f}".format(value)

            # Get the current price of the coin
            currentPrice = fetchCurrentPrice(entries[i]["symbol"])
            entry["price"] = currentPrice
            entry["currentValue"] = "{:.2f}".format(currentPrice * entries[i]["holdings"])

            # Do the math to calculate the profits and % change
            profit = (currentPrice * entries[i]["holdings"]) - value
            entry["profit"] = "{:.2f}".format(profit)

            entry["percentage"] = "{:.2f}".format((profit / value) * 100)

            # Append all the data into the portfolio as one list
            portfolio.append(entry.copy())

        # Calculate the total profits and the total percentage change in the value
        totalProfits = 0
        totalValue = 0
        currentValue = 0
        for i in range(len(portfolio)):
            totalProfits += float(portfolio[i]["profit"])
            totalValue += float(portfolio[i]["value"])
            currentValue += float(portfolio[i]["currentValue"])

        if totalValue == 0:
            totalPercentage = 0
        else:
            totalPercentage = "{:.2f}".format((totalProfits / totalValue) * 100)

        # Update the portfolio so that theres no 0 entries
        for i in range(len(portfolio)):
            if portfolio[i]["holdings"] == 0:
                del portfolio[i]
                db.execute("DELETE FROM holdings WHERE holdings = 0")
                break

        return render_template("dashboard.html", portfolio=portfolio, value="{:.2f}".format(totalValue), currentValue="{:.2f}".format(currentValue), profits="{:.2f}".format(totalProfits), percentageDifference=totalPercentage)


@app.route("/logout")
def logout():
    # Forget user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    # Inputted the cryptocurrency via the form
    if request.method == "POST":
        # Error checking for all the inputted values
        # Symbol of the cryptocurrency
        symbol = request.form.get("symbol").upper()
        allSymbols = fetchSymbols()

        if not symbol:
            return render_template("add.html", information="Input Symbol")
        if symbol not in allSymbols:
            return render_template("add.html", information="Invalid Symbol")

        # Holdings
        holdings = request.form.get("holdings")
        if not holdings:
            return render_template("add.html", information="Input Holdings")
        try:
            float(holdings)
        except ValueError:
            return render_template("add.html", information="Invalid Holdings")
        else:
            holdings = float(holdings)

        # Price
        price = request.form.get("price")
        if not price:
            return render_template("add.html", information="Input Price")
        try:
            float(price)
        except ValueError:
            return render_template("add.html", information="Invalid Price")
        else:
            price = float(price)

        userID = session["user_id"]

        db.execute("INSERT INTO holdings (user_id, holdings, symbol, price) VALUES(?, ?, ?, ?)", userID, holdings, symbol, price)

        # Insert into the history database the relevant values
        db.execute("INSERT INTO history (user_id, symbol, newHoldings, newPrice, newValue, type) VALUES(?, ?, ?, ?, ?, ?)",
                   userID, symbol, holdings, price, "{:.2f}".format(holdings * price), "ADD")

        return redirect("/dashboard")

    # GET method
    else:
        return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    # Get userID
    userID = session["user_id"]

    # Get the cryptocurrencies that the user currently owns
    portfolio = db.execute("SELECT * FROM holdings WHERE user_id = ?", userID)

    # POST method
    if request.method == "POST":
        # Error checking

        owned = []

        # Symbol
        symbolID = request.form.get("id")
        if not symbolID:
            return render_template("edit.html", information="Select Symbol")
        else:
            symbolID = int(symbolID)
        for crypto in portfolio:
            owned.append(crypto["id"])
        if symbolID not in owned:
            return render_template("edit.html", information="Invalid Symbol")

        # Holdings
        holdings = request.form.get("holdings")
        if not holdings:
            return render_template("edit.html", information="Input Holdings")
        try:
            float(holdings)
        except ValueError:
            return render_template("edit.html", information="Invalid Holdings")
        else:
            holdings = float(holdings)

        # Price
        price = request.form.get("price")
        if not price:
            return render_template("edit.html", information="Input Price")
        try:
            float(price)
        except ValueError:
            return render_template("edit.html", information="Invalid Price")
        else:
            price = float(price)

        # Insert into the history the old values
        old = db.execute("SELECT * FROM holdings WHERE id = ?", symbolID)

        symbol = old[0]["symbol"]
        oldHoldings = old[0]["holdings"]
        oldPrice = old[0]["price"]
        oldValue = "{:.2f}".format(oldPrice * oldHoldings)
        value = holdings * price

        db.execute("INSERT INTO history (user_id, symbol, oldHoldings, oldPrice, oldValue, newHoldings, newPrice, newValue, type) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   userID, symbol, oldHoldings, oldPrice, oldValue, holdings, price, value, "EDIT")

        # Update the holdings database with the edited values
        db.execute("UPDATE holdings SET holdings = ?, price = ? WHERE user_id = ? AND id = ?", holdings, price, userID, symbolID)

        return redirect("/dashboard")

    # GET method
    else:
        return render_template("edit.html", portfolio=portfolio)


@app.route("/history")
@login_required
def history():
    # Get all the data from the history database related to the user
    userID = session["user_id"]

    history = []
    row = {}

    histories = db.execute("SELECT * FROM history WHERE user_id = ? ORDER BY ts DESC", userID)

    # Append it to a new list to obtain the name of the cryptocurrency and not just the symbol. Also need to update the timestamp with the relevant date and time.
    for i in range(len(histories)):
        row.clear()

        row["rank"] = i + 1
        row["timestamp"] = histories[i]["ts"]
        row["symbol"] = histories[i]["symbol"]
        row["name"] = fetchName(histories[i]["symbol"])
        row["oldHoldings"] = histories[i]["oldHoldings"]
        row["oldPrice"] = histories[i]["oldPrice"]
        row["oldValue"] = histories[i]["oldValue"]
        row["newHoldings"] = histories[i]["newHoldings"]
        row["newPrice"] = histories[i]["newPrice"]
        row["newValue"] = histories[i]["newValue"]
        row["type"] = histories[i]["type"]

        history.append(row.copy())
    return render_template("history.html", history=history)


@app.route("/currency")
def currency():
    data = (requests.get("https://api.exchangerate-api.com/v4/latest/USD")).json()

    currencies = data["rates"]

    return render_template("currency.html", currencies=currencies)


@app.route("/username", methods=["GET", "POST"])
@login_required
def username():
    if request.method == "POST":
        userID = session["user_id"]
        username = request.form.get("username")
        year = request.form.get("year")
        USERNAMES = db.execute("SELECT username FROM users")

        # If username is blank
        if not username:
            return render_template("username.html", information="Invalid Username")
        # Check the year against the one inputted by the user
        profile = db.execute("SELECT * FROM users WHERE id = ?", userID)
        if username == profile[0]["username"]:
            return render_template("username.html", information="Cannot choose same username")

        # If username already in database
        for entry in USERNAMES:
            if username == entry["username"]:
                return render_template("username.html", information="Username already taken")
        # If year is blank
        if not year:
            return render_template("username.html", information="Invalid Date of Birth")
        if year != profile[0]["year"]:
            return render_template("username.html", information="Incorrect Date of Birth")

        # If all correct, update the user database
        db.execute("UPDATE users SET username = ? WHERE id = ?", username, userID)
        return redirect("/dashboard")

    else:
        return render_template("username.html")


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    if request.method == "POST":
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        year = request.form.get("year")
        userID = session["user_id"]

        profile = db.execute("SELECT * FROM users WHERE id = ?", userID)

        # If password is blank
        if not password:
            return render_template("password.html", information="Invalid password")
        # If passwords do not match
        if password != confirmation:
            return render_template("password.html", information="Passwords do not match")
        if not year:
            return render_template("password.html", information="Invalid Date of Birth")
        # Check whether its the same password
        if check_password_hash(profile[0]["hash"], password):
            return render_template("password.html", information="Cannot use same password")
        if year != profile[0]["year"]:
            return render_template("password.html", information="Incorrect Date of Birth")

        # Update the database with the new data
        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(password), userID)
        return redirect("/dashboard")
    else:
        return render_template("password.html")


@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        username = request.form.get("username")
        year = request.form.get("year")
        session["username"] = username

        if not username:
            return render_template("forgot.html", information="Invalid Username")

        exist = db.execute("SELECT COUNT(id) FROM users WHERE username = ?", username)
        if exist[0]["COUNT(id)"] == 0:
            return render_template("forgot.html", information="Account not Found")

        profile = db.execute("SELECT * FROM users WHERE username = ?", username)

        if not year:
            return render_template("forgot.html", information="Invalid Date of Birth")
        if year != profile[0]["year"]:
            return render_template("forgot.html", information="Incorrect Date of Birth")

        return render_template("change.html", username=session["username"])

    else:
        return render_template("forgot.html")


@app.route("/change", methods=["POST"])
def change():
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    # If password is blank
    if not password:
        return render_template("change.html", information="Invalid password", username=session["username"])
    # If passwords do not match
    if password != confirmation:
        return render_template("change.html", information="Passwords do not match", username=session["username"])

    db.execute("UPDATE users SET hash = ? WHERE username = ?", generate_password_hash(password), session["username"])
    session.clear()
    return redirect("/login")