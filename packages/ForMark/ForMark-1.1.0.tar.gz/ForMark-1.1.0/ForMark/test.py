import os

from ForMark.ForApp import ForApp
from flask import Flask


SECRET_KEY = "macktest"
# mongodb://root:pass@localhost:27017/bug_help
MONGO_HOST_URL = 'mongodb://localhost:27017/test'

log_folder = 'log/bug_help.log'
mark_tools = ForApp(import_name=__name__,
                    log_folder=log_folder,
                    MONGO_HOST_URL=MONGO_HOST_URL,
                    secret_key=SECRET_KEY,
                    )
app = mark_tools.app


@app.route('/')
def hello():
    """Add some data

        Add some data in this routing

        Args:
            pass

        Returns:
            pass
        """
    return "Help World"


@app.errorhandler(404)
def not_found(e):
    return '404'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4444)
