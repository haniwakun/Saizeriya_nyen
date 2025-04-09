from flask import Flask, render_template, request, jsonify
import json
from utils import generate_order

app = Flask(__name__)

# メニューの読み込み
def load_menu():
    with open("menu.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/order", methods=["GET"])
def order():
    menu = load_menu()
    exclude_alcohol = request.args.get("exclude_alcohol") == "true"
    target_price = request.args.get("target_price")
    if target_price:
        try:
            target_price = int(target_price)
        except ValueError:
            target_price = None

    
    order_result, total_result = generate_order(menu, target=target_price, exclude_alcohol=exclude_alcohol)
    return render_template("order.html", order=order_result, total=total_result, 
                           exclude_alcohol=exclude_alcohol, target_price=target_price)

if __name__ == "__main__":
    app.run(debug=True)
