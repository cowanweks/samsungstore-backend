import base64
import json
import logging
import os.path
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth
from flask import Blueprint, request, jsonify, current_app

# Payment blueprint
payment_route = Blueprint("payment_route", __name__, url_prefix="/api/payment")

BASE_URL = os.getenv("BASE_URL")

def get_mpesa_access_token():
    mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    consumer_key = '2y8zOJ5AXxtnYFneBiAfjI4hwOVyxPwU'
    consumer_secret = '2GztfgEbczZPFpd1'
    response = requests.get(mpesa_auth_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    if response.status_code == 200:
        try:
            data = response.json()
            access_token = data.get("access_token")
            if access_token:
                return access_token
            else:
                logging.error("Access token not found in response")
                return None
        except ValueError:
            logging.error("Response content is not valid JSON")
            return None
    else:
        logging.error(f"Failed to get access token, status code: {response.status_code}")
        return None


@payment_route.get("/access_token")
def get_access_token_route():
    token = get_mpesa_access_token()
    return token


@payment_route.get("/register_urls")
def register_urls_route():
    mpesa_endpoint_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    access_token = get_mpesa_access_token()
    req_headers = {"Authorization": "Bearer %s" % access_token}
    req_body = {
        "ShortCode": "601426",
        "ResponseType": "Completed",
        "ConfirmationURL": BASE_URL + "/payment/confirm",
        "ValidationURL": BASE_URL + "/payment/validate"
    }

    response_data = requests.post(mpesa_endpoint_url, headers=req_headers, json=req_body)
    return response_data.json()


@payment_route.get("/confirm")
def confirm_payment_route():
    data = request.json()

    print(data)

    with open(os.path.join(current_app.instance_path, "confirm.json"), "a") as fd:
        fd.write(json.dumps(data))
        fd.close()

    return {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }


@payment_route.get("/validate")
def validate_payment_route():
    data = request.json()

    with open(os.path.join(os.getcwd(), "validation.json"), "a") as fd:
        fd.write(json.dumps(data))
        fd.close()

    return {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }


@payment_route.get("/simulate")
def simulate_route():
    mpesa_endpoint_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    access_token = get_mpesa_access_token()
    req_headers = {"Authorization": "Bearer %s" % access_token}
    req_body = {
        "ShortCode": "601426",
        "CommandID": "CustomerPayBillOnline",
        "Amount": "1",
        "Msisdn": "254708374149",
        "BillRefNumber": "Payment Testing"
    }

    response = requests.post(mpesa_endpoint_url, headers=req_headers, json=req_body)
    return response.json()


@payment_route.get("/pay")
def pay_route():
    phone_number = request.args.get("phone_number")
    total_amount = request.args.get("total_amount")
    transaction_description = request.args.get("transaction_description")

    if transaction_description is None:
        transaction_description = ""

    if not phone_number:
        return jsonify("Phone number not provided"), 400

    my_endpoint = BASE_URL + "/api/payment/success"
    mpesa_endpoint_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    access_token = get_mpesa_access_token()
    req_headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json"
    }

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = "174379" + "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919" + timestamp
    data_pass = base64.b64encode(password.encode('utf-8')).decode('utf-8')

    req_body = {
        "BusinessShortCode": "174379",
        "Password": data_pass,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "PartyA": phone_number,
        "PartyB": "174379",
        "PhoneNumber": phone_number,
        "CallBackURL": my_endpoint,
        "AccountReference": "353 562",
        "TransactionDesc": "Purchased {}".format(transaction_description),
        "Amount": total_amount
    }

    try:
        response = requests.post(mpesa_endpoint_url, headers=req_headers, json=req_body)
        response.raise_for_status()  # raises exception when not a 2xx response
        return response.json(), response.status_code
    except requests.exceptions.RequestException as ex:
        logging.error(f"Error occurred: {ex}")
        return jsonify(error=str(ex)), 500


@payment_route.get("/check_status/<checkout_request_id>")
def check_payment_status(checkout_request_id):
    """Endpoint for querying transaction status"""

    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query'
    access_token = get_mpesa_access_token()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = "174379" + "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919" + timestamp
    data_pass = base64.b64encode(password.encode('utf-8')).decode('utf-8')

    # Prepare headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Prepare request payload
    payload = {
        'BusinessShortCode': '174379',
        'Password': data_pass,
        'Timestamp': timestamp,
        'CheckoutRequestID': checkout_request_id
    }

    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        response_data = response.json()

        # Check if payment is successful
        if response_data['ResponseCode'] == '0' and response_data[
            'ResultDesc'] == 'The service request is processed successfully.':
            return jsonify(msg="Transaction Complete", status=1), response.status_code

        else:
            return jsonify(msg="Transaction Failed!", status=0), response.status_code

    except requests.exceptions.RequestException as ex:
        print(f"Error querying transaction status: {ex}")
        return jsonify(f"Error querying transaction status: {str(ex)}"), 500


@payment_route.get('/success')
def lnmo_result():

    data = request.get_data()

    with open('success.json', 'ab') as fd:
        fd.write(data)
        fd.close()

    return jsonify("Success"), 200
