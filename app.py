from flask import Flask, request, redirect, render_template_string, send_file
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

ADMIN_PASSWORD = "6770"

products = []
cart = []

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Shop</title>
</head>
<body style="background:#111;color:white;text-align:center;font-family:tahoma;">
<h1>🛒 فروشگاه</h1>

{% for p in products %}
<div style="border:1px solid gray;margin:10px;padding:10px;">
<h3>{{loop.index0}} - {{p['name']}}</h3>
<p>قیمت: {{p['price']}}</p>
<p>موجودی: {{p['stock']}}</p>
<a href="/add/{{loop.index0}}">افزودن به سبد</a>
</div>
{% endfor %}

<h2>🧺 سبد خرید</h2>
{% for c in cart %}
<p>{{c['name']}} - {{c['price']}}</p>
{% endfor %}

<a href="/checkout">خرید نهایی</a>

<hr>
<h3>🔒 مدیریت</h3>
<form method="post" action="/admin">
<input name="password" placeholder="رمز">
<input name="name" placeholder="نام محصول">
<input name="price" placeholder="قیمت">
<input name="stock" placeholder="تعداد">
<button type="submit">اضافه محصول</button>
</form>

<form method="post" action="/increase">
<input name="password" placeholder="رمز">
<input name="index" placeholder="شماره محصول">
<input name="amount" placeholder="مقدار افزایش">
<button type="submit">افزایش موجودی</button>
</form>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, products=products, cart=cart)

@app.route("/admin", methods=["POST"])
def admin():
    if request.form["password"] == ADMIN_PASSWORD:
        products.append({
            "name": request.form["name"],
            "price": request.form["price"],
            "stock": int(request.form["stock"])
        })
    return redirect("/")

@app.route("/increase", methods=["POST"])
def increase():
    if request.form["password"] == ADMIN_PASSWORD:
        i = int(request.form["index"])
        amount = int(request.form["amount"])
        if i < len(products):
            products[i]["stock"] += amount
    return redirect("/")

@app.route("/add/<int:i>")
def add(i):
    if products[i]["stock"] > 0:
        cart.append(products[i])
        products[i]["stock"] -= 1
    return redirect("/")

@app.route("/checkout")
def checkout():
    global cart
    if not cart:
        return redirect("/")

    total = sum(int(c["price"]) for c in cart)

    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    y = 20
    draw.text((20, y), "Receipt", fill="black")
    y += 30

    for c in cart:
        draw.text((20, y), f"{c['name']} - {c['price']}", fill="black")
        y += 25

    draw.text((20, y+20), f"Total: {total}", fill="black")

    img.save("receipt.png")

    cart = []
    return send_file("receipt.png", mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
