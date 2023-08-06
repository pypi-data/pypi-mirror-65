"""DB operations

The functions in this module need to be called within the application
context of Flask unless stated otherwise.

"""
import os
import datetime
import csv
import pathlib

from sqlalchemy import MetaData
import sqlalchemy

from .sa import sa
from .conn import get_db_connection

##__________________________________________________________________||
def define_tables():
    """defines tables in the DB

    This function defines tables in the DB after dropping all existing
    tables.

    """

    engine = sa.engine
    metadata = MetaData()
    metadata.reflect(bind=engine)

    if metadata.tables:
        tbl_names = metadata.tables.keys()
        # ['maps', 'beams']

        tbl_names = ', '.join(['"{}"'.format(t) for t in tbl_names])
        # '"beams", "maps"'

        msg = "Dropped all tables: {}".format(tbl_names)

        metadata.drop_all(bind=engine)
        print(msg)

    if not sa.Model.metadata.tables:
        msg = "No tables to be created are found!"
        print(msg)
        return

    tbl_names = sa.Model.metadata.tables.keys()
    # ['maps', 'beams']

    tbl_names = ', '.join(['"{}"'.format(t) for t in tbl_names])
    # '"beams", "maps"'

    msg = "Created tables: {}".format(tbl_names)

    sa.Model.metadata.create_all(engine)

    print(msg)

##__________________________________________________________________||
def get_all_table_names():
    """returns the names of all tables in the DB.

    Returns
    -------
    list of str
        the names of all tables in the DB

    """
    engine = sa.engine
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return [tbl.name for tbl in metadata.sorted_tables]

def export_db_to_dict_of_dict_list():
    """exports the DB to a dict of table names and lists of dicts for each row

    Returns
    -------
    dict
        dict with one entry for each table: the table name as the key
        and the value lists of dicts: one dict for each row: field
        names as the keys and contents as the values. e.g.,

            {"tblA": [
                {'fieldA': 1001, 'fieldB': 'abc'},
                {'fieldA': 1002, 'fieldB': 'xyz'}
            ]}

    """
    tbl_names = get_all_table_names()
    ret = {n: export_table_to_dict_list(n) for n in tbl_names}
    return ret

def export_table_to_dict_list(tbl_name):
    """exports the table to a list of dicts

    Parameters
    ----------
    tbl_name : str
        the table name

    Returns
    -------
    list of dict
        the list of dicts: one dict for each row: field names as the
        keys and contents as the values. e.g.:

            [
                {'fieldA': 1001, 'fieldB': 'abc'},
                {'fieldA': 1002, 'fieldB': 'xyz'}
            ]

    """
    result_proxy = get_resultproxy_of_select_all_rows(tbl_name)
    return [dict(r) for r in result_proxy]

def get_resultproxy_of_select_all_rows(tbl_name):
    """returns ResultProxy with all rows of the table

    Parameters
    ----------
    tbl_name : str
        the table name

    Returns
    -------
    ResultProxy
        ResultProxy of SQLAlchemy with the result of query selecting
        all rows of the table.
        https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.ResultProxy

    """
    engine = sa.engine
    metadata = MetaData()
    metadata.reflect(bind=engine)
    tbl = metadata.tables[tbl_name]
    return engine.execute(tbl.select())

##__________________________________________________________________||
def import_tables_from_csv_files(csvdir):
    """imports tables from CSV files into the DB

    The tables need to be already defined in the DB.

    The folder `csvdir` should contain CSV files with the table
    contents to be imported: one CSV file for one table with the file
    name <<table name>>.csv

    Parameters
    ----------
    csvdir : str
        a path to a folder with CSV files

    """
    tbl_names = get_all_table_names()
    for tbl_name in tbl_names:
        csv_filename = '{}.csv'.format(tbl_name)
        csv_path = os.path.join(csvdir, csv_filename)
        if os.path.exists(csv_path):
            import_table_from_csv_file(tbl_name, csv_path)
            message = 'imported to "{}" from {}'.format(tbl_name, csv_path)
        else:
            message = 'skipped "{}". file not found: {}'.format(tbl_name, csv_path)
        print(message)

def import_table_from_csv_file(tbl_name, path):
    """import a table from a CSV file

    The table needs to be already defined in the DB.

    Parameters
    ----------
    tbl_name : str
        the name of the table
    path : str
        the path to the CSV file

    """
    engine = sa.engine
    metadata = MetaData()
    metadata.reflect(bind=engine)
    tbl = metadata.tables[tbl_name]

    with open(path, 'r') as f:
        rows = list(csv.reader(f))
    fields = rows[0]
    rows = rows[1:]
    data = [{f: convert_data_type_for_insert(e, tbl.columns[f].type)
             for f, e in zip(fields, r)} for r in rows]
    ins = tbl.insert()
    connection = get_db_connection()
    connection.execute(ins, data)

def convert_data_type_for_insert(str_, type_):
    """converts data type for insert

    This function converts the data type from str to a type relevant
    to insert in SQLAlchemy

    Parameters
    ----------
    str_ : str
        the data in str
    type_ :
        the data type in SQLAlchemy, i.e., one of the types listed in
        https://docs.sqlalchemy.org/en/13/core/type_basics.html

    Returns
    -------
    the data in the type relevant for insert

    """
    if isinstance(type_, sqlalchemy.sql.sqltypes.DATE):
        if str_:
            return datetime.datetime.strptime(str_, "%Y-%m-%d").date()
        return None
    return str_

##__________________________________________________________________||
def export_db_to_csv_files(outdir):
    """export all tables in the DB to CSV files

    The CSV files will be stored in the folder `csvdir`: one CSV file
    for one table with the file name <<table name>>.csv

    Parameters
    ----------
    csvdir : str
        a path to a folder to store the CSV files


    The tables need to be already defined in the DB.

    """
    tbl_names = get_all_table_names()

    pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)

    for tbl_name in tbl_names:
        csv_filename = '{}.csv'.format(tbl_name)
        csv_path = os.path.join(outdir, csv_filename)
        result_proxy = get_resultproxy_of_select_all_rows(tbl_name)
        with open(csv_path, 'w', newline='') as f:
            csv_writer = csv.writer(f, lineterminator='\n')
            csv_writer.writerow(result_proxy.keys())
            csv_writer.writerows(result_proxy)

##__________________________________________________________________||
