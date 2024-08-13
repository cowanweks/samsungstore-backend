import datetime
import random
import string


class bcolors:
    """ """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def generate_tracking_number():
    # Current date and time as a string (e.g., 20240624 for June 24, 2024)
    date_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Random alphanumeric string
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    # Combine them to form the tracking number
    tracking_number = date_str + random_str
    return tracking_number.capitalize()
