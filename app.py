from flask import Flask, jsonify, make_response, redirect, render_template, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from utils.models import init_models
import os
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

db = SQLAlchemy()

app = Flask(__name__)


UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploads'))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    try:
        os.makedirs(UPLOAD_FOLDER)
        print(f"Папка '{UPLOAD_FOLDER}' успешно создана.")
    except OSError as e:
        print(f"Ошибка при создании папки '{UPLOAD_FOLDER}': {e}")

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db.init_app(app)

User, Product, Category, Basket, Order, Message, News = init_models(db_instance=db)











@app.route('/',methods = ['GET'])
def get_page():
    if request.method == "GET":
        user_ip = request.remote_addr
        city, country = "city","country"
        if city and country:
            detail = {"message":"home","city":city,"country":country}
            return render_template('home.html',context=detail)
        else:
            detail = {"message":"home","city":"не удалось определить","country":"не удалось определить"}
            return render_template('home.html',context=detail)
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405












@app.route('/news',methods = ['GET'])
def get_news():
    bignews = News.query.filter_by(size = "big").all()
    midnews = News.query.filter_by(size = "medium").all()
    smallnews = News.query.filter_by(size = "small").all()

    detail = {
        "message": "open_news",
        "bignews":bignews,
        "midnews":midnews,  
        "smallnews":smallnews  
    }
    return render_template("news.html",context=detail)














@app.route('/error',methods = ['GET'])
def error():
    detail = {"message":"error","error":"ОШИБКА: Вы вошли не на тот роут."}
    if request.method == "GET":
        return render_template("error.html",context=detail)
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405











@app.route('/samsung/phone', methods=['GET'])
def get_samsung_phone():
    products = Product.query.filter_by().all()

    context = {
        "message": "samsung_phone",
        "products": products          
    }
    
    return render_template("home.html", context=context)













@app.route('/samsung/tablet',methods = ['GET'])
def get_samsung_tablet():
    detail = {"message":"samsung_tablet"}
    if request.method == "GET":
        return render_template("home.html",context=detail)
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405












@app.route('/samsung/notebook',methods = ['GET'])
def get_samsung_notebook():
    detail = {"message":"samsung_notebook"}
    if request.method == "GET":
        return render_template("home.html",context=detail)
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405










@app.route('/apple/phone',methods = ['GET'])
def get_apple_phone():
    detail = {"message":"apple_phone"}
    if request.method == "GET":
        return render_template("home.html",context=detail)
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405












@app.route('/apple/tablet',methods = ['GET'])
def get_apple_tablet():
    detail = {"message":"apple_tablet"}
    if request.method == "GET":
        return render_template("home.html",context=detail)
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405













@app.route('/apple/notebook',methods = ['GET'])
def get_apple_notebook():
    detail = {"message":"apple_notebook"}
    if request.method == "GET":
        return render_template("home.html",context=detail)
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405















@app.route('/profile/<username>', methods = ['GET'])
def get_profile(username):
    print(username,"name")
    if request.method == "GET":
        if username == "none":
            data = {"username":"none","email":"none","message":"error","error":"Такой учетной записи нету."}
            return render_template("login.html",context = data)

        user = User.query.filter_by(username=username).first()
        if not user:
            data = {"username":"none","email":"none","message":"error","error":"Такой учетной записи нету."}
            return render_template("login.html",context = data)

        username, email, role = user.username, user.email, user.role
        return render_template("login.html",context = {"username":username,"email":email,"message":"Welcome","role":role})
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405















@app.route('/profile/login', methods=['GET','POST'])
def log_in():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
        user = User.query.filter_by(username=username,password=password).first()
        if not user:
            data = {"username":"none","email":"none","message":"error","errorlog":"Имя пользователя или пароль не верно."}
            return render_template("login.html",context = data)
        if user.password == password:
            print("Пароль верный")
            response = make_response(redirect(f"/profile/{username}"))
            response.set_cookie('username', username, max_age=1500)
            return response
        else:
            return render_template("login.html",context = {"message":"errorlog","error":"Пароли не совподают."})

    elif request.method == 'GET':
        response = request.cookies.get('username')
        if response:
            return redirect(f"/profile/{response}")
        data = {}
        return render_template("login.html",context = data)
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405















