from flask import Flask, jsonify, make_response, redirect, render_template, request
import psycopg2
import requests
from utils.db import get_db

app = Flask(__name__)
def get_location_from_ipapi(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}?lang=ru")
        data = response.json()
        if data and data['status'] == 'success':
            city = data.get('city')
            country = data.get('country')
            return city, country
        else:
            print(f"Ошибка IP-API: {data.get('message', 'Неизвестная ошибка')}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Сетевая ошибка при запросе к IP-API: {e}")
        return None, None

@app.route('/',methods = ['GET'])
def get_page():
    if request.method == "GET":
        user_ip = request.remote_addr # Получить IP пользователя
        city, country = get_location_from_ipapi(user_ip)
        if city and country:
            detail = {"message":"home","city":city,"country":country}
            return render_template('home.html',context=detail)
        else:
            detail = {"message":"home","city":"не удалось определить","country":"не удалось определить"}
            return render_template('home.html',context=detail)

@app.route('/error',methods = ['GET'])
def error():
    detail = {"message":"error"}
    if request.method == "GET":
        return render_template("error.html",context=detail)

@app.route('/samsung/phone/',methods = ['GET'])
def get_samsung_phone():
    page = request.args.get('page') 
    print(page)
    detail = {"message":"samsung_phone","page":page}
    if request.method == "GET":
        return render_template("home.html",context=detail)

@app.route('/samsung/tablet',methods = ['GET'])
def get_samsung_tablet():
    detail = {"message":"samsung_tablet"}
    if request.method == "GET":
        return render_template("home.html",context=detail)

@app.route('/samsung/notebook',methods = ['GET'])
def get_samsung_notebook():
    detail = {"message":"samsung_notebook"}
    if request.method == "GET":
        return render_template("home.html",context=detail)

@app.route('/apple/phone',methods = ['GET'])
def get_apple_phone():
    detail = {"message":"apple_phone"}
    if request.method == "GET":
        return render_template("home.html",context=detail)

@app.route('/apple/tablet',methods = ['GET'])
def get_apple_tablet():
    detail = {"message":"apple_tablet"}
    if request.method == "GET":
        return render_template("home.html",context=detail)

@app.route('/apple/notebook',methods = ['GET'])
def get_apple_notebook():
    detail = {"message":"apple_notebook"}
    if request.method == "GET":
        return render_template("home.html",context=detail)

@app.route('/profile/<username>')
def get_profile(username):
    print(username,"name")
    if username == "none":
        message = "Такой учетной записи нету."
        data = {"username":"none","email":"none","message":message}
        return render_template("login.html",context = data)
    if request.method == 'GET':
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT name, email, role from users WHERE name = %s",(username,))
                db = cur.fetchone()
                if db is None:
                    message = "Такой учетной записи нету."
                    data = {"username":"none","email":"none","message":message}
                    return render_template("login.html",context = data)
                else:
                    usernameInDb = db[0]
                    email = db[1]
                    role = db[2]
                    message = "Welcome"
                    data = {"username":usernameInDb,"email":email,"message":message,"role":role}
                    return render_template("login.html",context = data)
@app.route('/profile/login', methods=['GET','POST'])
def log_in():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
        with get_db() as conn:
            with conn.cursor() as cur:
                if password:
                    cur.execute("SELECT email, password from users WHERE name = %s AND password = %s",(username, password,))
                    db = cur.fetchone()
                    if db is None:
                        message = "Имя пользователя или пароль не верно."
                        data = {"username":"none","email":"none","message":message}
                        return render_template("login.html",context = data)
                    else:
                        passwordOK = db[1]
                        email = db[0]
                        print(passwordOK)
                        if password == passwordOK:
                            message = "Вы вошли успешно"
                            print(message)
                            data = [username,email]
                            return redirect(f"/profile/{username}")
                        else:
                            message = "Пароли не совподают."
                            return render_template("login.html",context = data)
    elif request.method == 'GET':
        data = {}
        return render_template("login.html",context = data)
