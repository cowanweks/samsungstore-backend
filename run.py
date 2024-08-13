import os
from flask import send_from_directory
from app import create_app


flask_app = create_app()
flask_app.static_folder = "static"


@flask_app.route("/")
def index_page():
    return send_from_directory('static', 'index.html')


@flask_app.route("/<path:path>")
def static_file(path):
    return flask_app.send_static_file(path)


def main():
    os.environ["APP_ENV"] = "production"
    os.environ["SMTP_USER"] = "cowanweks"
    os.environ["SMTP_PASSWD"] = "ultimate"
    os.environ["BASE_URL"] = "https://web-production-7579e.up.railway.app/"
    flask_app.run(host=flask_app.config.get("HOST"), port=flask_app.config.get("PORT"))


if __name__ == "__main__":
    main()
