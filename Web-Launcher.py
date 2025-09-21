from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/home")
def home2():
    return redirect(url_for("home"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/shop")
def shopping():
    return render_template("shop.html")

@app.route("/checklist")
def checklist():
    return render_template("checklist.html")

@app.route("/cart")
def shopping_cart():
    return render_template("cart.html")

if __name__ == "__main__":
    app.run()
