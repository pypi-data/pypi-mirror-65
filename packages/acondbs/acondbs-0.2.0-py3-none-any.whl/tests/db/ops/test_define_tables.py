from sqlalchemy import MetaData

import pytest

from acondbs import create_app
from acondbs.db.ops import define_tables
from acondbs.db.sa import sa

##__________________________________________________________________||
@pytest.fixture
def app_with_empty_db():
    database_uri ="sqlite:///:memory:"
    app = create_app(SQLALCHEMY_DATABASE_URI=database_uri)
    yield app

##__________________________________________________________________||
def test_define_tables_start_with_empty_db(app_with_empty_db):
    """test define_tables()

    This function tests if tables will be defined starting from new db without
    any tables.

    """

    app = app_with_empty_db

    # confirm tables are not defined initially
    with app.app_context():
        metadata = MetaData()
        metadata.reflect(bind=sa.engine)
        assert not metadata.tables

    with app.app_context():
        define_tables()

    with app.app_context():
        metadata = MetaData()
        metadata.reflect(bind=sa.engine)
        tbl_names = {'beams', 'maps', 'map_path', 'simulations', 'simulation_path'}
        assert tbl_names == metadata.tables.keys()

##__________________________________________________________________||
def test_define_tables_start_with_nonempty_db(app):
    """test define_tables()

    This function tests if tables will be redefined starting from db
    with tables with entries.

    """

    # confirm tables are defined initially and not empty
    with app.app_context():
        metadata = MetaData()
        metadata.reflect(bind=sa.engine)
        assert metadata.tables
        total_nentries = sum([len([r for r in
                               sa.engine.execute(tbl.select())]) for tbl in
                          metadata.sorted_tables])
        assert total_nentries > 0

    with app.app_context():
        define_tables()

    # confirm tables are defined and all empty
    with app.app_context():
        metadata = MetaData()
        metadata.reflect(bind=sa.engine)
        tbl_names = {'beams', 'maps', 'map_path', 'simulations', 'simulation_path'}
        assert tbl_names == metadata.tables.keys()
        total_nentries = sum([len([r for r in
                               sa.engine.execute(tbl.select())]) for tbl in
                          metadata.sorted_tables])
        assert total_nentries == 0

##__________________________________________________________________||
