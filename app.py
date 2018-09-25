import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from flask_bootstrap import Bootstrap
from flask_wtf import Form


app = Flask(__name__)
Bootstrap(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:antonio1971@localhost/chapas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Origen(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20))
    #chapas = relationship("Chapa")


class Chapa(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20))
    ruta_imagen = db.Column(db.String(100))
    origen_id = db.Column(db.Integer, ForeignKey('origen.id'))
    origen = db.relationship('Origen', backref=db.backref('chapas', lazy=True))

@app.route('/')
def index():
    origenes = Origen.query.all()

    return render_template('upload.html',origenes=origenes)


@app.route("/upload", methods=['GET'])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    '''print (target)'''

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file.filename)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)


    print "upload"

    nombre = request.args.get('nombre')
    ruta = request.args.get('file')
    destination = "/".join([target, ruta])
    c = Chapa()

    c.nombre=nombre
    c.ruta_imagen = destination

    origen = request.args.get("origenes")
    print origen
    insertar(c,origen)

    print ('NOMBRE: ', nombre)
    return render_template("complete.html")


@app.route('/nuevoOrigen')
def nuevoOrigen():
    print "nuevoOrigen"
    origenes = listarOrigenes()
    return render_template("nuevoOrigen.html",origenes= origenes)


@app.route('/editarOrigen', methods=['GET'])
def editarOrigen():
    nombre = request.args.get('nombre')
    print nombre
    origen = buscarOrigen(nombre)
    return render_template('editarOrigen.html', origen=origen)


@app.route('/eliminarOrigen', methods=['GET'])
def eliminarOrigen():
    nonbre = request.args.get('nombre')
    eliminarOrigen(nonbre)
    return render_template('eliminarOrigen.htmlLA', origen = nonbre)


if __name__ == '__main__':
    app.run(debug=True)


def insertar(c, origen):
    #origen_substring = origen[1:-1]
    #print origen_substring
    o = Origen.query.filter_by(nombre=origen).first()
    o.chapas.append(c)
    #db.session.add(c)
    db.session.commit()


def listarOrigenes():
    origenes = Origen.query.all()
    return origenes


def buscarOrigen(origen):
    o = Origen.query.filter_by(nombre=origen).first()
    return o

def eliminarOrigen(origen):
    o = buscarOrigen(origen)
    db.session.delete(o)
    db.session.commit()