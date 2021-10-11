from itertools import product
from flask import Flask,request,render_template,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app = Flask(__name__)
PORT=5000
DEBUG=False
# 'postgresql://<usuario>:<contraseña>@<direccion de la db>:<puerto>/<nombre de la db>
#heapp.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/tiendadb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rogpgtywsaahgh:52cb52c2a7a44d753a2f1c185527b8f59be99d14f25531c7cab7ad4fa27154e4@ec2-3-221-100-217.compute-1.amazonaws.com:5432/d5m703a0li34gb'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cpdxxdhbrovthw:25d3ec47451f8e836675f3227c1713ee6ad8a0319f81895a5f666d4363029d46@ec2-52-207-47-210.compute-1.amazonaws.com:5432/d80ef8qqjqdhd0'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'some-secret-key'


db = SQLAlchemy(app)

# Importar los modelos

from models import Product, User, Admin, Lote, Sold, Factura, Gastos


# Crear el esquema de la DB
db.create_all()  
db.session.commit()





# Rutas de paginas


@app.route('/')
def inicio():
    adminVerif=Admin.query.filter_by(id_admin='admin',password_admin='0000').first()
    if(adminVerif == None):
        #creacion de admin
        admins=Admin("admin","0000")
        db.session.add(admins)
        db.session.commit()    
    return redirect('login')

@app.route('/login')
def get_login():
    adminveri=Admin.query.filter_by(id_admin='admin',password_admin='0000').first()
    if(adminveri == None):
        #creacion de admin
        admins=Admin("admin","0000")
        db.session.add(admins)
        db.session.commit()  
    return render_template("login.html")

@app.route('/home')
def get_home():
    return render_template("home.html")
#paginas de login a singup
@app.route('/signup')
def get_signup():
    return render_template("signup.html")
@app.route('/forgetpass')
def get_forget():
    return render_template("forgetpass.html")
#paginas enlaces del home     
@app.route('/gastos')
def get_gastos():
    gastos = db.session.query(Gastos).all()
    total = 0
    for gasto in gastos:
        total = total + int(gasto.price_buy)+ int(gasto.storagecost)+ int(gasto.servicecost) + int(gasto.admincost) + int(gasto.others)
    print(total)
    return render_template("gastos.html", gastos=gastos, total=total)

@app.route('/registrarGastos')
def set_gastos():

    return render_template("registroGastos.html")



@app.route('/ventas')
def get_ventas():
    consulta = db.session.query(Product).all()
    return render_template("ventas.html",datos = consulta)  


@app.route('/inventario')
def inventario():
    consulta = db.session.query(Product).all()
    return render_template("inventario.html",datos = consulta)    

@app.route('/resproducto')
def resproducto():
    return render_template("registroproducto.html")


@app.route('/admin')
def homeadmin():
    return render_template("admin.html")

#funciones

#verificacion en login
@app.route('/verify_user', methods=["GET",'POST'])
def verify_user():
    
    email=request.form["email"]
    password=request.form["password"]

    userdb=User.query.filter(User.password==password,User.email==email)
    try:
        if(userdb[0] is not None):
            return redirect("home")
    except:
        return redirect("login")


#verificacion login para el admin

@app.route('/loginadmin', methods=['POST'])
def verify_admin():
    adminId=request.form["adminId"]
    password=request.form["password"]    
    admindb=Admin.query.filter_by(id_admin= adminId,password_admin=password).first()
    if(admindb != None):
        return redirect("homeadmin")
    
    return redirect("admin")
#ver tabla de usuarios modo admin

@app.route('/homeadmin')
def tablausuarios():
    consultau = db.session.query(User).all()
    print(consultau)
    return render_template("homeadmin.html",datos = consultau)

