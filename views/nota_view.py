from flask import render_template, jsonify

def mostrar_notas(notas):
    return render_template("index.html", notas=notas)

def mostrar_nota(nota):
    return f"<h1>{nota['titulo']}</h1><p>{nota['texto']}</p><a href='/notas'>Volver</a>"

def nota_agregada():
    return "Nota agregada con éxito"

def nota_no_encontrada():
    return "Registro no encontrado", 404

def respuesta_json(data, status_code=200):
    return jsonify(data), status_code
