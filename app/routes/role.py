""" """

from uuid import uuid4
import sqlalchemy
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models import db, Roles


# Role blueprint
role_route = Blueprint("role_route", __name__, url_prefix="/api/roles")


# The route that handles role registration
@role_route.route("/", methods=["POST"])
def new_role():
    # Get the users identity

    # TODO Form Validation
    data = request.get_json()

    role_id = str(uuid4())
    role_name = data.get("role_name")
    role_description = data.get("role_description")

    print(role_description)

    try:
        db.session.add(
            Roles(
                role_id=role_id, role_name=role_name, role_description=role_description
            )
        )
        db.session.commit()
        return jsonify("Successfully Created new Role!"), 201

    except IntegrityError as ex:
        print("{}".format(ex))
        db.session.rollback()
        return jsonify(msg="Role already exists!"), 400


@role_route.route("/", methods=["GET"])
def get_roles():
    """Get the Roles"""

    role_id = request.args.get("role_id")

    try:
        if role_id:
            roles = (
                db.session.execute(
                    db.select(Roles)
                    .where(Roles.role_id == role_id)
                    .order_by(Roles.role_id)
                )
                .scalars()
                .all()
            )
        roles = (
            db.session.execute(db.select(Roles).order_by(Roles.role_id)).scalars().all()
        )
        serialized_roles = [role.serialize() for role in roles]
        return jsonify(serialized_roles), 200

    except SQLAlchemyError as ex:
        print(str(ex))
        db.session.rollback()
        return jsonify(msg="Database error occurred!"), 500


# The Route that handles role information update
@role_route.route("/", methods=["PUT", "PATCH"])
def update_role():
    """"""
    role_id = request.args.get("role_id")
    data = request.get_json()

    try:
        db.session.execute(
            db.update(Roles).where(Roles.role_id == role_id).values(data)
        )
        db.session.commit()
        return jsonify(msg="Successfully Updated Role!"), 200

    except SQLAlchemyError as ex:
        print(str(ex))
        db.session.rollback()
        return jsonify(msg="Database error occurred!"), 500


# The route that handles role deletion
@role_route.route("/", methods=["DELETE"])
def delete_role():
    """"""
    role_id = request.args.get("role_id")

    try:
        db.session.execute(db.delete(Roles).where(Roles.role_id == role_id))
        db.session.commit()
        return jsonify(msg="Successfully Deleted Role!"), 200

    except sqlalchemy.exc.SQLAlchemyError as ex:
        print(str(ex))
        db.session.rollback()
        return jsonify(msg="Database error occurred!"), 500
