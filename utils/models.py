from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


def init_models(db_instance):
    global db

    class User(db_instance.Model):
        __tablename__ = 'user'
        id = db_instance.Column(db_instance.Integer, primary_key=True)
        username = db_instance.Column(db_instance.String(80), unique=True, nullable=False)
        email = db_instance.Column(db_instance.String(120), unique=True, nullable=False)
        password = db_instance.Column(db_instance.String(200), nullable=False)
        role = db_instance.Column(db_instance.String(50), nullable=False, default='user')
        created_at = db_instance.Column(db_instance.TIMESTAMP(timezone=False), nullable=False, default=func.timezone('utc', func.now()))
        
        baskets = db_instance.relationship('Basket', backref='user', lazy=True)

        def __repr__(self):
            return f'<User {self.username}>'


    class Product(db_instance.Model):
            __tablename__ = 'product'
            id = db_instance.Column(db_instance.Integer, primary_key=True)
            name = db_instance.Column(db_instance.String(100), unique=True, nullable=False)
            price = db_instance.Column(db_instance.Integer, nullable=False)
            description = db_instance.Column(db_instance.String(4000), nullable=False)
            img_url = db_instance.Column(db_instance.String(255))
            cpu = db_instance.Column(db_instance.String(100), nullable=False)
            battery = db_instance.Column(db_instance.Integer, nullable=False)
            ram = db_instance.Column(db_instance.Integer, nullable=False)
            rom = db_instance.Column(db_instance.Integer, nullable=False)
            display = db_instance.Column(db_instance.String(100), nullable=False)
            camera = db_instance.Column(db_instance.String(100), nullable=False)
            liked_it = db_instance.Column(db_instance.Integer, default=0)
            storage = db_instance.Column(db_instance.Integer, default=1) 
            created_at = db_instance.Column(db_instance.TIMESTAMP(timezone=False), default=func.timezone('utc', func.now()))
            category_id = db_instance.Column(db_instance.Integer, nullable=False)
        
            baskets = db_instance.relationship('Basket', backref='product', lazy=True)

            def __repr__(self):
                return f'<Product {self.name}>'


    class Category(db_instance.Model):
        id = db_instance.Column(db_instance.Integer, primary_key=True)
        device = db_instance.Column(db_instance.String(50), nullable=False)
        company = db_instance.Column(db_instance.String(50), nullable=False)
        created_at = db_instance.Column(db_instance.TIMESTAMP(timezone=False), nullable=False, default=func.timezone('utc', func.now()))

        def __repr__(self):
            return f'<Category {self.device} - {self.company}>' 


    class Basket(db_instance.Model):
        __tablename__ = 'basket'
        id = db_instance.Column(db_instance.Integer, primary_key=True)
        user_id = db_instance.Column(db_instance.Integer, db_instance.ForeignKey('user.id'), nullable=False)
        product_id = db_instance.Column(db_instance.Integer, db_instance.ForeignKey('product.id'), nullable=False)
        added_date = db_instance.Column(db_instance.TIMESTAMP(timezone=False), nullable=False, default=func.timezone('utc', func.now()))
        active = db_instance.Column(db_instance.Boolean, nullable=False, server_default='true')

        def __repr__(self):
            return f'<Basket {self.user_id} - {self.product_id}>' 

    class Order(db_instance.Model):
        __tablename__ = 'orders'
        id = db_instance.Column(db_instance.Integer, primary_key=True)
        username = db_instance.Column(db_instance.String(80), nullable=False)
        email = db_instance.Column(db_instance.String(100),nullable=False)
        city = db_instance.Column(db_instance.String(100),nullable=False)
        address = db_instance.Column(db_instance.String(100),nullable=False)
        number = db_instance.Column(db_instance.Integer,nullable=False)
        message = db_instance.Column(db_instance.String(200),nullable=False)
        product_name = db_instance.Column(db_instance.String(500), nullable=False)
        added_date = db_instance.Column(db_instance.TIMESTAMP(timezone=False), nullable=False, default=func.timezone('utc', func.now()))
        total_price = db_instance.Column(db_instance.Integer,nullable=False)
        status = db_instance.Column(db_instance.String(50), nullable=False, server_default='shipped') #'pending', 'shipped', 'delivered', 'cancelled', 'refunded'

        def __repr__(self):
            return f'<Order {self.username} - {self.product_id}>' 


    return User, Product, Category, Basket, Order
