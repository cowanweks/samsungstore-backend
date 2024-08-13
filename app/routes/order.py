import os

import requests
from flask import request, jsonify, Blueprint
from app.controllers.mailing import send_email
from app.models import db, Order, Product, CartItem

order_route = Blueprint("order_route", __name__, url_prefix="/api/orders")

BASE_URL = os.getenv("BASE_URL")


@order_route.get("/")
def get_orders_route():
    """Get Orders"""

    order_id = request.args.get("order_id")

    try:
        if order_id:

            orders = db.session.query(Order).filter_by(Order.order_id == order_id).scalar()

        else:

            orders = db.session.query(Order).order_by(Order.order_id).all()

        serialized_orders = [order.serialize() for order in orders]
        return jsonify(serialized_orders), 200

    except Exception as ex:
        print(ex)
        return jsonify(str(ex)), 500


@order_route.delete("/")
def delete_order_route():
    """Delete Order"""

    order_id = request.args.get("order_id")

    if not order_id:
        return jsonify(error="Order ID Required")

    try:
        db.session.execute(db.delete(Order).where(Order.order_id == order_id))
        db.session.commit()
        return jsonify("Successfully Deleted Order!"), 300

    except Exception as ex:
        print(ex)
        return jsonify(str(ex)), 500


@order_route.get("/update_payment_status")
def update_payment_status():
    order_id = request.args.get("order_id")

    try:
        if not order_id:
            return jsonify("Order ID Not Provided")

        db.session.query(Order).filter(Order.order_id == order_id).update({'payment_status': 'completed'})
        db.session.commit()

        return jsonify(f"Order {order_id} payment status updated successfully")

    except Exception as ex:
        print(ex)
        return jsonify(str(ex)), 500


@order_route.put("/update_stock")
@order_route.patch("/update_stock")
def update_product_stock():
    cart_id = request.args.get("cart_id")

    try:
        cart_items = db.session.query(CartItem).filter_by(cart_id=cart_id)

        for item in cart_items:
            print(item.product_name)
            print(item.quantity)

            db.session.query(Product).filter_by(product_id=item.product_id).update({
                'in_stock': Product.in_stock - item.quantity
            })
            db.session.commit()

        return jsonify("Successfully Updated product Quantity"), 200

    except Exception as ex:
        print(ex)
        return jsonify(str(ex)), 500


@order_route.get("/email_customer")
def email_customer():
    order_id = request.args.get("order_id")
    first_name = request.args.get("first_name")
    email_address = request.args.get("email_address")
    tracking_number = request.args.get("tracking_number")

    if not first_name:
        return jsonify("First Name Not Provided"), 400

    if not email_address:
        return jsonify("Email address Not Provided"), 400

    if not order_id:
        return jsonify("Order ID Not Provided"), 400

    if not tracking_number:
        return jsonify("Tracking Number Not Provided"), 400

    if send_email(
            "samsungphonesandspairecentre@gmail.com",
            email_address,
            "Your Order Confirmation and Tracking Information",
            f"""
Dear {first_name},

We are pleased to inform you that your order has been successfully placed with us. Thank you for choosing our store for your purchase!

Here are the details of your order:
- Order Number: {order_id}
- Tracking Number: {tracking_number}

You can track your order using the tracking number provided through our website or the courier's tracking service.

We are committed to providing you with the best service possible. If you have any questions or need further assistance, please do not hesitate to contact our customer support team at support@example.com.

Thank you once again for shopping with us. We look forward to serving you again in the future.

Best regards,

Paul Mwangi
Director
Samsung Phone and Store Center
samsungphonesandspairecentre@gmail.com
"""
    ):
        return jsonify("Email sent successfully!"), 200

    return jsonify("Could not send Email!"), 500


@order_route.get("/email_store")
def email_store():

    order_id = request.args.get("order_id")
    total_amount = request.args.get("total_amount")
    email_address = request.args.get("email_address")
    tracking_number = request.args.get("tracking_number")

    if not total_amount:
        return jsonify("Total amount Not Provided"), 400

    # if not email_address:
    #     return jsonify("Email address Not Provided"), 400

    if not order_id:
        return jsonify("Order ID Not Provided"), 400

    if not tracking_number:
        return jsonify("Tracking Number Not Provided"), 400

    if send_email(
        os.getenv("SMTP_USER"),
        "samsungphonesandspairecentre@gmail.com"
        ,
        f"New Order Placed: {order_id}",
            f"Dear Store Owner,\n\nA new order has been placed.\n\nOrder ID: {order_id}\n\nBest regards,\nYour "
            f"E-commerce Platform"
    ):
        return jsonify("Email sent successfully!"), 200

    else:
        return jsonify("Could not send Email!"), 500


@order_route.get("/complete_order")
def complete_order_after_payment():

    payment_request_id = request.args.get("payment_request_id")
    order_id = request.args.get("order_id")

    order = db.session.query(Order).filter_by(order_id=order_id).scalar()

    response = requests.get("{}/payment/check_status/{}".format(BASE_URL, payment_request_id))
    response_data = response.json()

    if response.status_code == 200:

        if response_data["status"] == 1:
            # Clear the shopping cart
            response = requests.get("{}/cart/clear?cart_id={}".format(BASE_URL, order.cart_id))

            if response.status_code == 200:
                # Update the Product stock amount
                response = requests.get("{}/orders/update_stock?cart_id={}"
                                        .format(BASE_URL, order.cart_id))

                if response.status_code == 200:
                    # Email customer the order number and the tracking number
                    response = requests.post(
                        f"{BASE_URL}/orders/email_customer?order_id={order.order_id}"
                        f"&first_name={order.first_name}"
                        f"&email_address={order.email_address}"
                        f"&tracking_number={order.tracking_number}"
                    )

                    if response.status_code == 200:

                        try:

                            # Complete the Order
                            db.session.query(Order).filter_by(Order.order_id == order_id).update({'completed': True})
                            db.session.commit()

                            response = requests.get(
                                f"{BASE_URL}/orders/email_store?order_id={order_id}"
                                f"&total_amount={order.total_amount}&tracking_number={order.tracking_number}")

                            if response.status_code == 200:
                                # Successfully completed the Order
                                return jsonify("Order Placed successfully!"), 200
                            else:
                                # Failed Sending Store owner email
                                return response.content.decode(), response.status_code

                        except Exception as ex:
                            print(ex)
                            return jsonify(str(ex))
                    else:
                        return response.content.decode(), response.status_code
                else:
                    return response.content.decode(), response.status_code
            else:
                return response.content.decode(), response.status_code

        else:
            return response.content.decode(), response.status_code

    # Updating stock Failed
    return response.content.decode(), response.status_code
