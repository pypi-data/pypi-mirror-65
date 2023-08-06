"""Commands (click)

"""
from flask.cli import with_appcontext
import click

import json

from .ops import define_tables
from .ops import export_db_to_dict_of_dict_list
from .ops import import_tables_from_csv_files
from .ops import export_db_to_csv_files

##__________________________________________________________________||
@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    define_tables()
    click.echo("Initialized the database.")

##__________________________________________________________________||
@click.command("dump-db")
@with_appcontext
def dump_db_command():
    """Dump the DB contents

    """
    db_content = export_db_to_dict_of_dict_list()

    click.echo(json.dumps(db_content, indent=2, default=str))
    # https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable

##__________________________________________________________________||
@click.command("import-csv")
@click.argument("csvdir", type=click.Path(exists=True))
@with_appcontext
def import_csv_command(csvdir):
    """Import tables from CSV files in CSVDIR into the DB.

    """
    import_tables_from_csv_files(csvdir)

##__________________________________________________________________||
@click.command("export-csv")
@click.argument("csvdir", type=click.Path())
@with_appcontext
def export_csv_command(csvdir):
    """Export the tables into the DB to CSV files in CSVDIR.

    """
    export_db_to_csv_files(csvdir)

##__________________________________________________________________||
