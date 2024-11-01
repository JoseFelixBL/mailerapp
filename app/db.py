import mariadb
# import mysql.connector
# Click is a simple Python module inspired by the stdlib optparse to make writing command line scripts fun.
import click
from flask import current_app, g
from flask.cli import with_appcontext
# def with_appcontext(f: F@with_appcontext) -> F@with_appcontext
# Wraps a callback so that it's guaranteed to be executed with the script's application context.
from .schema import instructions


def get_db():
    if db not in g:
        g.db = mariadb.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)

    db.commit()


# init-db es el comando que invocamos desde la línea de comandos para que se ejecute init_db_command()
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Base de datos inicializada.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
