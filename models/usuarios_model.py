from flask import request, jsonify

from views.usuarios_view import (
    mostrar_usuarios,
    usuario_agregado,
    usuario_no_encontrado,
    respuesta_json,
)

class UsuarioModel:
    def __init__(self, mysql):
        self.mysql = mysql

    def obtener_usuarios(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario")
        usuarios = cursor.fetchall()
        cursor.close()
        return usuarios


    def agregar_usuario(self, username, contraseña):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO usuario (username, contraseña) VALUES (%s, %s)",
            (username, contraseña)
        )
        self.mysql.connection.commit()
        cursor.close()

    def obtener_usuario_por_id(self, id):
        try:
            cursor = self.mysql.connection.cursor()
            cursor.execute("SELECT * FROM usuario WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            cursor.close()
            return resultado
        except Exception as e:
            raise Exception(str(e))

    def eliminar_usuario(self, id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("DELETE FROM usuario WHERE id = %s", (id,))
        self.mysql.connection.commit()
        cursor.close()

    def actualizar_usuario(self, id, username, contraseña):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            "UPDATE usuario SET username = %s, contraseña = %s WHERE id = %s",
            (username, contraseña, id)
        )
        self.mysql.connection.commit()
        cursor.close()
