"""
Web Server Gateway Interface file to be used by Gunicorn
"""
from . import create_app

app = create_app()

if __name__ == "__main__":
    app.run(use_reloader=True, debug=True)
