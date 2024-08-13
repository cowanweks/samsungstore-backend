from functools import wraps
from dotenv import load_dotenv, find_dotenv
from app.extensions import db
from app.utils import bcolors
from app.models import Cart


def app_setup(func):
    """Set up the environment before starting the flask app"""

    @wraps(func)
    def init():
        print(bcolors.OKGREEN + "[*] - Hello am running before flask!")
        print(bcolors.OKGREEN + "[*] - Cleaning All empty carts!")

        # Load environment variables
        load_dotenv(find_dotenv(".env"))

        return func()

    return init


def clean_empty_carts():
    empty_carts = Cart.query.filter(~Cart.items.any()).all()
    for cart in empty_carts:
        db.session.delete(cart)
    db.session.commit()
