from flask import Flask
from flask_mysqldb import MySQL
from controllers.nota_controller import NotaController

app = Flask(__name__)

# Configuración de MySQL
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "BdAplicacionNotas"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# Inicializar MySQL
mysql = MySQL(app)

# Crear una instancia del controlador
nota_controller = NotaController(mysql)

# Rutas normales conectadas al controlador
@app.route('/notas', methods=['GET'])
def mostrar_notas():
    return nota_controller.listar_notas()

@app.route('/nota/<int:id>', methods=['GET'])
def obtener_nota(id):
    return nota_controller.obtener_nota(id)

@app.route('/agregar_nota', methods=['POST'])
def agregar_nota():
    return nota_controller.agregar_nota()

@app.route('/crear_nota', methods=['POST'])
def crear_nota():
    return nota_controller.crear_nota()

@app.route('/notas_json', methods=['GET'])
def obtener_todas_las_notas():
    return nota_controller.obtener_todas_las_notas()

@app.route('/eliminar_nota/<int:id>', methods=['DELETE'])
def eliminar_nota(id):
    return nota_controller.eliminar_nota(id)

@app.route('/notas_usuario', methods=['GET'])
def obtener_notas_usuario():
    return nota_controller.obtener_notas_usuario()

@app.route('/notas_usuario/<int:id>', methods=['GET'])
def obtener_notas_usuario_por_id(id):
    return nota_controller.obtener_notas_usuario_por_id(id)

# Ruta para actualizar una nota
@app.route('/actualizar_nota/<int:id>', methods=['PUT'])
def actualizar_nota(id):
    return nota_controller.actualizar_nota(id)

if __name__ == "__main__":
    app.run(debug=True)