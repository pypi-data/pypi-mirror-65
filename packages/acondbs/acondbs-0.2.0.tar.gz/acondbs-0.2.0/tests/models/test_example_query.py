import pytest

from flask_sqlalchemy import BaseQuery

from acondbs.models import Map, Beam

# These tests are written primarily for the developer to understand
# how models in flask_sqlalchemy work.

# __________________________________________________________________||
def test_context(app):

    # query cannot be accessed outside of the app context
    with pytest.raises(RuntimeError):
        Map.query

    with app.app_context():
        Map.query

def test_query_all(app):

    with app.app_context():

        # query is an instance of BaseQuery
        query = Map.query
        assert isinstance(query, BaseQuery)

        # query.all() returns a list of maps
        results = query.all()
        # e.g., [<Map 1001>, <Map 1012>, <Map 1013>]

        assert ['lat20190213', 'lat20200120', 'lat20200201'] == [
            e.name for e in results]

        assert isinstance(results[0], Map)

def test_query_filter(app):

    with app.app_context():

        # filter_by() returns an instance of BaseQuery
        query = Map.query.filter_by(name='lat20200120')
        assert isinstance(query, BaseQuery)

        # the results are a list with one element
        results = query.all()
        assert 1 == len(results)
        assert ['lat20200120'] == [e.name for e in results]

        # first() returns a map
        map = query.first()
        assert isinstance(map, Map)
        assert 'lat20200120' == map.name

        # the back-referenced beam can be accessed as an attribute of
        # the map
        assert ['20200123'] == [e.name for e in map.beams]
        beam = map.beams[0]
        assert isinstance(beam, Beam)

        # the beam, of course, references to the map
        assert map is beam.map

def test_query_filter_nonexistent(app):

    with app.app_context():

        query = Map.query.filter_by(name='no-such-map')
        assert isinstance(query, BaseQuery)

        # the results are an empty list
        results = query.all()
        assert [] == results

        # first() returns None
        map = query.first()
        assert map is None

# __________________________________________________________________||
