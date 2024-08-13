import re
import phonenumbers
from wtforms import Form, StringField, validators
from wtforms.validators import ValidationError


def at_least_one_filled(form, field):
    if not form.phone_number.data and not form.email_address.data:
        raise ValidationError("Either phone number or email address must be provided.")


def validate_mpesa_phone(form, field ):

    try:
        # Remove any non-digit characters
        cleaned_phone_number = re.sub(r'\D', '', field.data)

        # Define the regex pattern for Kenyan phone numbers
        pattern = r'^(254)([71][0-9]{8})$'
        regex = re.compile(pattern)

        # Check if the cleaned phone number matches the pattern
        if not regex.match(cleaned_phone_number):
            raise ValidationError('Invalid Mpesa phone number format')

    except Exception as ex:
        print(ex)


class OrderForm(Form):
    """A form representing new Order"""

    first_name = StringField(
        "First Name",
        [validators.DataRequired("First Name is required!")],
    )

    middle_name = StringField(
        "Sur Name",
        [],
    )

    last_name = StringField(
        "Last Name",
        [validators.DataRequired("Last Name is required!")],
    )

    street_address = StringField(
        "Street Address",
        [validators.DataRequired("Street Address is required!")],
    )
    city = StringField(
        "City",
        [validators.DataRequired("City is required!")],
    )
    zip_code = StringField(
        "Zip Code",
        [validators.DataRequired("Zip Code is required!")],
    )
    state_or_province = StringField(
        "State or Province",
        [validators.DataRequired("State or Province is required!")],
    )
    email_address = StringField(
        "Email Address",
        [validators.DataRequired("Email Address Required!"), validators.Email()],
    )
    phone_number = StringField(
        "Phone Number",
        [validators.DataRequired("Phone Number Required!")],
    )

    mpesa_number = StringField(
        "Mpesa Number",
        [validators.DataRequired("Mpesa Mobile Number Required"), validate_mpesa_phone],
    )