@app.route('/profile/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        repeat_password = request.form.get('repait_password')
        print(username, email, password)
        if password == repeat_password:
            user = User.query.filter_by(username=username,password=password).first()
            if user:
                detail = {'username': username, 'email': email,"message":"error","errorreg":"Пользователь с таким именем уже существует."}
                return render_template("login.html", context=detail)
            new_user = User(
                username = username,
                email = email,
                password = password)
            db.session.add(new_user)
            db.session.commit()
            detail = {'message':"Регистрация прошла успешно.", 'username': username, 'email': email}
            return redirect(f"/profile/{username}")
        else:
            detail = {"message":"error",'errorreg': "Пароли не совпадают.", 'username': "none", 'email': email}
            return render_template("login.html", context=detail)

    elif request.method == 'GET':
        response = request.cookies.get('username')
        if response:
            return redirect(f"/profile/{response}")
        data = {"message":"openreg"}
        return render_template("login.html",context = data)
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405















@app.route('/basket/order_ok', methods=['GET','POST'])
def submit_order():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        city = request.form.get('city')
        address = request.form.get('addres')
        number = request.form.get('number')
        mess = request.form.get('mess')
        total_price = request.form.get("total_price")
        product_name = request.form.get("product_name")
        print(name,email,city,address,number,mess,total_price,product_name)
        required_fields = [name,email,city,address,number,mess]
        if not all(required_fields):
            return jsonify({"error":"Не заполнены все данные"})
        new_order = Order(
            username = name,
            email = email,
            city = city,
            address = address,
            number = int(number),
            message = mess,
            product_name = product_name,
            total_price = int(total_price),
            status = "pending"
        )
        username = request.cookies.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            return render_template("error.html",context={"error":"User not found"})
        basket_records = Basket.query.filter_by(
                user_id=user.id,
                active=True
        ).all()
        if basket_records:
            for basket in basket_records:
                basket.active = False
        db.session.add(new_order)
        db.session.commit()
        data = {"message":"pending","status":"pending"}
        return render_template("login.html",context = data)
    elif request.method == 'GET':
        data = {"message":"pending","status":"shipped"}
        return render_template("login.html",context = data)












@app.route("/basket/<username>", methods = ['GET'])
def open_basket(username):
    basket_items_data = []
    if request.method == "GET":
        try:
            user = User.query.filter_by(username=username).first()
            if not user:
                return render_template("error.html",context={"error":"User not found"})
            basket_records = Basket.query.filter_by(
                user_id=user.id,
                active=True
            ).all()
            if not basket_records:
                return render_template("login.html",context={"message": "open_basket" ,"errorbas":"Ваша корзина пуста"})

            for item in basket_records:
                basket_items_data.append({
                    "product_name": item.product.name,
                    "price": item.product.price,
                    "added_date": item.added_date
                })

            context = {
                "username": username, 
                "basket_items": basket_items_data,
                "total_items": len(basket_items_data),
                "message": "open_basket" 
            }
            return render_template("login.html", context=context)

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Ошибка базы данных при открытии корзины для пользователя {username}: {e}")
            detail = {"error": "Ошибка при загрузке корзины. Пожалуйста, попробуйте позже."}
            return render_template("error.html", context=detail), 500
        except Exception as e:
            db.session.rollback()
            print(f"Неожиданная ошибка при открытии корзины для пользователя {username}: {e}")
            detail = {"error": "Произошла непредвиденная ошибка."}
            return render_template("error.html", context=detail), 500
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405















    
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
    orders_item_data = []
    messages_data = []
    if request.method == "GET":
        response = request.cookies.get('username')
        if response:
            user = User.query.filter_by(username=response).first()
            if user.username == 'admin':
                orders = Order.query.filter_by(status = "pending").all()
                if not orders:
                    error1 ="Заказов нету"
                for item in orders:
                    orders_item_data.append({
                        "order_id":item.id,
                        "name": item.username,
                        "email":item.email,
                        "city":item.city,
                        "address":item.address,
                        "number":item.number,
                        "mess":item.message,
                        "product_name":item.product_name,
                        "total_price": item.total_price,
                        "added_date": item.added_date
                    })
                messages = Message.query.filter_by(status = "non").all()
                # if not messages:
                    # error2 = "Писем нету"
                for userinfo in messages:
                    messages_data.append({
                        "id":userinfo.id,
                        "name": userinfo.name,
                        "email":userinfo.email,
                        "number":userinfo.number,
                        "textmessage":userinfo.message,
                        "added_date":userinfo.added_date
                    })
                print(messages_data)
                detail = {"message":"admin",
                        "username": response,
                        "orders":orders_item_data,
                        "messages":messages_data,
                        "error1":error1}
                print(user.username)
                return render_template('admin.html',context=detail)
            else:
                detail = {"message":"user","username": response}
                print(user.username)
                return render_template('home.html',context=detail)
        else:
            detail= {"message":"user"}
            return render_template('home.html',context=detail)
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405
















@app.route("/admin/order/shipped/",methods = ["GET"])
def order_approved():
    id = request.args.get("id")
    if request.method == "GET":
        response = request.cookies.get('username')
        if response:
            user = User.query.filter_by(username=response).first()
            if user.username == 'admin':
                orders = Order.query.filter_by(id = id,status = "pending").first()
                if not orders:
                    return render_template("error.html",context={"error":"Заказов нету"})
                orders.status = "shipped"

                db.session.commit()
                return jsonify({"message":"Ok"})
            else:
                detail= {"message":"user"}
                return render_template('home.html',context=detail)
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405

















@app.route("/admin/message/ok/",methods = ["GET"])
def message_ok():
    id = request.args.get("id")
    if request.method == "GET":
        response = request.cookies.get('username')
        if response:
            user = User.query.filter_by(username=response).first()
            if user.username == 'admin':
                messages = Message.query.filter_by(id = id,status = "non").first()
                if not messages:
                    return render_template("error.html",context={"error":"Писем нету"})
                messages.status = "ok"

                db.session.commit()
                return jsonify({"message":"Ok"})
            else:
                detail= {"message":"user"}
                return render_template('home.html',context=detail)
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405















@app.route("/admin/add_news/",methods = ['GET','POST'])
def add_news():
    size = request.args.get("size")
    if request.method == 'GET':
        detail = {"message":"add_big_news","size":size}
        return render_template("admin.html",context=detail)
    if request.method == "POST":
        img_url = None
        
        print(f"Request Files: {request.files}")
        print(f"Request Form: {request.form}")

        if 'img_url' not in request.files:
            return render_template('admin.html', context={"message":"error","error": "Файл изображения отсутствует в запросе."}), 400
        
        file = request.files['img_url']
        if file.filename == '':
            print("Поле img_url присутствует, но файл не выбран.")
            return render_template('admin.html', context={"message":"error","error": "Файл изображения обязателен для загрузки."}), 400
        
        if not allowed_file(file.filename):
            return render_template('admin.html', context={"message":"error","error": "Недопустимое расширение файла изображения. Разрешены: png, jpg, jpeg, gif."}), 400
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(filepath)
            img_url = url_for('uploaded_file', filename=filename, _external=True) 
            print(f"Изображение успешно сохранено: {filepath}, доступно по URL: {img_url}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
            return render_template('admin.html', context={"message":"error","error": f"Ошибка при сохранении файла: {e}"}), 500

        title = request.form.get("title")
        text = request.form.get("text")

        print(f"Собранные данные: Title='{title}', Size='{size}', Text='{text}', Img_URL='{img_url}'")

        if not title or not text:
            return render_template('admin.html', context={"message":"error","error": "Поля 'Название' и 'Текст' новости обязательны для заполнения."}), 400

        try:
            new_line = News(
                title=title,
                size=size,
                text=text,
                img_url=img_url
            )
            db.session.add(new_line)
            db.session.commit()
            print("Новость успешно добавлена в базу данных.")
            return redirect(url_for("get_admin_page"))
        except IntegrityError as e:
            db.session.rollback() 
            print(f"Ошибка базы данных (IntegrityError): {e}")
            return render_template('admin.html', context={"message":"error","error": "Ошибка базы данных: Возможно, новость с таким названием уже существует."}), 409
        except SQLAlchemyError as e:
            db.session.rollback() 
            print(f"Ошибка SQLAlchemy: {e}")
            return render_template('admin.html', context={"message":"error","error": "Ошибка базы данных. Пожалуйста, попробуйте позже."}), 500




















@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)














@app.route('/samsung/phone/add_new', methods=['GET', 'POST'])
def new_samsung_phone():
    if request.method == "GET":
        detail = {"message": "add_samsung_phone"}
        return render_template('admin.html', context=detail)

    if request.method == "POST":
        img_url = None 
        if 'img_url' in request.files: 
            file = request.files['img_url']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename) 
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath) 
                img_url = os.path.join('/uploads', filename)
            else:
                return render_template('admin.html', context={"message":"error","error": "Недопустимый файл изображения или расширение."}), 400
        else:
            return render_template('admin.html', context={"message":"error","error": "Файл изображения отсутствует."}), 400

        name = request.form.get('name')
        price_str = request.form.get('price') 
        processor = request.form.get('procesor') 
        description = request.form.get('description')
        battery_str = request.form.get('batarey') 
        ram_str = request.form.get('ram')
        rom_str = request.form.get('rom')
        camera = request.form.get('camera')
        display = request.form.get('display')
        count_str = request.form.get('count') 

        required_fields = [name, price_str, processor, description, battery_str, ram_str, rom_str, camera, display, count_str]
        if not all(required_fields):
            return render_template('admin.html', context={"message":"message","error": "Пожалуйста, заполните все поля."}), 400

        try:
            price = int(price_str)
            battery = int(battery_str)
            ram = int(ram_str)
            rom = int(rom_str)
            count = int(count_str) 
        except ValueError:
            return render_template('admin.html', context={"message":"error","error": "Ошибка: Цена, батарея, RAM, ROM или количество должны быть числами."}), 400

        try:
            existing_product = Product.query.filter_by(name=name).first()
            if existing_product:
                existing_product.storage += count
                db.session.commit()
                message = f"Количество товара '{name}' успешно обновлено. Новое количество: {existing_product.storage}"
            else:
                new_product = Product(
                    name=name,
                    price=price,
                    description=description,
                    img_url=img_url,
                    cpu=processor, 
                    battery=battery, 
                    ram=ram,
                    rom=rom,
                    display=display,
                    camera=camera,
                    storage=count,
                    category_id=1
                )
                db.session.add(new_product)
                db.session.commit()
                print(f"Новый продукт '{name}' успешно добавлен.")
            detail = {
                "message": "mobile_added",
                "name": name,
                "price": price,
                "processor": processor,
                "description": description,
                "battery": battery, 
                "ram": ram,
                "rom": rom,
                "camera": camera,
                "display": display,
                "count": count, 
                "img_url":img_url
            }
            return render_template('admin.html', context=detail)
        except IntegrityError as e:
            db.session.rollback()
            print(f"Ошибка целостности базы данных: {e}")
            return render_template('admin.html', context={"message":"error","error": "Ошибка базы данных: Продукт с таким именем уже существует (IntegrityError)."}), 409 # 409 Conflict

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Ошибка SQLAlchemy при добавлении/обновлении продукта: {e}")
            return render_template('admin.html', context={"message":"error","error": "Ошибка базы данных. Пожалуйста, попробуйте позже."}), 500

        except Exception as e:
            db.session.rollback()
            print(f"Непредвиденная ошибка при добавлении/обновлении продукта: {e}")
            return render_template('admin.html', context={"message":"error","error": "Произошла непредвиденная ошибка."}), 500

















