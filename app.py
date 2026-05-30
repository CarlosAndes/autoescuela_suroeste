from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import requests

GOOGLE_SCRIPT_URL="https://script.google.com/macros/s/AKfycbyNmE0s-1A4kTGyC428Y-540CtUY07bbH6Y2RzK5B7Zox8YPRqwgOVBWHpsKfovTsPg/exec"

app = Flask(__name__)
app.secret_key = "autoescuela_suroeste_2026"
# BASE DE DATOS

def crear_bd():

    conexion=sqlite3.connect("ventas.db")
    cursor=conexion.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS configuracion(

    curso TEXT,
    precio TEXT

    )

    """)

    cursor.execute(

    "SELECT * FROM configuracion"

    )

    datos=cursor.fetchall()

    if len(datos)==0:

        cursos=[

            ("A2","1140000"),
            ("B1","1440000"),
            ("C1","1670000"),
            ("C2","1580000"),
            ("A2+B1","2290000"),
            ("A2+C1","2490000"),
            ("LICENCIA","110000"),
            ("LICENCIA_PROMO","190000")

        ]

        cursor.executemany(

        "INSERT INTO configuracion(curso,precio) VALUES(?,?)",

        cursos

        )

        conexion.commit()

    conexion.close()


crear_bd()
# OBTENER PRECIO

def obtener_precio(curso):

    conexion=sqlite3.connect("ventas.db")
    cursor=conexion.cursor()

    cursor.execute(
    "SELECT precio FROM configuracion WHERE curso=?",
    (curso,)
    )

    resultado=cursor.fetchone()

    conexion.close()

    if resultado:
        return resultado[0]

    return "0"


def formato_precio(valor):

    return "{:,}".format(
        int(valor)
    ).replace(",", ".")

# INICIO

@app.route("/")
def inicio():
    return render_template("index.html")


# MOTO A2

@app.route("/moto")
def moto():

    curso = {

    "titulo":"🏍 Categoría A2",
    "imagen":"moto.jpg",
    "etiqueta":"Más solicitada",
    "descripcion":"Curso completo para motocicleta",

    "precio":"$"+formato_precio(
        obtener_precio("A2")
    ),

    "licencia":"$"+formato_precio(
        obtener_precio("LICENCIA")
    ),

    "incluye":[

        "Exámenes médicos (Andes)",
        "28 clases teoría grupal",
        "15 clases prácticas",
        "Certificado conducción"

    ]

}

    return render_template(
        "curso.html",
        curso=curso
    )


# CARRO B1

@app.route("/carro")
def carro():

    curso = {

        "titulo":"🚘 Categoría B1",
        "imagen":"carro.jpg",
        "etiqueta":"Más solicitada",
        "descripcion":"Curso completo carro particular",
       "precio":"$"+formato_precio(
    obtener_precio("B1")
),

"licencia":"$"+formato_precio(
    obtener_precio("LICENCIA")
),

        "incluye":[

            "Exámenes médicos",
            "30 clases teoría",
            "Prácticas personalizadas",
            "Certificado conducción"

        ]

    }

    return render_template(
        "curso.html",
        curso=curso
    )


# SERVICIO PUBLICO C1

@app.route("/publico")
def publico():

    curso = {

        "titulo":"🚕 Categoría C1",
        "imagen":"publico.jpg",
        "etiqueta":"Servicio público",
        "descripcion":"Curso servicio público",
        "precio":"$"+obtener_precio("C1"),
        "precio":"$"+formato_precio(
    obtener_precio("C1")
),

"licencia":"$"+formato_precio(
    obtener_precio("LICENCIA")
),
        "incluye":[

            "Exámenes médicos",
            "35 clases teoría",
            "Prácticas personalizadas",
            "Certificado"

        ]

    }

    return render_template(
        "curso.html",
        curso=curso
    )


# CAMION C2

@app.route("/camion")
def camion():

    curso = {

        "titulo":"🚛 Categoría C2",
        "imagen":"camion.jpg",
        "etiqueta":"Vehículos pesados",
        "descripcion":"Curso camión",
       "precio":"$"+formato_precio(
    obtener_precio("C2")
),

"licencia":"$"+formato_precio(
    obtener_precio("LICENCIA")
),

        "incluye":[

            "Exámenes médicos",
            "30 clases teoría",
            "Prácticas personalizadas",
            "Certificado"

        ]

    }

    return render_template(
        "curso.html",
        curso=curso
    )


# PROMO A2 + B1

@app.route("/promo_a2_b1")
def promo1():

    curso = {

        "titulo":"⭐ A2 + B1",
        "imagen":"promo_a2_b1.jpg",
        "etiqueta":"PROMOCIÓN",
        "descripcion":"Moto + Carro Particular",
        "precio":"$"+formato_precio(
    obtener_precio("A2+B1")
),

"licencia":"$"+formato_precio(
    obtener_precio("LICENCIA_PROMO")
),

        "incluye":[

            "Exámenes médicos",
            "30 clases teoría",
            "Prácticas personalizadas",
            "Certificado"

        ]

    }

    return render_template(
        "curso.html",
        curso=curso
    )


# PROMO A2 + C1

@app.route("/promo_a2_c1")
def promo2():

    curso = {

        "titulo":"⭐ A2 + C1",
        "imagen":"promo_a2_c1.jpg",
        "etiqueta":"PROMOCIÓN",
        "descripcion":"Moto + Servicio público",
        "precio":"$"+formato_precio(
    obtener_precio("A2+C1")
),

"licencia":"$"+formato_precio(
    obtener_precio("LICENCIA_PROMO")
),

        "incluye":[

            "Exámenes médicos",
            "35 clases teoría",
            "Prácticas personalizadas",
            "Certificado"

        ]

    }

    return render_template(
        "curso.html",
        curso=curso
    )

@app.route(
"/separar_cupo",
methods=["GET","POST"]
)
def separar_cupo():

    curso=request.args.get("curso")

    if request.method=="POST":

        nombre=request.form["nombre"]
        tipo=request.form["tipo_documento"]
        doc=request.form["documento"]
        cel=request.form["celular"]
        correo=request.form["correo"]
        fecha=request.form["fecha_nacimiento"]
        leer=request.form["sabe_leer"]
        pago=request.form["tipo_pago"]

        c1=request.form.get(
            "tiene_c1",
            "No aplica"
        )

        respuesta=requests.post(

            GOOGLE_SCRIPT_URL,

            json={

                "curso":curso,
                "nombre":nombre,
                "tipo_documento":tipo,
                "documento":doc,
                "celular":cel,
                "correo":correo,
                "fecha_nacimiento":fecha,
                "tiene_c1":c1,
                "sabe_leer":leer,
                "tipo_pago":pago,
                "comprobante":"Pendiente"

            }

        )

        print("STATUS:",respuesta.status_code)
        print("RESPUESTA:",respuesta.text)

        return """

