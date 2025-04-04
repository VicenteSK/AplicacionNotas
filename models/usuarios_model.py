# models/usuarios_model.py
from flask_mysqldb import MySQL

class UsuariosModel:
    def __init__(self, mysql):
        self.mysql = mysql

    def obtener_usuarios(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario")
        usuarios = cursor.fetchall()
        cursor.close()
        return usuarios

    def obtener_usuario_por_id(self, id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE id = %s", (id,))
        usuario = cursor.fetchone()
        cursor.close()
        return usuario

    def agregar_usuario(self, username, contraseña):
        cursor = self.mysql.connection.cursor()
        cursor.execute("INSERT INTO usuario (username, contraseña) VALUES (%s, %s)", (username, contraseña))
        self.mysql.connection.commit()
        cursor.close()

    def actualizar_usuario(self, id, username, contraseña):
        cursor = self.mysql.connection.cursor()
        cursor.execute("UPDATE usuario SET username = %s, contraseña = %s WHERE id = %s", (username, contraseña, id))
        self.mysql.connection.commit()
        cursor.close()

    def eliminar_usuario(self, id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("DELETE FROM usuario WHERE id = %s", (id,))
        self.mysql.connection.commit()
        cursor.close()