@app.route('/profile/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        repeat_password = request.form.get('repait_password')
        print(username, email, password)
        if password == repeat_password:
            message = "Регистрация прошла успешно!"
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT name from users WHERE password = %s",(password,))
                    usernameInDb = cur.fetchone()
                    if usernameInDb is None:
                        cur.execute("""
                        INSERT INTO users (name, email, password)
                        VALUES (%s, %s, %s)""",(username, email, password))
                        print(username)
                        detail = {'message': message, 'username': username, 'email': email}
                        return redirect(f"/profile/{username}")
                    else:
                        print(username)
                        detail = {'message': message, 'username': username, 'email': email}
                        return redirect(f"/profile/{username}")
        else:
            message = "Пароли не совпадают."
        detail = {'message': message, 'username': "none", 'email': email}
        return render_template("login.html", context=detail)
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405

@app.route("/basket/<username>")
def open_basket(username):
    basket_items = []
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM users WHERE name = %s", (username,))
                user_record = cur.fetchone()
                if user_record:
                    user_id = user_record[0]

                    cur.execute("""
                        SELECT
                            p.name AS product_name,
                            p.price,
                            b.added_date
                        FROM
                            product AS p
                        INNER JOIN
                            basket AS b ON p.id = b.product_id
                        WHERE
                            b.user_id = %s
                            AND b.active = true;
                    """, (user_id,)) 

                    raw_items = cur.fetchall()
                    for item in raw_items:
                        basket_items.append({
                            "product_name": item[0],
                            "price": item[1],
                            "added_date": item[2]
                        })
                        product_names = item[0]
                        price = item[1]
                        added_date = item[2]
                        print(product_names, price, added_date)
                else:
                    detail = {"message":f"Пользователь '{username}' не найден."}
                    return render_template("error.html", context=detail), 404

    except psycopg2.Error as e:
        print(f"Ошибка базы данных при открытии корзины: {e}")
        detail = {"message":"Ошибка при загрузке корзины. Пожалуйста, попробуйте позже."}
        return render_template("error.html",context=detail ), 500
    except Exception as e:
        print(f"Неожиданная ошибка при открытии корзины: {e}")
        detail = {"message":"Произошла непредвиденная ошибка."}
        return render_template("error.html", context=detail), 500

    context = {
        "message":"open_basket",
        "basket_items": basket_items,
        "total_items": len(basket_items) 
    }
    return render_template("login.html", context=context)
@app.route('/set_cookie/<key>/<value>')
def set_cookie_route(key, value):
    print(key, value)
    response = make_response(jsonify({'status': 'success', 'message': f'Куки "{key}" установлена'}))
    response.set_cookie(key, value, max_age=1500)
    return response
@app.route('/get_cookie/<key>')
def get_cookie_route(key):
    cookie_value = request.cookies.get(key)
    print(cookie_value)
    if cookie_value:
        return jsonify({'status': 'success', 'data': cookie_value})
    else:
        return jsonify({'status': 'error', 'message': f'Куки "{key}" не найдена'}), 404

@app.route('/admin',methods = ['GET'])
def get_admin_page():
    if request.method == "GET":
        response = request.cookies.get('username')
        if response:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT role from users WHERE name = %s",(response,))
                    db = cur.fetchone()
                    if db == ('user',):
                        detail = {"message":"user","username": response}
                        print(db)
                        return render_template('home.html',context=detail)
                    if db == ('admin',):
                        detail = {"message":"admin","username": response}
                        print(db)
                        return render_template('admin.html',context=detail)
        else:
            detail= {"message":"user"}
            return render_template('home.html',context=detail)

@app.route('/samsung/phone/add_new', methods = ['GET', 'POST'])
def new_samsung_phone():
    if request.method == "GET":
        detail = {"message":"add_samsung_phone"}
        return render_template('admin.html',context=detail)
    if request.method == "POST":
        name = request.form.get('name')
        price = request.form.get('price')
        procesor = request.form.get('procesor')
        description = request.form.get('description')
        batarey = request.form.get('batarey')
        ram = request.form.get('ram')
        rom = request.form.get('rom')
        camera = request.form.get('camera')
        display = request.form.get('display')
        count = request.form.get('count')
        print(name, price, description,procesor, batarey, ram, rom, camera, display)
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT name, price, description, procesor, batarey, ram, rom, display, camera FROM samsung_mobile
                            WHERE name = %s AND description = %s AND procesor = %s AND batarey = %s AND ram = %s AND rom = %s AND display = %s AND camera = %s;
                            """,(name, description, procesor, batarey, ram, rom, display, camera))
                db = cur.fetchone()
                if db is None:
                    cur.execute("INSERT INTO samsung_mobile ( name, price, description, procesor, batarey, ram, rom, display, camera, storage)  VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                ( name, price, description, procesor, batarey, ram, rom, display, camera, count))
                    print("added")        
                    detail = {"message":"mobile_added",
                            "name": name,
                            "price": price,
                            "procesor":procesor,
                            "description":description,
                            "batarey":batarey,
                            "ram":ram,
                            "rom":rom,
                            "camera":camera,
                            "display":display,
                            "count":count}
                    return render_template('admin.html',context=detail)
                else:
                    detail = {"message":"mobile_in_db",}
                    return render_template('admin.html',context=detail)

@app.route('/samsung/tablet/add_new', methods = ['GET', 'POST'])
def new_samsung_tablet():
    detail = {"message":"add_samsung_tablet"}
    if request.method == "GET":
        return render_template('admin.html',context=detail)
    #и тут не забудь написать логику для Пост запроса

@app.route('/samsung/notebook/add_new', methods = ['GET', 'POST'])
def new_samsung_notebook():
    detail = {"message":"add_samsung_notebook"}
    if request.method == "GET":
        return render_template('admin.html',context=detail)
    #и тут не забудь написать логику для Пост запроса

@app.route('/about_us', methods = ['GET'])
def get_info():
    detail = {"message":"about_us"}
    if request.method == "GET":
        return render_template('aboutus.html',context=detail)

@app.route('/like/phone/<int:phone_id>', methods=['POST'])
def like_phone(phone_id):
    liked_status_str = request.args.get('liked') 
    if liked_status_str is None:
        return jsonify({"status": "error", "message": "Missing 'liked' query parameter."}), 400
    liked_status = liked_status_str.lower() == 'true'
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT "like" FROM samsung_mobile WHERE id = %s;""",(phone_id,))
            likes = cur.fetchone()
            like = likes[0]

    if liked_status == True:
        like+=1
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""UPDATE samsung_mobile SET "like"=%s WHERE id = %s""",(like, phone_id))
                success = True
    if liked_status == False:
        like -=1
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""UPDATE samsung_mobile SET "like"=%s WHERE id = %s""",(like, phone_id))
                success = True
    if success:
        action = "liked" if liked_status else "unliked"
        return jsonify({"status": "success", "message": f"Phone {phone_id} {action} successfully."}), 200
    else:
        return jsonify({"status": "error", "message": f"Failed to update like status for phone {phone_id}."}), 500

@app.route("/add_to_basket/<username_from_url>", methods=["POST"]) 
def add_to_basket(username_from_url):
    product_id = request.args.get("id")
    if not product_id:
        return jsonify({"status": "error", "message": "Product ID is missing"}), 400
    user_id = None
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM users WHERE name = %s", (username_from_url,)) 
                user_record = cur.fetchone()

                if user_record:
                    user_id = user_record[0]
                else:
                    return jsonify({"status": "error", "message": "User not found"}), 404
    except Exception as e:
        print(f"Ошибка при поиске пользователя: {e}")
        return jsonify({"status": "error", "message": "Database error while finding user"}), 500
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO basket(user_id, product_id) VALUES (%s, %s)",
                    (user_id, product_id)
                )
                return jsonify({"status": "success", "message": "Product added to basket"}), 200
    except psycopg2.IntegrityError as e:
        print(f"Ошибка целостности базы данных: {e}")
        return jsonify({"status": "error", "message": "Invalid product ID or user ID (Integrity error)"}), 400
    except Exception as e:
        print(f"Общая ошибка при добавлении в корзину: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=7010,host="0.0.0.0")


#opencard