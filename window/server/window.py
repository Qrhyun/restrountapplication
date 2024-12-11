
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