<!DOCTYPE html>

<html lang="es">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>
Inscripción realizada
</title>

<style>

*{
margin:0;
padding:0;
box-sizing:border-box;
font-family:Arial,sans-serif;
}

body{

background:
linear-gradient(
135deg,
#f0fff4,
#eef4ff
);

min-height:100vh;

display:flex;

justify-content:center;

align-items:center;

padding:25px;

}

.card{

background:white;

max-width:850px;

width:100%;

padding:60px;

border-radius:35px;

text-align:center;

box-shadow:
0 20px 60px rgba(0,0,0,.1);

}

.check{

font-size:90px;

width:130px;

height:130px;

border-radius:100%;

background:#ebfff1;

display:flex;

justify-content:center;

align-items:center;

margin:auto;

}

h1{

font-size:50px;

color:#11a847;

margin-top:25px;

}

p{

margin-top:20px;

font-size:22px;

line-height:1.8;

color:#666;

}

.info{

margin-top:35px;

background:#f7fff8;

padding:30px;

border-radius:20px;

font-size:20px;

line-height:1.8;

}

.btn{

display:inline-block;

margin-top:35px;

background:#25D366;

color:white;

padding:18px 35px;

text-decoration:none;

border-radius:15px;

font-size:22px;

font-weight:bold;

transition:.3s;

}

.btn:hover{

transform:scale(1.05);

}

.footer{

margin-top:30px;

color:#777;

}

</style>

</head>

<body>

<div class="card">

<div class="check">

✅

</div>

<h1>

¡Inscripción realizada!

</h1>

<p>

Tu inscripción fue registrada correctamente.

En Autoescuela SUROESTE estamos felices de acompañarte en este nuevo paso 🚗🏍️

</p>

<div class="info">

🎉 Hemos recibido tus datos correctamente.

Muy pronto nos comunicaremos contigo para continuar el proceso.

</div>

<a
class="btn"
href="https://wa.me/573113416655">

💬 Hablar por WhatsApp

</a>

<div class="footer">

Gracias por confiar en Autoescuela SUROESTE ❤️

</div>

</div>

</body>

</html>

        """

    precio = ""

    curso_texto = str(curso)

    if "A2 + B1" in curso_texto:
        precio = obtener_precio("A2+B1")

    elif "A2 + C1" in curso_texto:
        precio = obtener_precio("A2+C1")

    elif "A2" in curso_texto:
        precio = obtener_precio("A2")

    elif "B1" in curso_texto:
        precio = obtener_precio("B1")

    elif "C1" in curso_texto:
        precio = obtener_precio("C1")

    elif "C2" in curso_texto:
        precio = obtener_precio("C2")

    return render_template(
        "separar_cupo.html",
        curso=curso,
        precio=precio
    )

# PANEL ADMIN
@app.route(
    "/admin_login",
    methods=["GET","POST"]
)
def admin_login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        clave = request.form["clave"]

        if (
            usuario == "admin"
            and
            clave == "Suroeste2026"
        ):

            session["admin"] = True

            return redirect(
                url_for("admin")
            )

    return render_template(
        "admin_login.html"
    )

# PANEL ADMIN

@app.route(
    "/admin",
    methods=["GET","POST"]
)
def admin():

    if "admin" not in session:

        return redirect(
            url_for("admin_login")
        )

    conexion = sqlite3.connect(
        "ventas.db"
    )

    cursor = conexion.cursor()

    if request.method == "POST":

        cursor.execute(
            "SELECT curso FROM configuracion"
        )

        cursos = cursor.fetchall()

        for curso in cursos:

            nombre = curso[0]

            nuevo_precio = request.form.get(
                nombre
            )

            nuevo_precio = nuevo_precio.replace(
                ".",
                ""
            )

            cursor.execute(

                """
                UPDATE configuracion
                SET precio=?
                WHERE curso=?
                """,

                (
                    nuevo_precio,
                    nombre
                )

            )

        conexion.commit()

    cursor.execute(

        """
        SELECT curso, precio
        FROM configuracion
        """

    )

    datos = cursor.fetchall()

    conexion.close()

    return render_template(
        "admin.html",
        datos=datos
    )


if __name__=="__main__":
    app.run(
        debug=True
    )