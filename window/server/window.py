
from flask import Flask, request, jsonify
from db_config import get_db_connection
from flask_cors import CORS
from flask import Blueprint

window_app = Blueprint('window', __name__)
CORS(window_app)



@window_app.route('/view_data', methods=['GET'])
def view_data():
    view_name = request.args.get('view_name')
    if not view_name:
        return jsonify({'error': 'view_name is required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('GetViewData', [view_name])
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
        cursor.close()
        conn.close()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@window_app.route('/totalwin_vegpurchases', methods=['GET'])
def totalwin_vegpurchases():
    dish_id = request.args.get('dish_id', type=int)
    if not dish_id:
        return jsonify({'error': 'dish_id is required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('QueryVegPurchases', [dish_id])
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
        cursor.close()
        conn.close()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@window_app.route('/gettop5windows', methods=['GET'])
def gettop5windows():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc('GetTop5Windows')
    results = []
    for result in cursor.stored_results():
        results.extend(result.fetchall())
    cursor.close()
    conn.close()
    return jsonify(results)



@window_app.route('/gettop5veg', methods=['GET'])
def gettop5veg():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc('GetTop5VegByRemark')
    results = []
    for result in cursor.stored_results():
        results.extend(result.fetchall())
    cursor.close()
    conn.close()
    return jsonify(results)


# 模拟三个食堂的座位数据
canteens = {
    1: [
        {"seat_id": row * 10 + col + 1, "status": "available"}
        for row in range(10)  # 10 排
        for col in range(10)  # 每排 10 个座位
    ],
    2: [
        {"seat_id": row * 10 + col + 1, "status": "available"}
        for row in range(8)  # 8 排
        for col in range(12)  # 每排 12 个座位
    ],
    3: [
        {"seat_id": row * 10 + col + 1, "status": "available"}
        for row in range(6)  # 6 排
        for col in range(15)  # 每排 15 个座位
    ],
}

# 示例：将部分座位设置为已预定
for reserved_seat_id in [5, 15, 25, 35, 45]:
    for canteen_id, seats in canteens.items():
        for seat in seats:
            if seat["seat_id"] == reserved_seat_id:
                seat["status"] = "reserved"

@window_app.route('/seats', methods=['GET'])
def get_seats():
    """
    获取指定食堂的所有座位状态
    """
    canteen_id = request.args.get('canteen_id', type=int)
    if not canteen_id or canteen_id not in canteens:
        return jsonify({"error": "Invalid or missing canteen_id"}), 400

    return jsonify(canteens[canteen_id]), 200

@window_app.route('/reserve_seat', methods=['POST'])
def reserve_seat():
    """
    预定指定食堂的座位
    """
    data = request.json
    canteen_id = data.get('canteen_id')
    seat_id = data.get('seat_id')

    if not canteen_id or canteen_id not in canteens:
        return jsonify({"error": "Invalid or missing canteen_id"}), 400
    if not seat_id:
        return jsonify({"error": "seat_id is required"}), 400

    # 查找座位
    seats = canteens[canteen_id]
    seat = next((s for s in seats if s["seat_id"] == seat_id), None)
    if not seat:
        return jsonify({"error": "Seat not found"}), 404

    # 检查座位状态
    if seat["status"] == "reserved":
        return jsonify({"error": "Seat is already reserved"}), 400

    # 更新座位状态
    seat["status"] = "reserved"
    return jsonify({"message": f"Seat {seat_id} in canteen {canteen_id} reserved successfully"}), 200