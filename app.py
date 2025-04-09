from flask import Flask, render_template, request, jsonify
from utils import load_menu, generate_order

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/order", methods=["GET"])
def order():
    menu = load_menu()
    exclude_alcohol = request.args.get("exclude_alcohol") == "true"
    try:
        target_price = int(request.args.get("target_price", "").strip())
    except(ValueError, AttributeError):
        target_price = None

    order_result, total_result = generate_order(
        menu, 
        target=target_price, 
        exclude_alcohol=exclude_alcohol
    )
    
    return render_template(
        "order.html", 
        order=order_result, 
        total=total_result, 
        exclude_alcohol=exclude_alcohol, 
        target_price=target_price
    )

if __name__ == "__main__":
    app.run(debug=True)
