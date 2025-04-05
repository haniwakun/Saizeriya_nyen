from flask import Flask, render_template, request, jsonify
import json
import random

app = Flask(__name__)

# メニューの読み込み
def load_menu():
    with open("menu.json", "r", encoding="utf-8") as f:
        return json.load(f)

# 合計1000円になる注文をランダムに作成
def generate_order(menu, target=1000, exclude_alcohol=False):
    # targetがNoneや法外な値の場合
    if target is None:
        target = 1000
    target = min(target, 99999)

    # アルコールを除外
    if exclude_alcohol:
        menu = [item for item in menu if not item.get("contains_alcohol", False)]


    min_price = min(int(item['price']) for item in menu)
    extended_menu = menu * (target // min_price + 1)
    random.shuffle(extended_menu)

    order = []
    total = 0
    
    for item in extended_menu:
        if total + int(item["price"]) <= target:
            order.append(item)
            total += int(item["price"])
        if total == target:
            break
    
    return order, total

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
