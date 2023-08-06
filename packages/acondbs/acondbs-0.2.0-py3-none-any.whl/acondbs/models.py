"""declare ORM models

In this module, ORM (Object-relational mapping) models are declared.
One model is mapped to one table in the DB. Models are declared as
Python classes inheriting the Model class in Flask-SQLAlchemy.

"Declaring Models" in Flask-SQLAlchemy doc:
https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

"Declare a Mapping" in SQLAlchemy doc:
https://docs.sqlalchhttps://docs.sqlalchemy.org/en/13/orm/tutorial.html#declare-a-mapping

"""

from .db.sa import sa

##__________________________________________________________________||
class Simulation(sa.Model):
    __tablename__ = 'simulations'
    simulation_id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.Text(), nullable=False, unique=True, index=True)
    date_posted = sa.Column(sa.Date())
    mapper = sa.Column(sa.Text())
    note = sa.Column(sa.Text())

class SimulationFilePath(sa.Model):
    __tablename__ = 'simulation_path'
    simulation_file_path_id = sa.Column(sa.Integer(), primary_key=True)
    simulation_id = sa.Column(sa.ForeignKey('simulations.simulation_id'))
    path = sa.Column(sa.Text())
    note = sa.Column(sa.Text())
    simulation = sa.relationship("Simulation", backref=sa.backref("simulation_file_paths"))

class Map(sa.Model):
    __tablename__ = 'maps'
    map_id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.Text(), nullable=False, unique=True, index=True)
    date_posted = sa.Column(sa.Date())
    mapper = sa.Column(sa.Text())
    note = sa.Column(sa.Text())

class Beam(sa.Model):
    __tablename__ = 'beams'
    beam_id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.Text(), nullable=False, unique=True, index=True)
    path = sa.Column(sa.Text())
    input_map_id = sa.Column(sa.ForeignKey('maps.map_id'))
    input_beam_id = sa.Column(sa.ForeignKey('beams.beam_id'))
    map = sa.relationship("Map", backref=sa.backref("beams"))
    parent_beam = sa.relationship(lambda: Beam, remote_side=beam_id, backref=sa.backref("child_beams"))

class MapFilePath(sa.Model):
    __tablename__ = 'map_path'
    map_file_path_id = sa.Column(sa.Integer(), primary_key=True)
    map_id = sa.Column(sa.ForeignKey('maps.map_id'))
    path = sa.Column(sa.Text())
    note = sa.Column(sa.Text())
    map = sa.relationship("Map", backref=sa.backref("map_file_paths"))

##__________________________________________________________________||
