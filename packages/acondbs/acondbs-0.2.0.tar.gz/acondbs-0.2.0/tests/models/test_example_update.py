from acondbs.db.sa import sa
from acondbs.models import Map

# __________________________________________________________________||
def test_simple(app):
    '''A simple test of updating an object
    '''

    with app.app_context():
        map1 = Map.query.filter_by(map_id=1012).first()
        assert 'lat20200120' == map1.name
        map1.name = 'new-map-name'
        sa.session.commit()

    with app.app_context():
        map1 = Map.query.filter_by(map_id=1012).first()
        assert 'new-map-name' == map1.name

# __________________________________________________________________||
