#!/usr/bin/env python
import sys
import os

# third imports
from docopt import DocoptExit, docopt
import pandas as pd

# local imports
from aws_local import s3
from server import server

APP_BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def docopt_full_help(docstring, *args, **kwargs):
    try:
        return docopt(docstring, *args, **kwargs)
    except DocoptExit:
        raise SystemExit(docstring)


def handle_command(handlers, options, doc):
    """
    Execute a command if is valid or exit with doc help.

    Parameters
    ----------
    handlers : dict
        Dict with commands (functions) handlers.
    options : dict
        Dict with args parsed.
    doc : str
        Docopt documentation.

    """
    command = options["COMMAND"]
    if command is None:
        raise SystemExit(doc)
    try:
        handler = handlers[command]
    except KeyError:
        raise SystemExit(f"No such command: {command}\n{doc}")
    docstring = handler.__doc__
    if docstring is None:
        raise SystemExit(f"No such command: {command}\n{doc}")
    options = docopt_full_help(docstring, options["ARGS"], options_first=True)
    handler(options)


def load(options):
    """Load local data to S3 bucket.

    Usage:
        load [options]

    Options:
        -h, --help                      Show this message.
        -d DIR, --directory     DIR     Local path where data is located. [default: ./]
        -b BCT, --bucket        BCT     S3 Bucket name. [default: ./]
    """
    _dir = options["--directory"]
    _bucket = options["--bucket"]
    return s3.load_data(_dir, _bucket)


def database(options):
    """Load local data to S3 bucket.

    Usage:
        database [options]

    Options:
        -h, --help                      Show this message.
        -m MTD, --metadata      MTD     Path to metadata file.
    """
    _metadata = options["--metadata"]
    df = None
    try:
        df = pd.read_csv(_metadata, error_bad_lines=False)
        dir_ = os.path.join(APP_BASE_DIR, 'data', 'db.pkl')
        df.to_pickle(dir_)
    except Exception as e:
        print(f"Error creating dataframe with {_metadata} - {e}")


def server_start(options):
    """Start Flask server.

    Usage:
        start [options]

    Options:
        -h, --help              Show this message.
    """
    server.start()


def server_stop(options):
    """Stop Flask server.

    Usage:
        stop [options]

    Options:
        -h, --help              Show this message.
    """
    server.stop()


def server_(options):
    """Start Flask web app.

    Usage:
        server [options] COMMAND [ARGS...]

    Commands:
        start           Start Flask server.
        stop            Stop Flask server.

    Options:
        -h, --help      Show this message.
    """
    handlers = {
        "start": server_start,
        "stop": server_stop,

    }
    handle_command(
        handlers,
        options,
        server_.__doc__,
    )


def main():
    """ML-pipeline CLI.
    Usage:
        ./main.py [options] COMMAND [ARGS...]

    Commands:
        load            Load data to S3.
        database        Create a database from S3.
        server          Run Flask server.

    Options:
        -h, --help      Show this message.
        -i, --ignore    Ignore config validation.
    """
    options = docopt_full_help(main.__doc__, sys.argv[1:], options_first=True)
    handlers = {
        "load": load,
        "database": database,
        "server": server_,
    }
    handle_command(handlers, options, main.__doc__)


if __name__ == "__main__":
    main()
