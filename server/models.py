from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

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
    founding_year = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable = False)
    region = db.Column(db.String)
    operation_size = db.Column(db.String, nullable = False)
    image = db.Column(db.String)

    #validations for producers
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name must be provided")
        return name
    
    @validates('founding_year')
    def validate_founding_year(self, key, year):
        current_year = datetime.now().year
        if not 1900 <= year <= current_year:
            raise ValueError(f"Founding year must be between 1900 and {current_year}")
        return year
    
    @validates('operation_size')
    def validate_operation_size(self, key, size):
        valid_sizes = ["small", "medium", "large", "family", "corporate"]
        if size.lower() not in valid_sizes:
            raise ValueError(f"Operation size must be one of: {', '.join(valid_sizes)}")
        return size.lower()


    # adding the relationship
    cheeses = db.relationship('Cheese', back_populates='producer')

    def __repr__(self):
        return f"<Producer {self.id}>"


class Cheese(db.Model, SerializerMixin):
    __tablename__ = "cheeses"

    id = db.Column(db.Integer, primary_key=True)
    #adding columns
    #cheese gets foreign key because it's on the many side
    producer_id = db.Column(db.Integer, db.ForeignKey('producers.id'))
    kind = db.Column(db.String)
    is_raw_milk = db.Column(db.Boolean)
    production_date = db.Column(db.DateTime, nullable=False)
    image = db.Column(db.String)
    price = db.Column(db.Float, nullable=False)

    #add cheese validations
    @validates
    def validate_production_date(self, key, production_date):
        if not production_date <= datetime.now():
            raise ValueError(f"Production date must be before {datetime.now()}.")
        return production_date

    @validates
    def validate_price(self, key, price):
        if not 1.00 <= price <= 45.00:
            raise ValueError(f"Price must be between 1.00 and 45.00.")
        return price

    # add the relationship
    producer = db.relationship('Producer', back_populates='cheeses')


    def __repr__(self):
        return f"<Cheese {self.id}>"
    

    #1. add models and relationships
    #2. add validations
    #3. $ flask db migrate -m'your message'
        #$ flask db upgrade
        #$ python seed.py
