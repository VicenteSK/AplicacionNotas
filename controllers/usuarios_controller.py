from flask import request, jsonify
from models.usuarios_model import UsuarioModel
from views.usuarios_view import (
    mostrar_usuarios,
    usuario_agregado,
    usuario_no_encontrado,
    respuesta_json,
)

class UsuarioController:
    def __init__(self, mysql):
        self.modelo = UsuarioModel(mysql)

    def listar_usuarios(self):
        try:
            usuarios = self.modelo.obtener_usuarios()
            print("Usuarios obtenidos:", usuarios)
            if not usuarios:
                return respuesta_json({"error": "No se encontraron usuarios"}, 404)
            return mostrar_usuarios(usuarios)
        except Exception as e:
            print("Error al obtener usuarios:", e)
            return respuesta_json({"error": f"Error al obtener usuarios: {str(e)}"}, 500)

    def obtener_usuario(self, id):
        try:
            usuario = self.modelo.obtener_usuario_por_id(id)
            if usuario:
                return jsonify(usuario), 200
            return jsonify({"error": "No se encontró el usuario"}), 404
        except Exception as e:
            print("Error en obtener_usuario:", e)
            return respuesta_json({"error": f"Error al obtener usuario: {str(e)}"}, 500)

    def agregar_usuario(self):
        if not request.is_json:
            return respuesta_json({"error": "La solicitud debe ser JSON"}, 400)
        try:
            data = request.get_json(force=True)
            if "username" not in data or "contraseña" not in data:
                return respuesta_json({"error": "Faltan campos 'username' o 'contraseña'"}, 400)

            self.modelo.agregar_usuario(data["username"], data["contraseña"])
            return usuario_agregado()
        except Exception as e:
            print("Error en agregar_usuario:", e)
            return respuesta_json({"error": f"Error al agregar usuario: {str(e)}"}, 500)

    def eliminar_usuario(self, id):
        try:
            usuario = self.modelo.obtener_usuario_por_id(id)
            if not usuario:
                return usuario_no_encontrado()
            self.modelo.eliminar_usuario(id)
            return respuesta_json({"mensaje": f"Usuario con ID {id} eliminado correctamente"})
        except Exception as e:
            print("Error en eliminar_usuario:", e)
            return respuesta_json({"error": f"Error al eliminar usuario: {str(e)}"}, 500)

    def actualizar_usuario(self, id):
        if not request.is_json:
            return respuesta_json({"error": "La solicitud debe tener Content-Type 'application/json'"}, 400)
        try:
            data = request.get_json(force=True)
            if not data or "username" not in data or "contraseña" not in data:
                return respuesta_json({"error": "Faltan datos: 'username' y 'contraseña' son requeridos"}, 400)

            self.modelo.actualizar_usuario(id, data["username"], data["contraseña"])
            return respuesta_json({"mensaje": "Usuario actualizado correctamente"}, 200)
        except Exception as e:
            print("Error en actualizar_usuario:", e)
            return respuesta_json({"error": f"Error al actualizar usuario: {str(e)}"}, 500)