@app.route('/samsung/tablet/add_new', methods = ['GET', 'POST'])
def new_samsung_tablet():
    detail = {"message":"add_samsung_tablet"}
    if request.method == "GET":
        return render_template('admin.html',context=detail)
    #и тут не забудь написать логику для Пост запроса
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405










@app.route('/samsung/notebook/add_new', methods = ['GET', 'POST'])
def new_samsung_notebook():
    detail = {"message":"add_samsung_notebook"}
    if request.method == "GET":
        return render_template('admin.html',context=detail)
    #и тут не забудь написать логику для Пост запроса
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405











@app.route('/about_us', methods = ['GET'])
def get_info():
    detail = {"message":"about_us"}
    if request.method == "GET":
        return render_template('aboutus.html',context=detail)
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405












@app.route("/about_us/message",methods = ['POST'])
def message_to_admin():
    name = request.form.get("name")
    email = request.form.get("email")
    number = request.form.get("number")
    textmessage = request.form.get("textmessage")
    required_fields = [name, email, number, textmessage]
    print(name,email,number,textmessage)
    if not all(required_fields):
        return render_template("error.html",context={"error":"Заполните все поля!"})
    new_message = Message(
        name = name,
        email = email,
        number = number,
        message = textmessage
    )
    db.session.add(new_message)
    db.session.commit()
    return redirect("/about_us")










