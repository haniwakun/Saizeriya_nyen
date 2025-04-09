import random
import json

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

    # 最低金額のアイテムのみで予算に到達しても良いようにmenuをかさ増し
    min_price = min(int(item['price']) for item in menu)
    extended_menu = menu * (target // min_price + 1)
    random.shuffle(extended_menu)

    order = []
    total = 0
    
    # かさ増ししてシャッフルしたメニュー内のアイテムを順に確認し、片っ端から注文する
    for item in extended_menu:
        if total + int(item["price"]) <= target:
            order.append(item)
            total += int(item["price"])
    
    return order, total

