# Archivo: app/models/clase_model.py

from app.extensions import db

class Clase(db.Model):
    __tablename__ = 'clases'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)

    # Relación con Grado (una clase pertenece a un grado)
    grado_id = db.Column(db.Integer, db.ForeignKey('grados.id'), nullable=False)

    # Relación con User (una clase tiene un maestro)
    maestro_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    maestro = db.relationship('User', backref='clases')
    
    # Campos para el horario de la clase
    horario_inicio = db.Column(db.Time, nullable=False)
    horario_fin = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f'<Clase {self.nombre} - Grado: {self.grado.nombre} - Maestro: {self.maestro.username}>'