@app.route('/order', methods = ['POST'])
def post_ordering():
    detail = {"message":"order"}
    return render_template('login.html',context=detail)













@app.route('/like/phone/<int:phone_id>', methods=['POST'])
def like_phone(phone_id):
    liked_status_str = request.args.get('liked')

    if liked_status_str is None:
        return jsonify({"status": "error", "message": "Параметр 'liked' отсутствует."}), 400

    liked_status = liked_status_str.lower() == 'true'

    try:
        product = Product.query.get(phone_id)

        if not product:
            return jsonify({"status": "error", "message": f"Телефон с ID {phone_id} не найден."}), 404

        if liked_status:
            product.liked_it += 1 
            action_message = "понравился"
        else:
            if product.liked_it > 0:
                product.liked_it -= 1
            action_message = "не понравился"

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": f"Телефон {phone_id} {action_message} успешно.",
            "current_likes": product.liked_it 
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Ошибка базы данных при обновлении лайков для телефона {phone_id}: {e}")
        return jsonify({"status": "error", "error": "Ошибка базы данных при обновлении лайков."}), 500
    except Exception as e:
        db.session.rollback()
        print(f"Непредвиденная ошибка при обновлении лайков для телефона {phone_id}: {e}")
        return jsonify({"status": "error", "error": "Произошла непредвиденная ошибка."}), 500



















