from datetime import date, datetime
from sqlalchemy.orm import backref
from servidor import db

# Tabla producto
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    price_buying = db.Column(db.Float)
    category = db.Column(db.String)
    lote = db.Column(db.Date)
    price_sale = db.Column(db.Float)
    amount = db.Column(db.Integer)
    

    def __init__(self, name, description, price_buying, category,lote, price_sale,amount):
        
        self.name= name
        self.description = description
        self.price_buying = price_buying
        self.category = category
        self.lote=lote
        self.price_sale = price_sale
        self.amount=amount

class User(db.Model):
    __tablename__ = 'user'

    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __init__(self, email, password):
        self.email=email
        self.password=password

class Admin(db.Model):
    __tablename__ = 'admin'
    id_admin = db.Column(db.String, unique=True, primary_key=True)
    password_admin = db.Column(db.String)
    def __init__(self,id_admin,password_admin):
        self.id_admin=id_admin
        self.password_admin=password_admin
        
class Lote(db.Model):
    __tablename__='lote'
    id_lote = db.Column(db.Integer, primary_key=True, autoincrement=True)
    due_date =db.Column(db.Date)
    amount = db.Column(db.Integer)
    def __init__(self,due_date,amount):

        self.due_date=due_date
        self.amount=amount


class Sold(db.Model):
    __tablename__='venta'

    id_venta=db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_product=db.Column(db.Integer)
    discount=db.Column(db.Float)
    id_factura=db.Column(db.ForeignKey("factura.id_factura"))
    amount_sold=db.Column(db.Integer)
    def __init__(self,discount,amount_sold, producto, fecha):
        product=Product.query.filter_by(id=producto).first()
        self.id_product=producto
        sudtotal=product.price_sale*int(amount_sold)
        newSubtotal=int(sudtotal*(1-int(discount)/100))
        factura = Factura(newSubtotal, fecha, 0.19, int(1.19*newSubtotal))


        db.session.add(factura)
        db.session.commit()
        self.id_factura=factura.id_factura
        self.discount=discount
        self.amount_sold=amount_sold

class Factura(db.Model):
    __tablename__='factura'
    id_factura=db.Column(db.Integer, primary_key=True, autoincrement=True)
    precio_venta=db.Column(db.Float)
    taxes=db.Column(db.Float)
    total=db.Column(db.Float)
    fecha_venta=db.Column(db.Date)
    def __init__(self, precio_venta, fecha_venta, taxes, total):
        self.precio_venta = precio_venta
        self.taxes=taxes
        self.total=total
        self.fecha_venta = fecha_venta


class Gastos(db.Model):
    __tablename__='gastos'
    id_gasto=db.Column(db.Integer, primary_key=True,autoincrement=True)
    price_buy=db.Column(db.Float)
    amount=db.Column(db.Integer)
    storagecost=db.Column(db.Float)
    servicecost=db.Column(db.Float)
    admincost=db.Column(db.Float)
    others=db.Column(db.Float)
    datetime=db.Column(db.Date)
    def  __init__(self,storagecost,servicecost,admincost, others, datetime,price_buy,amount):
        self.storagecost=storagecost
        self.servicecost=servicecost
        self.admincost=admincost
        self.others=others
        self.datetime = datetime
        self.price_buy=price_buy
        self.amount=amount
