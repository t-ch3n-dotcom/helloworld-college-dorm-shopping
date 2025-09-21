from flask import Flask, render_template

app = Flask(__name__)

# Example cart items with images and quantity
cart_items = [
    {"name": "Mini Fridge", "price": 120, "quantity": 1, "image": "https://simzlife.com/cdn/shop/files/3_ee23f253-cd74-4bb9-aa2f-e5ad0a70cd29.jpg?v=1706243940"},
    {"name": "Desk Lamp", "price": 25, "quantity": 2, "image": "https://mobileimages.lowes.com/productimages/b8e6068d-58a3-4076-9328-c57f25de82e5/67572327.jpeg?size=pdhz"},
    {"name": "Laundry Basket", "price": 15, "quantity": 1, "image": "https://www.sterilite.com/image/600/12167906-BEAUTY-1.jpg"}
]

@app.route("/cart")
def cart():
    total = sum(item["price"] * item["quantity"] for item in cart_items)
    return render_template("cart.html", items=cart_items, total=total)

if __name__ == "__main__":
    app.run(debug=True)