@app.route("/add_to_basket/<username_from_url>", methods=["POST"])
def add_to_basket(username_from_url):
    if request.method == "POST":
        product_id_from_args = request.args.get("id")

        if not product_id_from_args:
            return jsonify({"status": "error", "message": "Product ID is missing"}), 400

        try:
            product_id = int(product_id_from_args)
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid Product ID format"}), 400

        try:
            user = User.query.filter_by(username=username_from_url).first()
            print(user.username)
            if not user:
                return jsonify({"status": "error", "message": "User not found"}), 404

            product = Product.query.get(product_id) 
            if not product:
                return jsonify({"status": "error", "message": "Product with this ID does not exist"}), 404

            existing_basket_item = Basket.query.filter_by(
                user_id=user.id,
                product_id=product_id
            ).first()

            if existing_basket_item:
                new_line_in_basket = Basket(user_id=user.id, product_id=product_id)
                product.storage -=1
                db.session.add(new_line_in_basket)
                db.session.commit()
                return jsonify({"status": "info", "message": "Product already in basket"}), 200

            new_line_in_basket = Basket(user_id=user.id, product_id=product_id)
            product.storage -=1
            db.session.add(new_line_in_basket)
            db.session.commit()

            return jsonify({"status": "success", "message": "Product added to basket"}), 200

        except IntegrityError as e:
            db.session.rollback()
            print(f"Ошибка целостности базы данных при добавлении в корзину: {e}")
            return jsonify({"status": "error", "message": "Database integrity error (e.g., user/product ID not found)"}), 400

        except Exception as e:
            db.session.rollback()
            print(f"Общая ошибка при добавлении в корзину: {e}")
            return jsonify({"status": "error", "message": "Internal server error"}), 500
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405
















@app.route("/basket/delete_product/", methods=['POST'])
def delete_product_from_basket():
    if request.method == "POST":
        product_name = request.args.get('product_name')
        user_name_from_query = request.args.get('username')

        if not product_name:
            return jsonify({"status": "error", "message": "Product name is missing"}), 400
        if not user_name_from_query:
            return jsonify({"status": "error", "message": "Username is missing"}), 400

        try:
            user = User.query.filter_by(username=user_name_from_query).first()
            if not user:
                return jsonify({"status": "error", "message": "User not found"}), 404

            product = Product.query.filter_by(name=product_name).first()
            if not product:
                return jsonify({"status": "error", "message": "Product not found"}), 404

            basket_item = Basket.query.filter_by(
                user_id=user.id,
                product_id=product.id
            ).first()

            if not basket_item:
                return jsonify({"status": "error", "message": "Product not found in user's basket"}), 404

            db.session.delete(basket_item)
            db.session.commit()

            return jsonify({"status": "success", "message": "Product successfully removed from basket"}), 200

        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при удалении из корзины: {e}")
            return jsonify({"status": "error", "message": "Internal server error"}), 500
    else:
        return jsonify({'error': 'Метод не разрешен'}), 405