@app.route('/deleteuser', methods=["GET",'POST'])
def del_user():
    requestdata=request.form
    id=requestdata["id"]
    user=User.query.filter_by(id_user=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect("homeadmin")

#ccrear usuario
@app.route('/create_user', methods=["GET",'POST'])
def create_user():
    if request.form["email"]=="" or request.form["password"]=="":
        return redirect("signup")
    email = request.form["email"]
    password = request.form["password"]
    user = User(email, password)
    db.session.add(user)
    db.session.commit()
    return redirect("login")

@app.route('/create_product', methods=['GET','POST'])
def create_product():
    if request.form["name"]=="":
        return redirect("resproducto")
    name = request.form["name"]
    description = request.form["description"]
    pricebuy = request.form["price_buying"]
    category = request.form["category"]
    lote=request.form["lote"]
    price_sale= request.form["price_sale"]
    amount = request.form["amount"]
    if lote=="":
        lote=date(1000, 1,1)

    producto = Product(name, description,pricebuy,category,lote,price_sale,amount)
    gasto = Gastos(0,0,0,0,date.today(),pricebuy,amount)
    db.session.add(producto)
    db.session.add(gasto)
    db.session.commit()
    return redirect("inventario")


@app.route('/registrar_venta', methods=['POST'])
def registrar_venta():
    producto=request.form["producVent"]
    cantidad=request.form["cantidad"]
    descuento=request.form["descuento"]
    fecha = (date.today())
    if cantidad=="" or cantidad=="0":
        return redirect("ventas")
    elif descuento=="":
        descuento=0
    else:
        descuento=int(descuento)

    changeCantidad = Product.query.filter_by(id=producto).first()
    if int(changeCantidad.amount) < int(cantidad):
        return "No hay suficiente producto"
    

    changeCantidad.amount= int(changeCantidad.amount)-int(cantidad)
    venta = Sold(descuento, cantidad, producto, fecha)
    
    db.session.add(venta)
    db.session.commit()
    global id_facturar
    id_facturar=venta.id_factura
    print(id_facturar)
    return redirect("facturar")

@app.route('/deleteproduct', methods=['POST'])
def del_product():
    requestdata=request.form
    id=requestdata["id_product"]
    productdb=Product.query.filter_by(id=id).first()
    db.session.delete(productdb)
    db.session.commit()
    return redirect("inventario")



@app.route('/save_spents', methods=['POST'])
def save_spents():

    storagecost = request.form["storagecost"]
    servicecost = request.form["servicecost"]
    admincost = request.form["admincost"]
    others = request.form["others"]
    if storagecost=="":
        storagecost="0"
    if servicecost=="":
        servicecost="0"
    if admincost=="":
        admincost="0"
    if others=="":
        others="0"
    if not(others=="0" and storagecost=="0" and servicecost=="0" and admincost=="0"):
            fecha = (date.today())
            gastos = Gastos(storagecost, servicecost, admincost, others, fecha, 0, 0)
            db.session.add(gastos)
            db.session.commit()

    return redirect("registrarGastos")

#Rutas de metodos
@app.route('/updatePasswordUser', methods=['GET','POST'])
def get_vencido():
    if request.method == 'POST':
        request_data = request.form
        email = request_data['email']
        newPassword = request_data['newPassword']
        changeUser = User.query.filter_by(email=email).first()
        retorno = "Actualización exitosa" 

        if changeUser==None:
            #aqui se debe poner una alerta en el navegador que diga que el correo no existe
            retorno = "Fallo de actualización, "  + email + " no existe en la base de datos."
        else:
            changeUser.password = newPassword
            db.session.commit() 
        flash(retorno)
        return render_template("forgetpass.html")

    elif request.method == 'GET':
        return render_template("forgetpass.html")


@app.route('/facturas', methods=['GET'])
def get_facturas():

    factura = db.session.query(Factura).all()
    return render_template("facturas.html", factura=factura)

  



@app.route('/facturar', methods=['GET'])
def get_facturar():

    factura = Factura.query.filter_by(id_factura=id_facturar).first()

    if factura==None:
        print(id_facturar)
        return "Error: Hay un error en el id de la factura!"
    else:

        ventas = Sold.query.filter_by(id_factura=factura.id_factura).first()
        producto = Product.query.filter_by(id=ventas.id_product).first()
        
        return render_template("facturar.html", factura=factura, ventas=ventas, producto=producto)


if __name__ == "__main__":
    app.run(port=PORT,debug=DEBUG)