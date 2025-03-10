from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de MySQL
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "BdAplicacionNotas"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"  # Cambié la configuración aquí

# Inicializar MySQL
mysql = MySQL(app)

# Ruta para mostrar todas las notas
@app.route("/")
def home():
    conexion = mysql.connection
    cursor = conexion.cursor()  # Ahora se usa DictCursor por la configuración

    cursor.execute("SELECT * FROM notas")  
    notas = cursor.fetchall()
    cursor.close()

    return render_template("index.html", notas=notas)

# Ruta para obtener una nota por ID
@app.route("/nota/<int:id>")
def obtener_nota(id):
    conexion = mysql.connection
    cursor = conexion.cursor()  # Ahora se usa DictCursor por la configuración

    cursor.execute("SELECT * FROM notas WHERE Id = %s", (id,))
    nota = cursor.fetchone()
    cursor.close()

    if nota:
        # Corregí "Tiyulo" a "titulo"
        return f"<h1>{nota['titulo']}</h1><p>{nota['texto']}</p><a href='/'>Volver</a>"
    else:
        return "Registro no encontrado", 404

# Ruta para agregar una nueva nota
@app.route("/agregar", methods=["POST"])
def agregar_nota():
    if request.method == "POST":
        titulo = request.form["titulo"]
        texto = request.form["texto"]

        conexion = mysql.connection
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO notas (titulo, texto) VALUES (%s, %s)", (titulo, texto))
        conexion.commit()
        cursor.close()

        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)


