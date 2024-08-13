import os
from uuid import uuid4
from flask import Blueprint, request, jsonify
from app.models import db, Product, Image
from app.forms.product import ProductForm, ProductUpdateForm
from app.models import db, Product
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# Products blueprint
product_route = Blueprint(
    "product_route", __name__, url_prefix="/api/products"
)


@product_route.post("/")
def new_product_route():
    """New Product"""

    new_product_form = ProductForm()

    if new_product_form.validate():

        product_image = new_product_form.product_image.data

        mimetype = product_image.mimetype
        file_name = str(uuid4())
        extension = os.path.splitext(product_image.filename)[1]

        file_name = secure_filename("{}{}".format(file_name, extension))

        try:
            img = Image(id=file_name, image_name=file_name, image=product_image.read(), mimetype=mimetype)
            db.session.add(img)
            db.session.commit()

            product = Product(
                product_id=str(uuid4()),
                product_name=new_product_form.product_name.data,
                available_colors=new_product_form.available_colors.data,
                product_category=new_product_form.product_category.data,
                description=new_product_form.description.data,
                is_available=new_product_form.is_available.data,
                product_unit_price=new_product_form.product_unit_price.data,
                product_image=file_name,
                in_stock=new_product_form.in_stock.data,
                battery=new_product_form.battery.data,
                cameras=new_product_form.cameras.data,
                display=new_product_form.display.data,
                processor=new_product_form.processor.data,
                ram=new_product_form.ram.data,
                brand=new_product_form.brand.data,
                model=new_product_form.model.data,
            )

            db.session.add(product)
            db.session.commit()
            return jsonify("Successfully Created new Product!"), 200

        except IntegrityError as ex:
            print(ex)
            return jsonify("Product already exists!"), 400

    else:
        print(new_product_form.errors)
        return jsonify(new_product_form.errors), 400



@product_route.get("/")
def get_products_route():
    """Get Products"""

    product_id = request.args.get("product_id")
    product_category = request.args.get("category")

    try:
        query = db.select(Product).order_by(Product.product_id)

        if product_id:

            product = db.session.query(Product).filter_by(product_id=product_id).scalar()
            if not product:
                return jsonify(f"Product of id {product_id} can not be found!"), 404

            return jsonify(product.serialize()), 200

        if product_category:

            products = db.session.query(Product).filter_by(product_category=product_category).all()

            if not products:
                return jsonify("Products of category {} can not be found!"),

            serialized_products = [product.serialize() for product in products]
            return serialized_products, 200

        products = db.session.query(Product).all()
        serialized_products = [product.serialize() for product in products]
        return serialized_products, 200

    except Exception as ex:
        print(ex)
        return jsonify(str(ex)), 500


@product_route.put("/")
@product_route.patch("/")
def update_product_route():
    """Update Product"""

    product_id = request.args.get("product_id")

    try:
        updated_product_form = ProductUpdateForm(request.form)

        if updated_product_form.validate():
            db.session.execute(
                db.update(Product)
                .where(Product.product_id == product_id)
                .values(
                    product_id=updated_product_form.product_id.data,
                    product_name=updated_product_form.product_name.data,
                )
            )
            db.session.commit()
            return jsonify("Successfully Updated Product!"), 200

        else:
            return jsonify(updated_product_form.errors), 400

    except SQLAlchemyError as ex:
        print(ex)
        return jsonify(f"Database error occurred! {ex}"), 500




@product_route.delete("/")
def delete_product_route():
    """Delete Product"""

    product_id = request.args.get("product_id")

    try:
        db.session.execute(db.delete(Product).where(Product.product_id == product_id))
        db.session.commit()
        db.session.close()
        return jsonify("Successfully Deleted Product!"), 200

    except SQLAlchemyError as ex:
        print(ex)
        db.session.close()
        return jsonify("Database error occurred!"), 400



@product_route.delete("/delete_all")
def delete_all_products():
    try:
        # Delete all records in the Image table
        num_rows_deleted = db.session.query(Product).delete()
        db.session.commit()
        return jsonify({'message': 'All products deleted successfully', 'num_rows_deleted': num_rows_deleted}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
