from acondbs.db.sa import sa
from acondbs.models import Map, Beam

# These tests are written primarily for the developer to understand
# how models in flask_sqlalchemy work.

# __________________________________________________________________||
def test_simple(app):
    '''A simple test of deleting an object
    '''

    with app.app_context():

        # save the initial number of the maps to compare later
        nmaps = len(Map.query.all())

    with app.app_context():
        map1 = Map.query.filter_by(map_id=1012).first()
        sa.session.delete(map1)
        sa.session.commit()

    with app.app_context():

        # test the number of the maps is decreased by one
        assert (nmaps - 1) == len(Map.query.all())

        # the map is no longer found
        map1 = Map.query.filter_by(map_id=1012).first()
        assert map1 is None

# __________________________________________________________________||
