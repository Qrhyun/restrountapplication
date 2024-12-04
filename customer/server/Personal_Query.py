#Personal_Query的后端代码
# 用于查询用户最近一次的消费记录和用户的剩余金额
from flask import Flask, request, jsonify
from db_config import get_db_connection
from flask_cors import CORS
from flask import Blueprint

personal_query_app = Blueprint('personal_query', __name__)
CORS(personal_query_app)



@personal_query_app.route('/recent_meal', methods=['GET'])
def recent_meal():
    user_id = request.args.get('user_id', type=int)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc('QueryRecentMeal', [user_id])
    results = []
    for result in cursor.stored_results():
        results.extend(result.fetchall())
    cursor.close()
    conn.close()
    return jsonify(results)


@personal_query_app.route('/remaining_money', methods=['GET'])
def remaining_money():
    user_id = request.args.get('user_id', type=int)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc('GetRemainingMoney', [user_id])
    result = []
    for res in cursor.stored_results():
        result.extend(res.fetchall())
    cursor.close()
    conn.close()
    return jsonify(result)


@personal_query_app.route('/total_spent', methods=['GET'])
def total_spent():
    user_id = request.args.get('user_id', type=int)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 执行查询
    cursor.execute('SELECT GetTotalSpent(%s) AS total_spent', (user_id,))

    # 获取单行结果
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    # 确保返回的格式是一个包含字典的数组
    if result:
        return jsonify([result])  # 包装成数组
    else:
        return jsonify([])  # 如果没有结果，返回一个空数组



@personal_query_app.route('/dine_in', methods=['GET'])
def dine_in():
    input_Bid = request.args.get('Bid', type=int)
    input_Vid = request.args.get('Vid', type=int)
    input_Bnum = request.args.get('Bnum', type=int)

    if not input_Bid or not input_Vid or not input_Bnum:
        return jsonify({'error': 'Bid, Vid, and Bnum are required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('DineInProcess', [input_Bid, input_Vid, input_Bnum])
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Dine-in process completed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@personal_query_app.route('/top3_spenders', methods=['GET'])
def top3_spenders():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('GetTop3SpendersInLast30Days')
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
        cursor.close()
        conn.close()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

