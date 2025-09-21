import requests
from bs4 import BeautifulSoup
import random
import re
from markupsafe import escape


from flask import Flask, render_template, redirect, url_for, request

user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36", 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0]"]

accept_lang = "en"

accept_enc = "gzip, deflate, br"

accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"

def amazon_scraper(query, n):
    url = "https://www.amazon.com/s?k=" + "+".join(query.lower().split()) + "&ref=nb_sb_noss"

    ua = random.choice(user_agents)

    amazon_referer_pages = ["https://www.amazon.com/ref=nav_logo",
                    "https://www.amazon.com/gp/cart/view.html?ref_=nav_cart",
                    "https://www.amazon.com/gp/history?ref_=nav_cs_timeline",
                    "https://www.amazon.com/gp/css/order-history?ref_=nav_orders_first",
                    "https://www.amazon.com/haul/store?ref_=nav_cs_hul_disb"]

    referer = random.choice(amazon_referer_pages)

    headers = {
        "User-Agent": ua,
        "Accept-Language": accept_lang,
        "Accept-Encoding": accept_enc,
        "Accept": accept,
        "Referer": referer
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.find_all('h2', class_='a-size-base-plus a-spacing-none a-color-base a-text-normal')
    print(len(items))
    images = soup.find_all('img', {"class":'s-image', "data-image-latency":'s-product-image'})
    prices = soup.find_all('span', class_='a-offscreen')
    ratings = soup.find_all('span', class_='a-size-small a-color-base')
    links = soup.find_all('a', class_="a-link-normal s-no-outline")
    
    prices = [i for i in prices if not re.search("[A-Za-z]", i.text)]
    returndict = {}
    for i in range(n):
        name = items[i]["aria-label"]
        if name[:15] == "Sponsored Ad - ":
            name = name[15:]
        returndict[i] = [name, images[i]["src"], prices[i].text, ratings[i].text, "https://www.amazon.com/" + links[i]["href"]]
    
    return returndict

app = Flask(__name__)

def card(name, img, price, rating):
    s = f"<div><img src=\"{img}\">{name}<br>{price}<br>{rating}</div>"
    return s

@app.route("/shop/<item>")
def main(item):
    d = amazon_scraper(item, 15)
    entries = list(d.values())
    return render_template("catalog.html", entries = entries)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/home")
def home2():
    return redirect(url_for("home"))

@app.route("/shop")
def shopping():
    return render_template("shop.html")

@app.route("/checklist")
def checklist():
    return render_template("checklist.html")

@app.route("/cart")
def shopping_cart():
    return render_template("cart.html")


@app.route("/checklist", methods=["GET", "POST"])
def default_checklist():
    if request.method == "POST":
        username = request.form.get('username', '').strip()
        if not username:
            return render_template('home.html', error='Please enter a name')
        return redirect(url_for('checklist', username=escape(username)))
    default_user = "Guest"
    return redirect(url_for('checklist', username=default_user))

checked_store = {}

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


if __name__ == '__main__':  
   app.run(port="5090", debug=True)  