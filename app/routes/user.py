from flask import Blueprint, request, jsonify
from app.controllers.user import new_user, get_users, delete_user, update_user

# User blueprint
user_route = Blueprint("user_route", __name__, url_prefix="/api/users")


@user_route.route("/", methods=["POST"])
def new_user_route():
    """New User"""

    valid, msg = new_user(request.form)

    if valid:
        return jsonify(msg=msg), 201

    return jsonify(msg=msg), 500


@user_route.route("/", methods=["GET"])
def get_users_route():
    """Get the users"""

    valid, response = get_users(request.args.get("user_id"))

    if valid:
        return jsonify(data=response), 200

    return jsonify(msg=response), 500


@user_route.route("/", methods=["PUT", "PATCH"])
def update_user_route():
    """Update User"""

    valid, response = update_user(request.args.get("user_id"), request.form)

    if valid:
        return jsonify(msg="Successfully Updated User!"), 201

    else:
        return jsonify(msg="Database error occurred!"), 500


@user_route.route("/", methods=["DELETE"])
def delete_user_route():
    """Delete User"""

    valid, response = delete_user(request.args.get("user_id"))

    if valid:
        return jsonify(msg="Successfully Deleted User!"), 200

    else:
        return jsonify(msg="Database error occurred!"), 500
