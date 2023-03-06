import pymysql
from app import app
from config import mysql
from flask import jsonify, session
from flask import flash, request
from werkzeug.security import check_password_hash

@app.route('/signup', methods=['POST'])
def create_user():
    try:
        _json = request.json
        _EmailId = _json['EmailId']
        _PetrolPumpName = _json['PetrolPumpName']
        _Branch = _json['Branch']
        _Password = _json['Password']
        if _EmailId and _PetrolPumpName and _Branch and _Password and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO signup(EmailId, PetrolPumpName, Branch, Password) VALUES(%s, %s, %s, %s)"
            bindData = (_EmailId, _PetrolPumpName, _Branch, _Password)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Employee added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/login', methods=['POST'])
def login():
    conn = None
    cursor = None

    try:
        _json = request.json
        _EmailId = _json['EmailId']
        _Password = _json['Password']

        # validate the received values
        if _EmailId and _Password:
            # check user exists
            conn = mysql.connect()
            cursor = conn.cursor()

            sql = "SELECT * FROM signup WHERE EmailId=%s and Password=%s"
            sql_where = (_EmailId, _Password)

            cursor.execute(sql, sql_where)
            row = cursor.fetchone()
            # print(conn)

            if row:
                return jsonify({'message': 'You are logged in Successfully'})
            if not row:
                return jsonify({'message': 'Bad Request - Invalid Email / Invalid Password'})
                
                
            # if row:
            #     if check_password_hash(row[2], _Password):
            #         session['EmailId'] = row[1]
            #         return jsonify({'message': 'You are logged in successfully'})
            #     else:
            #         resp = jsonify(
            #             {'message': 'Bad Request - invalid password'})
            #         resp.status_code = 400
            #         return resp

        else:
            resp = jsonify({'messages': 'Bad Request - invalid credendtials'})
            resp.status_code = 400
            return resp

    except Exception as e:
        print(e)

    finally:
        if cursor and conn:
            cursor.close()
            conn.close()


@app.route('/emp')
def emp():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT EmailId,PetrolPumpName,Branch,Password FROM signup")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# @app.route('/emp/<string:EmailId>')
# def emp_details(emp_id):
#     try:
#         conn = mysql.connect()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         cursor.execute("SELECT EmailId, PetrolPumpName, Branch, Password FROM signup WHERE EmailId =%s", emp_id)
#         empRow = cursor.fetchone()
#         respone = jsonify(empRow)
#         respone.status_code = 200
#         return respone
#     except Exception as e:
#         print(e)
#     finally:
#         cursor.close()
#         conn.close()

# @app.route('/update', methods=['PUT'])
# def update_emp():
#     try:
#         _json = request.json
#         _EmailId = _json['EmailId']
#         _PetrolPumpName = _json['PetrolPumpName']
#         _Branch = _json['Branch']
#         _Password = _json['Password']
#         if _EmailId and _PetrolPumpName and _Branch and _Password and request.method == 'PUT':
#             sqlQuery = "UPDATE signup SET EmailId=%s, PetrolPumpName=%s, Branch=%s, Password=%s WHERE EmailId=%s"
#             bindData = (_EmailId, _PetrolPumpName, _Branch, _Password, _EmailId,)
#             conn = mysql.connect()
#             cursor = conn.cursor()
#             cursor.execute(sqlQuery, bindData)
#             conn.commit()
#             respone = jsonify('Employee updated successfully!')
#             respone.status_code = 200
#             return respone
#         else:
#             return showMessage()
#     except Exception as e:
#         print(e)
#     finally:
#         cursor.close()
#         conn.close()

# @app.route('/delete/<string:EmailId>', methods=['DELETE'])
# def delete_emp(id):
# 	try:
# 		conn = mysql.connect()
# 		cursor = conn.cursor()
# 		cursor.execute("DELETE FROM signup WHERE EmailId =%s",)
# 		conn.commit()
# 		respone = jsonify('Employee deleted successfully!')
# 		respone.status_code = 200
# 		return respone
# 	except Exception as e:
# 		print(e)
# 	finally:
# 		cursor.close()
# 		conn.close()

@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


if __name__ == "__main__":
    app.run()
