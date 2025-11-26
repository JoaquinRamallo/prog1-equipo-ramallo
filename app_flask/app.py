# ----------------------------------------------------
# APLICACIÓN FLASK
# ----------------------------------------------------
import json
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

# ============================================================
# IMPORTS AGREGADOS DE utilidades_avanzadas.py
# ============================================================
import re
from functools import reduce
import os

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

# ============================================================
# FUNCIONES AGREGADAS DE utilidades_avanzadas.py
# ============================================================

# -----------------------
# LAMBDA / MAP / FILTER / REDUCE
# -----------------------
def procesar_transacciones_numeros(lista):
    """Ejemplo con lista de números: filter (positivos), map (aplicar impuesto 10%), reduce (sumar)."""
    positivos = list(filter(lambda x: x > 0, lista))
    con_impuesto = list(map(lambda x: round(x * 1.10, 2), positivos))
    total = reduce(lambda a, b: a + b, con_impuesto, 0)
    return positivos, con_impuesto, total

def resumen_transacciones_dicts(transacciones):
    """Trabaja con lista de diccionarios de transacciones (forma usada en la app)."""
    montos = [t.get('monto', 0) for t in transacciones]
    return procesar_transacciones_numeros(montos)

# -----------------------
# TUPLAS (logs inmutables)
# -----------------------
def crear_log_tuple(usuario, accion):
    fecha = datetime.now().isoformat()
    return (usuario, accion, fecha)

# -----------------------
# SETS (categorías únicas)
# -----------------------
def categorias_unicas(transacciones):
    """Extrae una categoría simple a partir de la primera palabra de la descripción."""
    categorias = set()
    for t in transacciones:
        desc = t.get('descripcion', '') or ''
        desc = desc.strip()
        if not desc:
            continue
        categoria = desc.split()[0].lower()
        categorias.add(categoria)
    return categorias

# -----------------------
# RECURSIVIDAD (interés compuesto)
# -----------------------
def interes_compuesto_recursivo(capital, tasa, años):
    if años <= 0:
        return capital
    return interes_compuesto_recursivo(capital * (1 + tasa), tasa, años - 1)

# -----------------------
# ARCHIVOS PLANOS (guardar logs)
# -----------------------
def guardar_log_texto(texto, archivo=None):
    if archivo is None:
        archivo = os.path.join(os.path.dirname(__file__), 'logs_adicionales.txt')
    with open(archivo, 'a', encoding='utf-8') as f:
        f.write(texto + '\n')
    return archivo

# -----------------------
# MATRICES (historial)
# -----------------------
def matriz_historial(transacciones):
    """Convierte lista de transacciones en matriz [descripcion, monto]"""
    return [[t.get('descripcion',''), t.get('monto',0)] for t in transacciones]

# -----------------------
# FUNCIONES UTILES PARA DEMOSTRACIÓN
# -----------------------
def ejemplo_todo(transacciones):
    """Ejecuta varios ejemplos y devuelve un dict con resultados para mostrar en app si se desea."""
    positivos, con_impuesto, total = resumen_transacciones_dicts(transacciones)
    cats = categorias_unicas(transacciones)
    matriz = matriz_historial(transacciones)
    log = crear_log_tuple('demo_user', 'resumen_ejemplo')
    saved = guardar_log_texto(str(log))
    return {
        'positivos': positivos,
        'con_impuesto': con_impuesto,
        'total': total,
        'categorias': cats,
        'matriz': matriz,
        'log_guardado_en': saved
    }

# ============================================================
# FIN FUNCIONES AGREGADAS DE utilidades_avanzadas.py
# ============================================================

# -------------------------------------------
# VALIDACIONES DE EMAIL Y CONTRASEÑA
# ============================================================
# FUNCIONES REEMPLAZADAS DE utilidades_avanzadas.py (REGEX)
# ============================================================
# -------------------------------------------

def validar_email(email):
    """Valida email con regex - FUNCIÓN DE utilidades_avanzadas.py"""
    patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return re.match(patron, email) is not None


def validar_password(password):
    """Valida que la contraseña tenga al menos una mayúscula y un número - FUNCIÓN DE utilidades_avanzadas.py"""
    patron = r"^(?=.*[A-Z])(?=.*\d).{6,}$"
    return re.match(patron, password) is not None


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