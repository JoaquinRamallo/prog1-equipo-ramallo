# ----------------------------------------------------
# APLICACIÓN FLASK
# ----------------------------------------------------
import json
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "mi_clave_secreta"


# ----------------------------------------------------
# BASE DE DATOS (JSON SEGURO)
# ----------------------------------------------------

def cargar_usuarios():
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {k.lower(): v for k, v in data.items()}
    except:
        return {}

def guardar_usuarios(data):
    with open('usuarios.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def cargar_transacciones():
    try:
        with open('transacciones.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {k.lower(): v for k, v in data.items()}
    except:
        return {}

def guardar_transacciones(data):
    with open('transacciones.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def cargar_inversiones():
    try:
        with open('inversiones.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {k.lower(): v for k, v in data.items()}
    except:
        return {}

def guardar_inversiones(data):
    with open('inversiones.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# -------------------------------------------
# VALIDACIONES DE EMAIL Y CONTRASEÑA
# -------------------------------------------

def validar_email(email):
    """Valida estructura mínima de email."""
    if "@" not in email:
        return False

    pos_arroba = email.index("@")

# Debe tener algo antes del @

    if pos_arroba == 0:
        return False

# Debe tener un . después del @
    if "." not in email[pos_arroba:]:
        return False

    return True


def validar_password(password):
    """La contraseña debe tener 1 mayúscula y 1 carácter especial."""
    tiene_mayuscula = False
    tiene_especial = False
    especiales = "!@#$%&*?."

    for caracter in password:
        if caracter.isupper():
            tiene_mayuscula = True
        if caracter in especiales:
            tiene_especial = True

    return tiene_mayuscula and tiene_especial


# ----------------------------------------------------
# LOGIN
# ----------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        session.clear()
        return render_template('iniciar_sesion.html')

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    usuarios = cargar_usuarios()


    if not validar_email(email):
        return render_template("iniciar_sesion.html",
                               error="Ingresá un email válido.")


    if email not in usuarios:
        return render_template("iniciar_sesion.html",
                               error="No existe una cuenta con ese correo.")


    if usuarios[email]["password"] != password:
        return render_template("iniciar_sesion.html",
                               error="Contraseña incorrecta.")

    session["usuario_actual"] = email
    return redirect(url_for("inicio"))



# ----------------------------------------------------
# INICIO
# ----------------------------------------------------
@app.route("/inicio")
def inicio():
    if "usuario_actual" not in session:
        return redirect(url_for("login"))

    email = session["usuario_actual"]
    usuarios = cargar_usuarios()
    usuario = usuarios[email]

    transacciones = cargar_transacciones().get(email, [])

    ingresos = sum(t["monto"] for t in transacciones if t["tipo"] == "ingreso")
    gastos = sum(abs(t["monto"]) for t in transacciones if t["tipo"] == "gasto")

    return render_template("inicio.html",
                           nombre=usuario["nombre"],
                           saldo=usuario["saldo"],
                           ingresos=ingresos,
                           gastos=gastos)



# ----------------------------------------------------
# CREAR CUENTA
# ----------------------------------------------------
@app.route('/crear_cuenta', methods=['GET', 'POST'])
def crear_cuenta():
    if request.method == 'GET':
        return render_template('crear_cuenta.html')

    nombre = request.form.get("nombre")
    email = request.form.get("email").strip().lower()
    password = request.form.get("password")

    usuarios = cargar_usuarios()


    if not validar_email(email):
        return render_template('crear_cuenta.html',
                               error="El email no tiene un formato válido.")


    if not validar_password(password):
        return render_template(
            'crear_cuenta.html',
            error="La contraseña debe tener al menos UNA mayúscula y UN carácter especial (!@#$%&*?)."
        )

    if email in usuarios:
        return render_template('crear_cuenta.html', error="Ese correo ya existe.")

    usuarios[email] = {
        "nombre": nombre,
        "password": password,
        "saldo": 0
    }

    guardar_usuarios(usuarios)
    return render_template("iniciar_sesion.html", mensaje="Cuenta creada correctamente.")


# ----------------------------------------------------
# PAGAR (GASTO)
# ----------------------------------------------------
@app.route('/pagar', methods=['GET', 'POST'])
def pagar():
    if "usuario_actual" not in session:
        return redirect(url_for("login"))

    email = session["usuario_actual"]
    usuarios = cargar_usuarios()
    usuario = usuarios[email]

    if request.method == "POST":
        descripcion = request.form.get("descripcion")
        monto = float(request.form.get("monto", 0))

#Validar saldo suficiente

        if monto > usuario["saldo"]:
            return render_template(
                "pagar.html",
                usuario=usuario["nombre"],
                saldo=usuario["saldo"],
                error="No tenés saldo suficiente para realizar este pago."
            )

#validar monto positivo

        usuario["saldo"] -= monto
        guardar_usuarios(usuarios)

        transacciones = cargar_transacciones()
        transacciones.setdefault(email, []).insert(0, {
            "fecha": datetime.now().isoformat(),
            "descripcion": descripcion,
            "monto": -monto,
            "tipo": "gasto"
        })
        guardar_transacciones(transacciones)

        return redirect(url_for("inicio"))

    return render_template("pagar.html", usuario=usuario["nombre"], saldo=usuario["saldo"])



# ----------------------------------------------------
# INGRESO
# ----------------------------------------------------
@app.route('/ingreso', methods=['GET', 'POST'])
def ingreso():
    if "usuario_actual" not in session:
        return redirect(url_for("login"))

    email = session["usuario_actual"]
    usuarios = cargar_usuarios()
    usuario = usuarios[email]

    if request.method == "POST":
        fuente = request.form.get("fuente")
        monto = float(request.form.get("monto", 0))

        usuario["saldo"] += monto
        guardar_usuarios(usuarios)

        transacciones = cargar_transacciones()
        transacciones.setdefault(email, []).insert(0, {
            "fecha": datetime.now().isoformat(),
            "descripcion": f"Ingreso: {fuente}",
            "monto": monto,
            "tipo": "ingreso"
        })
        guardar_transacciones(transacciones)

        return redirect(url_for("inicio"))

    return render_template("ingreso.html", nombre=usuario["nombre"], saldo=usuario["saldo"])



# ----------------------------------------------------
# MOVIMIENTOS
# ----------------------------------------------------
@app.route('/movimientos')
def movimientos():
    if "usuario_actual" not in session:
        return redirect(url_for('login'))

    usuario = session["usuario_actual"]

    usuarios = cargar_usuarios()
    saldo_real = usuarios[usuario]["saldo"]

    transacciones = cargar_transacciones().get(usuario, [])

    return render_template(
        "movimientos.html",
        transacciones=transacciones,
        saldo=saldo_real
    )

# ----------------------------------------------------
# INVERSIONES
# ----------------------------------------------------

@app.route('/inversiones', methods=['GET', 'POST'])
def inversiones():
    usuario = session.get("usuario_actual", "").lower()

    inversiones = cargar_inversiones()
    usuarios = cargar_usuarios()

    if usuario not in inversiones:
        inversiones[usuario] = {
            "Fondos Comunes": 0,
            "Acciones": 0,
            "Bonos": 0,
            "Plazo Fijo": 0
        }

    if usuario not in usuarios:
        return redirect(url_for("login"))

    if request.method == "POST":
        monto = float(request.form.get("monto", 0))
        tipo = request.form.get("tipo")

#Validar saldo suficiente

        if monto > usuarios[usuario]["saldo"]:
            return render_template(
                "inversiones.html",
                totales=inversiones[usuario],
                saldo=usuarios[usuario]["saldo"],
                error="No tenés saldo suficiente para realizar esta inversión."
            )

#Validacion de saldo positivo

        usuarios[usuario]["saldo"] -= monto
        guardar_usuarios(usuarios)

        inversiones[usuario][tipo] += monto
        guardar_inversiones(inversiones)

        transacciones = cargar_transacciones()
        transacciones.setdefault(usuario, []).insert(0, {
            "fecha": datetime.now().isoformat(),
            "descripcion": f"Inversión en {tipo}",
            "monto": -monto,
            "tipo": "gasto"
        })
        guardar_transacciones(transacciones)

        return redirect(url_for('inversiones'))

    totales = inversiones[usuario]
    saldo = usuarios[usuario]["saldo"]

    return render_template("inversiones.html",
                           totales=totales,
                           saldo=saldo)


# ----------------------------------------------------
# PERFIL
# ----------------------------------------------------
@app.route('/perfil')
def perfil():
    usuario = session.get("usuario_actual")

    if not usuario:
        return redirect(url_for("login"))

    usuarios = cargar_usuarios()
    datos = usuarios.get(usuario, {})

    return render_template("perfil.html", datos=datos, email=usuario)


# ----------------------------------------------------
# OLVIDÉ CONTRASEÑA
# ----------------------------------------------------
@app.route('/olvide_contra')
def olvide_contra():
    return render_template('olvide_contra.html')


@app.route('/procesar_olvide_contra', methods=['POST'])
def procesar_olvide_contra():
    email = request.form.get('email', '').strip().lower()
    usuarios = cargar_usuarios()

    if not email:
        return render_template('olvide_contra.html',
                               error="Ingresá tu email.")

    if email not in usuarios:
        return render_template('olvide_contra.html',
                               error="Ese correo no existe.")

    mensaje = f"Se envió un enlace de recuperación a {email}."
    return render_template('olvide_contra.html', mensaje=mensaje)

# ----------------------------------------------------
# CAMBIAR CONTRASEÑA
# ----------------------------------------------------
@app.route('/cambiar_contra', methods=['GET', 'POST'])
def cambiar_contra():

    usuario = session.get("usuario_actual")

    if not usuario:
        return redirect(url_for('login'))

    if request.method == "GET":
        return render_template("cambiar_contra.html")

    nueva = request.form.get("password")

    usuarios = cargar_usuarios()
    usuarios[usuario]["password"] = nueva
    guardar_usuarios(usuarios)

    return redirect(url_for("perfil"))


# ----------------------------------------------------
# CERRAR SESIÓN
# ----------------------------------------------------
@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()
    return redirect(url_for("login"))



# ----------------------------------------------------
# EJECUCIÓN
# ----------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)