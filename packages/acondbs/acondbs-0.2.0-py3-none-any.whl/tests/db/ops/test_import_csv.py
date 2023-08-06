import os
import pytest

from acondbs import create_app
from acondbs.db.ops import define_tables, import_tables_from_csv_files, export_db_to_dict_of_dict_list

from ...constants import SAMPLE_DIR

##__________________________________________________________________||
@pytest.fixture
def app():
    database_uri ="sqlite:///:memory:"
    app = create_app(SQLALCHEMY_DATABASE_URI=database_uri)
    with app.app_context():
        define_tables()
    yield app


##__________________________________________________________________||
def test_import_tables_from_csv_files(app, snapshot):
    csvdir = os.path.join(SAMPLE_DIR, 'csv')
    with app.app_context():
        import_tables_from_csv_files(csvdir)
    with app.app_context():
        snapshot.assert_match(export_db_to_dict_of_dict_list())

##__________________________________________________________________||
