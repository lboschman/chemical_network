#!/usr/bin/env python

"""This file is used to provide a proper starting point when running the application.
"""


from src.app.base_app import app

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True, port=8050)