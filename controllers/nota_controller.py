from flask import request
from models.nota_model import NotaModel
from views.nota_view import (
    mostrar_notas,
    mostrar_nota,
    nota_agregada,
    nota_no_encontrada,
    respuesta_json,
)

class NotaController:
    def __init__(self, mysql):
        self.modelo = NotaModel(mysql)

    def listar_notas(self):
        try:
            notas = self.modelo.obtener_notas()
            return mostrar_notas(notas)
        except Exception as e:
            return respuesta_json({"error": f"Error al obtener notas: {str(e)}"}, 500)

    def obtener_nota(self, id):
        try:
            nota = self.modelo.obtener_nota_por_id(id)
            if nota:
                return mostrar_nota(nota)
            else:
                return nota_no_encontrada()
        except Exception as e:
            return respuesta_json({"error": f"Error al obtener la nota: {str(e)}"}, 500)

    def agregar_nota(self):
        try:
            titulo = request.form.get("titulo")
            texto = request.form.get("texto")
            id_usuario = request.form.get("id_usuario")
            if not titulo:
                return "Error: El campo 'titulo' es requerido", 400
            self.modelo.agregar_nota(titulo, texto, id_usuario)  # Si el modelo no usa id_usuario, no es necesario agregarlo aquí
            return nota_agregada()
        except Exception as e:
            return respuesta_json({"error": f"Error al agregar nota: {str(e)}"}, 500)

    def crear_nota(self):
        if not request.is_json:
            return respuesta_json({"error": "La solicitud debe tener Content-Type 'application/json'"}, 400)
        try:
            data = request.get_json(force=True)
            if not data or "titulo" not in data or "texto" not in data or "id_usuario" not in data:
                return respuesta_json({"error": "Faltan datos: 'titulo', 'texto' y 'id_usuario' son requeridos"}, 400)

            titulo = data["titulo"]
            texto = data["texto"]
            id_usuario = data["id_usuario"]  # Aquí corregimos para obtener el id_usuario correctamente

            # Llamamos al modelo para agregar la nota con el id_usuario
            self.modelo.agregar_nota(titulo, texto, id_usuario)
            return respuesta_json({"mensaje": "Nota creada exitosamente"}, 201)
        except Exception as e:
            return respuesta_json({"error": f"Error al crear nota: {str(e)}"}, 500)


    def obtener_todas_las_notas(self):
        try:
            notas = self.modelo.obtener_notas()
            return respuesta_json(notas)
        except Exception as e:
            return respuesta_json({"error": f"Error al obtener notas: {str(e)}"}, 500)

    def eliminar_nota(self, id):
        try:
            nota = self.modelo.obtener_nota_por_id(id)
            if not nota:
                return respuesta_json({"error": "Nota no encontrada"}, 404)
            self.modelo.eliminar_nota(id)
            return respuesta_json({"mensaje": f"Nota con ID {id} eliminada correctamente"})
        except Exception as e:
            return respuesta_json({"error": f"Error al eliminar nota: {str(e)}"}, 500)

    def obtener_notas_usuario(self):
        try:
            notas = self.modelo.obtener_notas_usuario()
            return respuesta_json(notas)
        except Exception as e:
            return respuesta_json({"error": f"Error al obtener notas del usuario: {str(e)}"}, 500)

    def obtener_notas_usuario_por_id(self, id):
        try:
            notas = self.modelo.obtener_notas_por_usuario(id)
            if notas:
                return respuesta_json(notas)
            else:
                return respuesta_json({"error": "No se encontraron notas para este usuario"}, 404)
        except Exception as e:
            return respuesta_json({"error": f"Error al obtener notas del usuario: {str(e)}"}, 500)


    def actualizar_nota(self, id):
        if not request.is_json:
            return respuesta_json({"error": "La solicitud debe tener Content-Type 'application/json'"}, 400)
        try:
            data = request.get_json(force=True)
            if not data or "titulo" not in data or "texto" not in data or "id_usuario" not in data:
                return respuesta_json({"error": "Faltan datos: 'titulo', 'texto' y 'id_usuario' son requeridos"}, 400)

            titulo = data["titulo"]
            texto = data["texto"]
            id_usuario = data["id_usuario"]

            # Llamamos al método del modelo para actualizar la nota
            self.modelo.actualizar_nota(id, titulo, texto, id_usuario)
            return respuesta_json({"mensaje": "Nota actualizada exitosamente"}, 200)
        except Exception as e:
            return respuesta_json({"error": f"Error al actualizar nota: {str(e)}"}, 500)