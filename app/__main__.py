from . import create_app
from flask_sqlalchemy import SQLAlchemy

app = create_app()

if __name__ == "__main__":  # only in dev
    app.run(host="0.0.0.0", port=8080, debug=True)
