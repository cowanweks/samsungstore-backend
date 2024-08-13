from wtforms import Form, StringField, validators


class ShippingAddressForm(Form):
    full_name = StringField('Full Name', validators=[validators.DataRequired(), validators.Length(max=100)])
    street_address = StringField('Street Address', validators=[validators.DataRequired(), validators.Length(max=200)])
    address_line_2 = StringField('Address Line 2', validators=[validators.Length(max=200)])
    city = StringField('City', validators=[validators.DataRequired(), validators.Length(max=100)])
    state = StringField('State/Province/Region', validators=[validators.DataRequired(), validators.Length(max=100)])
    postal_code = StringField('Postal/Zip Code', validators=[validators.DataRequired(), validators.Length(max=20)])
    country = StringField('Country', validators=[validators.DataRequired(), validators.Length(max=100)])
    phone_number = StringField('Phone Number', validators=[validators.DataRequired(), validators.Length(max=20)])
    email_address = StringField('Email Address', validators=[validators.Email(), validators.Length(max=100)])


class UpdateShippingAddressForm(Form):
    full_name = StringField('Full Name', validators=[validators.Length(max=100)])
    street_address = StringField('Street Address', validators=[validators.Length(max=200)])
    address_line_2 = StringField('Address Line 2', validators=[validators.Length(max=200)])
    city = StringField('City', validators=[validators.Length(max=100)])
    state = StringField('State/Province/Region', validators=[validators.Length(max=100)])
    postal_code = StringField('Postal/Zip Code', validators=[validators.Length(max=20)])
    country = StringField('Country', validators=[validators.Length(max=100)])
    phone_number = StringField('Phone Number', validators=[validators.Length(max=20)])
    email_address = StringField('Email Address', validators=[validators.Email(), validators.Length(max=100)])