from flask_migrate import Migrate

from .sa import sa
from .conn import close_db_connection
from .cmds import init_db_command
from .cmds import dump_db_command
from .cmds import import_csv_command
from .cmds import export_csv_command

migrate = Migrate()

##__________________________________________________________________||
def init_app(app):
    """initializes the Flask application object

    This function is called by `create_app()` of Flask

    Parameters
    ----------
    app : Flask
        The Flask application object, an instance of `Flask`
    """
    sa.init_app(app)
    migrate.init_app(app, sa)
    app.cli.add_command(init_db_command)
    app.cli.add_command(dump_db_command)
    app.cli.add_command(import_csv_command)
    app.cli.add_command(export_csv_command)
    app.teardown_appcontext(close_db_connection)

##__________________________________________________________________||
