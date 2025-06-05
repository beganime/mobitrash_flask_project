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
            cpu = db_instance.Column(db_instance.String(100), nullable=False)
            battery = db_instance.Column(db_instance.Integer, nullable=False)
            ram = db_instance.Column(db_instance.Integer, nullable=False)
            rom = db_instance.Column(db_instance.Integer, nullable=False)
            display = db_instance.Column(db_instance.String(100), nullable=False)
            camera = db_instance.Column(db_instance.String(100), nullable=False)
            liked_it = db_instance.Column(db_instance.Integer, default=0)
            storage = db_instance.Column(db_instance.Integer, default=0) 
            created_at = db_instance.Column(db_instance.TIMESTAMP(timezone=False), nullable=False, default=func.timezone('utc', func.now()))
        
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


    return User, Product, Category, Basket
