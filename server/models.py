from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

from sqlalchemy import MetaData
...
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata, engine_options={"echo": True})



class Producer(db.Model, SerializerMixin):
    __tablename__ = "producers"

    id = db.Column(db.Integer, primary_key=True)
    #adding columns
    founding_year = (db.Integer)
    name = (db.String)
    region = (db.String)
    operation_size = (db.String)
    image = (db.String)

    # Add the relationship
    cheeses = db.relationship('Cheese', back_populates='producer')

    def __repr__(self):
        return f"<Producer {self.id}>"


class Cheese(db.Model, SerializerMixin):
    __tablename__ = "cheeses"

    id = db.Column(db.Integer, primary_key=True)
    #adding columns
    producer_id = (db.Integer, db.ForeignKey('producers.id'))
    kind = (db.String)
    is_raw_milk = (db.Boolean)
    production_date = (db.DateTime)
    image = (db.String)
    price = (db.Float)

    # Add the relationship
    producer = db.relationship('Producer', back_populates='cheeses')


    def __repr__(self):
        return f"<Cheese {self.id}>"
