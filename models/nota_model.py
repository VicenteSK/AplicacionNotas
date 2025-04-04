# models/nota_model.py
from flask_mysqldb import MySQL

class NotaModel:
    def __init__(self, mysql):
        self.mysql = mysql

    def obtener_notas(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM notas")
        resultado = cur.fetchall()
        cur.close()
        return resultado

    def obtener_nota_por_id(self, id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM notas WHERE Id = %s", (id,))
        nota = cursor.fetchone()
        cursor.close()
        return nota

    def agregar_nota(self, titulo, texto, id_usuario):
        cursor = self.mysql.connection.cursor()
        cursor.execute("INSERT INTO notas (titulo, texto, id_usuario) VALUES (%s, %s, %s)", (titulo, texto, id_usuario))
        self.mysql.connection.commit()
        cursor.close()

    def eliminar_nota(self, id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("DELETE FROM notas WHERE Id = %s", (id,))
        self.mysql.connection.commit()
        cursor.close()

    def obtener_notas_usuario(self):
        cursor = self.mysql.connection.cursor()
        query = """
            SELECT notas.id, usuario.username, notas.titulo, notas.texto
            FROM notas
            INNER JOIN usuario ON notas.id_usuario = usuario.id
        """
        cursor.execute(query)
        notas = cursor.fetchall()
        cursor.close()
        return notas

    def obtener_notas_por_usuario(self, id):
        cursor = self.mysql.connection.cursor()
        query = """
            SELECT notas.id, usuario.username, notas.titulo, notas.texto
            FROM notas
            INNER JOIN usuario ON notas.id_usuario = usuario.id
            WHERE usuario.id = %s
        """
        cursor.execute(query, (id,))
        notas = cursor.fetchall()
        cursor.close()
        return notas

    def actualizar_nota(self, id,  titulo, texto, id_usuario):
        cursor = self.mysql.connection.cursor()
        cursor.execute("""
            UPDATE notas 
            SET titulo = %s, texto = %s, id_usuario = %s 
            WHERE id = %s
        """, (titulo, texto, id_usuario, id))
        self.mysql.connection.commit()
        cursor.close()