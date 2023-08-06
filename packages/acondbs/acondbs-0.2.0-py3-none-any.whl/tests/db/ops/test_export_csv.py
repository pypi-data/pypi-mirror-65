import os
import pytest

from acondbs import create_app
from acondbs.db.ops import define_tables, import_tables_from_csv_files
from acondbs.db.ops import export_db_to_dict_of_dict_list
from acondbs.db.ops import export_db_to_csv_files

from ...constants import SAMPLE_DIR

##__________________________________________________________________||
@pytest.fixture
def app():
    database_uri ="sqlite:///:memory:"
    csvdir = os.path.join(SAMPLE_DIR, 'csv')
    app = create_app(SQLALCHEMY_DATABASE_URI=database_uri)
    with app.app_context():
        define_tables()
        import_tables_from_csv_files(csvdir)
    yield app

##__________________________________________________________________||
def test_export_db_to_csv_files(app, tmpdir_factory, snapshot):
    outdir = str(tmpdir_factory.mktemp('csv'))

    with app.app_context():
        export_db_to_csv_files(outdir)

    with app.app_context():
        define_tables()
        import_tables_from_csv_files(outdir)
        snapshot.assert_match(export_db_to_dict_of_dict_list())

##__________________________________________________________________||
