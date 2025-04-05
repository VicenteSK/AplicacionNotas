from flask import jsonify

def mostrar_usuarios(usuarios):
    return jsonify(usuarios)

def mostrar_usuario(usuario):
    return jsonify(usuario)

def usuario_agregado():
    return jsonify({"mensaje": "Usuario agregado correctamente"}), 201

def usuario_no_encontrado():
    return jsonify({"error": "Usuario no encontrado"}), 404

def respuesta_json(data, status=200):
    return jsonify(data), status
