from flask import Flask, render_template, request, redirect, url_for, jsonify
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
@app.route("/notas")
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
        # Corregí"titulo"
        return f"<h1>{nota['titulo']}</h1><p>{nota['texto']}</p><a href='/'>Volver</a>"
    else:
        return "Registro no encontrado", 404

# Ruta para agregar una nueva nota
@app.route("/agregar_nota", methods=["POST"])
def agregar_nota():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        print(f"Titulo recibido: {titulo}")  # Depuración
        if not titulo:
            return "Error: El campo 'titulo' es requerido", 400

        texto = request.form.get("texto")
        print(f"Texto recibido: {texto}")  # Depuración
        conexion = mysql.connection
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO notas (titulo, texto) VALUES (%s, %s)", (titulo, texto))
        conexion.commit()
        cursor.close()
        return "Nota agregada con éxito"

# Ruta para crear una nueva nota desde JSON
@app.route("/crear_nota", methods=["POST"])
def crear_nota():
    # Verifica si la solicitud contiene JSON
    if not request.is_json:
        return jsonify({"error": "La solicitud debe tener Content-Type 'application/json'"}), 400

    try:
        data = request.get_json(force=True)  # Usa force=True para forzar la lectura de JSON
    except Exception as e:
        return jsonify({"error": f"Error al procesar JSON: {str(e)}"}), 400

    # Verifica que los datos requeridos estén presentes
    if not data or "titulo" not in data or "texto" not in data:
        return jsonify({"error": "Faltan datos: 'titulo' y 'texto' son requeridos"}), 400

    titulo = data["titulo"]
    texto = data["texto"]

    # Conectar a MySQL e insertar los datos
    try:
        conexion = mysql.connection
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO notas (titulo, texto) VALUES (%s, %s)", (titulo, texto))
        conexion.commit()
        cursor.close()

        return jsonify({"mensaje": "Nota creada exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {str(e)}"}), 500

# Ruta para ver todas las notas
@app.route("/notas", methods=["GET"])
def obtener_todas_las_notas():
    conexion = mysql.connection
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM notas")
    notas = cursor.fetchall()  # Lista de diccionarios
    
    cursor.close()
    
    return jsonify(notas)  # Devolver todo en formato JSON

#ruta para eliminar nota
@app.route("/eliminar_nota/<int:id>", methods=["DELETE"])
def eliminar_nota(id):
    conexion = mysql.connection
    cursor = conexion.cursor()

    # Verifica si la nota existe
    cursor.execute("SELECT * FROM notas WHERE Id = %s", (id,))
    nota = cursor.fetchone()

    if not nota:
        cursor.close()
        return jsonify({"error": "Nota no encontrada"}), 404

    # Si la nota existe, elimínala
    cursor.execute("DELETE FROM notas WHERE Id = %s", (id,))
    conexion.commit()
    cursor.close()

    return jsonify({"mensaje": f"Nota con ID {id} eliminada correctamente"}), 200

# Ruta para mostrar todos los usuarios
@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    conexion = mysql.connection
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuario")  # Asegúrate de que la tabla se llama "usuario"
    usuarios = cursor.fetchall()
    cursor.close()

    return jsonify(usuarios)  # Retorna los usuarios en formato JSON

    # Ruta para agregar un nuevo usuario
# Ruta para agregar un nuevo usuario
@app.route("/agregar_usuario", methods=["POST"])
def agregar_usuario():
    # Verificar si la solicitud contiene JSON
    if not request.is_json:
        return jsonify({"error": "La solicitud debe ser en formato JSON"}), 400

    try:
        # Obtener datos del JSON
        data = request.get_json()
        username = data.get("username")
        contraseña = data.get("contraseña")

        if not username or not contraseña:
            return jsonify({"error": "Los campos 'username' y 'contraseña' son requeridos"}), 400

        # Conectar a MySQL e insertar los datos
        conexion = mysql.connection
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuario (username, contraseña) VALUES (%s, %s)", (username, contraseña))
        conexion.commit()
        cursor.close()

        return jsonify({"mensaje": "Usuario agregado con éxito"}), 201

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)


