from flask import Flask, render_template, redirect, url_for, request
from markupsafe import escape

# Simple in-memory store: { username: set(of item ids) }
checked_store = {}

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/checklist", methods=["GET", "POST"])
def default_checklist():
    if request.method == "POST":
        username = request.form.get('username', '').strip()
        if not username:
            return render_template('home.html', error='Please enter a name')
        return redirect(url_for('checklist', username=escape(username)))
    default_user = "Guest"
    return redirect(url_for('checklist', username=default_user))


@app.route("/<username>", methods=["GET", "POST"])
def checklist(username):
    # Static sections (same as before)
    sections = [
        {'title': 'Bathroom & Toiletries', 'items': ['Shower Slippers', 'Towels', 'Caddie', 'Wet Wipes']},
        {'title': 'Bedding & Organization', 'items': ['Sheets', 'Comforter', 'Pillows', 'Pillow Covers']},
        {'title': 'Dorm Cutlery', 'items': ['Plastic Cups', 'Forks', 'Knives', 'Spoons', 'Bowls', 'Plates', 'Paper Towels']},
        {'title': 'Extras', 'items': ['Organizers', 'Hangers', 'Iron']}
    ]

    user = escape(username)

    # Handle form submission on user's checklist page to update checked items
    if request.method == 'POST':
        # form sends checkbox values as 'item-<section>-<index>' = 'on' when checked
        checked = set(request.form.getlist('checked'))
        checked_store[user] = checked
        return redirect(url_for('checklist', username=username))

    user_checked = checked_store.get(user, set())
    return render_template('checklist.html', name=username, sections=sections, checked=user_checked)


if __name__ == "__main__":
    app.run(debug=True)