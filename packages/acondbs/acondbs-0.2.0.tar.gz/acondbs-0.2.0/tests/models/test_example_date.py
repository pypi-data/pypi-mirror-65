import datetime
import sqlalchemy
import pytest

from acondbs.db.sa import sa
from acondbs.models import Map

# __________________________________________________________________||
def test_type(app):
    '''confirm the type of the date field
    '''

    with app.app_context():
        map = Map.query.filter_by(name='lat20200120').first()

        # The type of the field "date_posted" of Map is "datetime.date"
        assert isinstance(map.date_posted, datetime.date)

# __________________________________________________________________||
def test_add(app):
    '''A simple test of adding an object with a date field
    '''

    # date_posted needs to be initialized with a datetime.date
    date_posted = datetime.date(2019, 2, 23)
    map1 = Map(name="map1", date_posted=date_posted)

    with app.app_context():
        sa.session.add(map1)
        sa.session.commit()

    with app.app_context():
        map1 = Map.query.filter_by(name='map1').first()
        assert datetime.date(2019, 2, 23) == map1.date_posted

# __________________________________________________________________||
def test_add_raise(app):
    '''A simple test of adding an object with a wrong type
    '''

    # It is not impossible to instnaiate a date field with a wrong
    # type, e.g, str
    map1 = Map(name="map1", date_posted="2019-02-13")

    with app.app_context():

        # It is also possible to add
        sa.session.add(map1)

        # However, it is not possible to commit
        with pytest.raises(sqlalchemy.exc.StatementError):
            sa.session.commit()

# __________________________________________________________________||
