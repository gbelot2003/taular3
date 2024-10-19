# Archivo: app/models/grado_model.py

from app.extensions import db

class Grado(db.Model):
    __tablename__ = 'grados'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)  # Nombre del grado
    descripcion = db.Column(db.String(255), nullable=True)  # Descripción opcional del grado

    # Relación uno-a-muchos con la tabla de clases
    clases = db.relationship('Clase', backref='grado', lazy=True)

    def __repr__(self):
        return f'<Grado {self.nombre}>'