if __name__ == '__main__':
    with app.app_context():
        db.drop_all() 
        db.create_all()
        print("Таблицы базы данных успешно созданы или уже существуют.")
        if User.query.filter_by(username='admin').first() is None:
            admin_user = User(
                username='admin',
                email='admin@example.com',
                password='admin', 
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Пользователь 'admin' добавлен.")
        if User.query.filter_by(username='David').first() is None:
            test_user = User(
                username='David',
                email='david@example.com',
                password='1234567890',
                role='user'
            )
            db.session.add(test_user)
            db.session.commit()
            print("Пользователь 'test_user' добавлен.")
            if Product.query.filter_by(name='Samsung Galaxy S25+').first() is None:
                test_product = Product(
                    name = "Samsung Galaxy S25+",
                    price = 544,
                    description = """В линейке S25 модель с приставкой «плюс» должна была стать основным предложением по соотношению цена/качество. Не такой компактный аппарат, как базовый S25, но и не такой большой, как S25 Ultra, этакая золотая середина. По стоимости модель
                    также выглядела интереснее, чем Ultra, выступала прямым конкурентом для iPhone 16 Pro. Надо учитывать, что модель мало чем отличается от прошлогоднего S24+, который все еще присутствует на рынке. Серые аппараты стоят около 45-50 тысяч
                    рублей, соотношение цена/качество запредельное, отличный выбор в любом аспекте. При этом никаких серьезных недостатков по сравнению с новинкой у этой модели нет, она выглядит отлично. Возникает сакраментальный вопрос: насколько выгодно
                    покупать новый аппарат? Ответ ровно такой же, как с любым новым поколением флагманов, они не так интересны по соотношению цена/качество, как устройства, уходящие с рынка. Получается странная ситуация: с одной стороны — реклама, продвижение
                    и фокус на новых моделях, но лучше продаются предыдущие аппараты (в федеральной рознице они также присутствуют). Понятно, что Galaxy S25+ станет востребован в больших объемах в следующем году, когда цены упадут, а новая модель не продемонстрирует
                    огромных отличий. Разница между аппаратами определенно присутствует, но она не настолько ошеломляющая, чтобы отличия в стоимости были так разительны. Так что покупка этого аппарата напрямую зависит от того, насколько вы экономите деньги.
                    Возможно, вам нужен подарок, тогда прошлогодняя модель не выглядит престижно для такого случая. С другой стороны, последние модели быстрее получают софт, который может вас порадовать (тот же OneUI 7 — очень классная штука, одна из
                    лучших систем на рынке). Давайте посмотрим на аппарат и оценим его.""",
                    cpu = "Snapdragon 8 Gen 8 ядер",
                    battery = 5000,
                    ram = 8,
                    rom = 256,
                    display = "Dynamic AMOLED – 1440 x 3120",
                    camera = "3 (100 MP + 16 MP + 16 MP)",
                    storage = 10,
                    category_id = 1,
                    img_url = "/static/images/phone/galaxy-s25 plus.jpg"
                )
            db.session.add(test_product)
            db.session.commit()
            print(f"Продукт {test_product} добавлен.")
            if Product.query.filter_by(name='Samsung Galaxy S25 Ultra').first() is None:
                test_product = Product(
                    name = "Samsung Galaxy S25 Ultra",
                    price = 670,
                    description = """В линейке S25 модель с приставкой «Ultra» традиционно становится флагманом, воплощающим все самые передовые технологии и инновации, доступные на момент выхода. S25 Ultra — это бескомпромиссный аппарат для тех, кто ищет максимум функциональности,
                    мощную камеру и огромный экран, а также ценит наличие стилуса S Pen. Он выступает прямым конкурентом для iPhone 16 Pro Max, а также другим топовым Android-флагманам. Надо учитывать, что модель мало чем отличается от прошлогоднего S24
                    Ultra, который все еще присутствует на рынке. Серые аппараты стоят около 70-80 тысяч рублей, соотношение цена/качество запредельное, отличный выбор в любом аспекте. При этом никаких серьезных недостатков по сравнению с новинкой у этой
                    модели нет, она выглядит отлично. Возникает сакраментальный вопрос: насколько выгодно покупать новый аппарат? Ответ ровно такой же, как с любым новым поколением флагманов, они не так интересны по соотношению цена/качество, как устройства,
                    уходящие с рынка. Получается странная ситуация: с одной стороны — реклама, продвижение и фокус на новых моделях, но лучше продаются предыдущие аппараты (в федеральной рознице они также присутствуют). Понятно, что Galaxy S25 Ultra станет
                    востребован в больших объемах в следующем году, когда цены упадут, а новая модель не продемонстрирует огромных отличий. Разница между аппаратами определенно присутствует, но она не настолько ошеломляющая, чтобы отличия в стоимости
                    были так разительны. Так что покупка этого аппарата напрямую зависит от того, насколько вы экономите деньги. Возможно, вам нужен подарок, тогда прошлогодняя модель не выглядит престижно для такого случая. С другой стороны, последние
                    модели быстрее получают софт, который может вас порадовать (тот же OneUI 7 — очень классная штука, одна из лучших систем на рынке, а новые функции Galaxy AI могут быть эксклюзивны или работать лучше на новом железе). Давайте посмотрим
                    на аппарат и оценим его.""",
                    cpu = "Qualcom Snapdragon 8 Elite 8 ядер",
                    battery = 5000,
                    ram = 10,
                    rom = 512,
                    display = "Dynamic AMOLED – 1440 x 3120",
                    camera = "4 (200 MP + 50 MP + 50 MP + 10 MP)",
                    storage = 10,
                    category_id = 1,
                    img_url = "/static/images/phone/galaxy-s25 ultra.avif"
                )
            db.session.add(test_product)
            db.session.commit()
            print(f"Продукт {test_product} добавлен.")
            if Product.query.filter_by(name='Samsung Galaxy S25').first() is None:
                test_product = Product(
                    name = "Samsung Galaxy S25",
                    price = 499,
                    description = """В линейке S25 модель стала базовым флагманским предложением, призванным обеспечить премиальный опыт в более компактном форм-факторе. Этот аппарат ориентирован на тех, кто ищет сбалансированное сочетание мощной производительности, качественных
                    камер и флагманских функций, но при этом ценит удобство использования одной рукой и не нуждается в гигантском экране или сверх-продвинутом зуме. Он выступает прямым конкурентом для iPhone 16 и других компактных флагманов от различных
                    производителей. Надо учитывать, что модель была официально представлена 22 января 2025 года и поступила в продажу 7 февраля 2025 года. Хотя это новинка, на рынке все еще активно присутствует ее предшественник – Galaxy S24. Серые аппараты
                    или устройства в отличном состоянии на вторичном рынке Galaxy S24 могут предлагаться по существенно более выгодным ценам (ориентировочно от 50-60 тысяч рублей), и они по-прежнему демонстрируют очень достойное соотношение цена/качество.
                    При этом, хоть S25 и предлагает ряд важных улучшений, серьезных недостатков у S24 нет, и он все еще выглядит отлично, особенно если вы ищете полноценный флагман по более доступной цене. Возникает сакраментальный вопрос: насколько выгодно
                    покупать новый аппарат? Ответ ровно такой же, как с любым новым поколением флагманов: они не так интересны по соотношению цена/качество, как устройства, уходящие с рынка. Получается странная ситуация: с одной стороны — реклама, продвижение
                    и фокус на новых моделях, но лучше продаются предыдущие аппараты (в федеральной рознице они также присутствуют). Понятно, что Galaxy S25 будет оставаться флагманом продаж в своем сегменте до выхода следующего поколения. Разница между
                    аппаратами определенно присутствует, но она не настолько ошеломляющая, чтобы отличия в стоимости были так разительны для всех. Так что покупка этого аппарата напрямую зависит от того, насколько вы экономите деньги и что для вас приоритетнее.
                    Возможно, вам нужен самый свежий смартфон с новейшей версией Android "из коробки" (Android 15 с One UI 7) и максимально длительной поддержкой обновлений (Samsung обещает до 7 лет основных обновлений Android и 7 лет патчей безопасности),
                    а также полноценной интеграцией всех функций Galaxy AI. С другой стороны, если вам нужен функциональный, мощный и уникальный аппарат за меньшие деньги, Galaxy S24 может быть очень выгодным выбором. Давайте посмотрим на аппарат и оценим
                    его.""",
                    cpu = "Qualcom Snapdragon 8 Elite",
                    battery = 5000,
                    ram = 8,
                    rom = 256,
                    display = "Dynamic AMOLED – 1080 x 2340",
                    camera = "3 (50 MP + 10 MP + 12 MP)",
                    storage = 10,
                    category_id = 1,
                    img_url = "/static/images/phone/galaxy-s25.avif"
                )
            db.session.add(test_product)
            db.session.commit()
            print(f"Продукт {test_product} добавлен.")
            if News.query.filter_by(title='Обзор Samsung Galaxy S25 Edge: эксклюзивный сверхтонкий флагман-пушинка').first() is None:
                test_news = News(
                title="Обзор Samsung Galaxy S25 Edge: эксклюзивный сверхтонкий флагман-пушинка",
                size="big",
                text="""Samsung Galaxy S25 Edge – самый тонкий смартфон 2025 года. Насколько оправдан новый тренд, при чем тут iPhone 17 Air, и чем Samsung пришлось пожертвовать ради достижения такого тонкого корпуса – разбираемся в обзоре Hi-Tech Mail.«Вау! А он точно настоящий?» — первое, о чем я подумал после распаковки Samsung Galaxy S25 Edge. Все дело в том, что при вполне большой диагонали в 6,7 дюймов новинка весит смехотворные 163 грамма, а толщина устройства составляет всего 5,8 мм.Держа его в руках, даже не понимаешь, как Samsung удалось уместить всю начинку в такой гаджет. Для сравнения, мой основной смартфон, iPhone 16 Pro, имеет 6,3-дюймовый экран и при толщине 8,3 мм весит 199 граммов. Оттого и в голове происходит диссонанс — вроде модель от Samsung больше, но при этом тоньше и легче.
И самое забавное, тактильно ощущается не столько его толщина, сколько его вес — буквально пушинка.Samsung Galaxy S25 Edge настолько тонкий и легкий, что даже сложно поверить, что это флагманский смартфон — что у меня, что у знакомых возникало ощущение, будто это какой-то сверхдешевый гаджет от ноунейм-бренда. При этом тут титановые рамки, есть влагозащита, а корпус и экран прикрыты закаленным стеклом Gorilla Glass Victus 2 и Gorilla Glass Ceramic 2 соответственно.
В общем, исполнение и материалы — флагманские.""",
                img_url="/static/images/news/AQAK5eTzth_XkPUQPwSa3873fPOzPbe45APJY87Vqawa_iVwMeGa0NNjnTkU2rRGXv7B0D2XL3rxfcj1dc58zfRWbrc.jpg"
                )
            db.session.add(test_news)
            db.session.commit()
            print(f"Новость {test_news} добавлена.")
            if News.query.filter_by(title='Обзор Nintendo Switch 2: игр нет, но вы держитесь').first() is None:
                test_news = News(
                title="Обзор Nintendo Switch 2: игр нет, но вы держитесь",
                size="medium",
                text="""Nintendo Switch 2 — это продолжение культовой и одной из самых популярных в мире консолей, Nintendo Switch 2017 года. Японцы значительно прокачали производительность, сделали новинку больше, повысили разрешение и даже завезли поддержку DLSS.
                Казалось бы, чего тут может не хватать?Как оказалось, многого. Почему не стоит бежать и покупать новую гибридную консоль от большой «N» — разбираемся в обзоре Hi-Tech Mail.В России купить гибридную консоль Nintendo можно в отечественной рознице, на маркетплейсах и у «серых» продавцов. В зависимости от выбора продавца цена может значительно отличаться.На текущий момент крупные сети еще не запустили свободные продажи Nintendo Switch 2, из-за чего цены на консоль хаотичны. Купить здесь и сейчас в магазинах, в том числе «серых», можно от 62 до 94 тысяч рублей! Это дороже, чем у ритейлеров, хоть они пока и предлагают лишь предзаказы.
                Также можно рассмотреть покупку на маркетплейсах, но имейте в виду, что зачастую это товар из-за границы, а значит, придется оплатить таможенную пошлину (около 7 тысяч рублей). Если новинка нужна здесь и сейчас, можно обратиться в магазин GIX, который предоставил Nintendo Switch 2 на обзор.""",
                img_url="/static/images/news/AQAKTqfSxlfRUlG6aTLDI-SyKByPUMPSADv636jqoBitss2Z1LRvKN68Y0qnoFwtqYRwTtxz_dFYF9Fo9diy4zWTeZU.jpg"
                )
            db.session.add(test_news)
            db.session.commit()
            print(f"Новость {test_news} добавлена.")
            if News.query.filter_by(title='Обзор Google Pixel 9a: достойная камера, а к остальному вопросы Google').first() is None:
                test_news = News(
                title="Обзор Google Pixel 9a: достойная камера, а к остальному вопросы Google",
                size="small",
                text="""Google Pixel 9a — один из самых странных смартфонов 2025 года. За время тестов он постоянно вызывал у меня вопросы, а скорость зарядки и вовсе вгоняла в депрессию. В обзоре рассказываю, к чему готовиться, если хотите себе этот смартфон. И почему его лучше не хотеть.
                По сравнению с прошлым поколением Pixel 9a изменился не сильно: внутри многое осталось на том же уровне. Это самый младший и бюджетный представитель линейки, который вроде бы позиционируется как субфлагман, но таких ощущений лично у меня не вызывает. Все протестировал, разобрался с главными плюсами и минусами устройства, а также сравнил его с Pixel 8a и базовым Pixel 9.В США смартфон представили 19 марта 2025 года, однако из-за необходимости пофиксить проблемные компоненты в продажу аппарат вышел только 10 апреля. В течение недели после этого новый «пиксель» стал доступен в странах Европы и Азии. До России добрался в середине мая.Официально в России смартфон не продается, но его можно заказать на уже упомянутых маркетплейсах. Правда, высока вероятность, что придется долго ждать доставку. Или платить сверху пошлину, если товар везут из-за границы. Более удобный вариант — купить Google Pixel 9a в магазине BigGeek: с быстрой доставкой и без всяких пошлин.
                """,
                img_url="/static/images/news/AQAKDi3oAkir_lPJ2NqbEDxCjvn2j4ErxyKvDffqHtlnkGixC8y9qJfAvyUT-ZgVa7lJlibFlEzZ64ratwvdC5wWkzo.jpg"
                )
            db.session.add(test_news)
            db.session.commit()
            print(f"Новость {test_news} добавлена.")
            
    app.run(debug=True, port=7010,host="0.0.0.0")

# git init
# git status
# git add .
# git commit -m "новое обновление"
# git push

#opencart