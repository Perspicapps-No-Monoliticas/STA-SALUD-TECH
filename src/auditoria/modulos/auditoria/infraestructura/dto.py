from config.db import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey

import uuid

Base = db.declarative_base()

class Regulacion(db.Model):
    __tablename__ = "regulaciones"
    id = db.Column(db.String(40), primary_key=True)
    nombre = db.Column(db.String(500), nullable=False)
    region = db.Column(db.String(500), nullable=False)
    payload = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)

class EventosRegulacion(db.Model):
    __tablename__ = "eventos_regulacion"
    id = db.Column(db.String(40), primary_key=True)
    id_entidad = db.Column(db.String(40), nullable=False)
    fecha_evento = db.Column(db.DateTime, nullable=False)
    payload = db.Column(db.Text, nullable=False)
    tipo_evento = db.Column(db.String(100), nullable=False)
    formato_contenido = db.Column(db.String(10), nullable=False)
    nombre_servicio = db.Column(db.String(40), nullable=False)
    contenido = db.Column(db.Text, nullable=False)