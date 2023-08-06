from acondbs.db.sa import sa
from acondbs.models import Map, Beam

# These tests are written primarily for the developer to understand
# how models in flask_sqlalchemy work.

# __________________________________________________________________||
def test_simple(app):
    '''A simple test of adding an object
    '''

    with app.app_context():

        # save the initial number of the maps to compare later
        nmaps = len(Map.query.all())

    # this instantiation doesn't need be within a app context
    map1 = Map(name="map1")

    with app.app_context():
        sa.session.add(map1)
        sa.session.commit()

    with app.app_context():

        # test the number of the maps is increased by one
        assert (nmaps + 1) == len(Map.query.all())

        # the new map can be retrieved in a different app context
        map1_ = Map.query.filter_by(name='map1').first()
        assert isinstance(map1_, Map)

# __________________________________________________________________||
def test_python_object(app):
    '''A simple test about Python object
    '''

    map1 = Map(name="map1")

    with app.app_context():
        sa.session.add(map1)
        sa.session.commit()

        map1_ = Map.query.filter_by(name='map1').first()

        # the query returns the same Python object
        assert map1 is map1_

    with app.app_context():
        map1_ = Map.query.filter_by(name='map1').first()

        # In a different app context, no longer the same Python object
        assert map1 is not map1_

# __________________________________________________________________||
def test_primary_key(app):
    '''A simple test about the primary key
    '''

    map1 = Map(name="map1")

    # The primary key (map_id) is None at this point
    assert map1.map_id is None

    with app.app_context():
        sa.session.add(map1)
        sa.session.commit()

        # After the commit, map_id is automatically assigned
        map_id = map1.map_id
        assert map_id is not None

    with app.app_context():

        # The object can be retrived by the map_id in another context
        map1 = Map.query.filter_by(map_id=map_id).first()
        assert 'map1' == map1.name

# __________________________________________________________________||
def test_relation(app):
    '''A simple test of adding an object with relation
    '''

    map1 = Map(name="map1")
    beam1 = Beam(name="beam1", map=map1)

    # The relation has been already established
    assert map1 is beam1.map
    assert [beam1] == map1.beams

    # The primary and foreign keys are still None
    assert map1.map_id is None
    assert beam1.beam_id is None
    assert beam1.input_map_id is None

    with app.app_context():
        sa.session.add(map1)
        sa.session.commit()

        # The primary keys are assigned
        assert map1.map_id is not None
        assert beam1.beam_id is not None

        # The foreign key is correctly set
        assert map1.map_id == beam1.input_map_id

    with app.app_context():
        map1 = Map.query.filter_by(name='map1').first()
        beam1 = Beam.query.filter_by(name='beam1').first()

        # The relation is preserved in a different app context
        assert map1 is beam1.map
        assert beam1 is map1.beams[0]
        assert map1.map_id == beam1.input_map_id

# __________________________________________________________________||
