from sqlalchemy import MetaData

import pytest

from acondbs.db.ops import export_db_to_dict_of_dict_list
from acondbs.db.sa import sa

##__________________________________________________________________||
def test_export_db_to_dict_of_dict_list(app, snapshot):
    """test export_db_to_dict_of_dict_list()

    """

    with app.app_context():
        snapshot.assert_match(export_db_to_dict_of_dict_list())

##__________________________________________________________________||
