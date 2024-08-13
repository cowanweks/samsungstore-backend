import json
import datetime
from sqlalchemy.types import DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from .extensions import db
from sqlalchemy import LargeBinary


class Users(db.Model):
    """Model Representing Users"""

    user_id: Mapped[str] = mapped_column(db.String, primary_key=True)
    customer_id: Mapped[str] = mapped_column(db.String(), unique=True)
    email: Mapped[str] = mapped_column(db.String(), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(db.String(), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(db.String())
    roles: Mapped[str] = mapped_column(db.String())

    def serialize(self):
        return {
            "user_id": self.user_id,
            "customer_id": self.customer_id,
            "password": self.password,
            "username": self.username,
            "email": self.email,
            "role": self.roles,
        }


class Address(db.Model):
    """Model Representing Users"""

    address_id: Mapped[str] = mapped_column(db.String, primary_key=True)
    customer_id: Mapped[str] = mapped_column(db.String(), unique=True)
    street_address: Mapped[str] = mapped_column(db.String())
    address_line_2: Mapped[str] = mapped_column(db.String())
    city: Mapped[str] = mapped_column(db.String())
    state: Mapped[str] = mapped_column(db.String())
    postal_code: Mapped[str] = mapped_column(db.String())
    country: Mapped[str] = mapped_column(db.String())
    phone_number: Mapped[str] = mapped_column(db.String())
    email_address: Mapped[str] = mapped_column(db.String())

    def serialize(self):
        return {
            "address_id": self.address_id,
            "customer_id": self.customer_id,
            "email_address": self.email_address,
            "address_line_2": self.address_line_2,
            "street_address": self.street_address,
            "city": self.city,
            "country": self.country,
            "phone_number": self.phone_number,
            "postal_code": self.postal_code,
            "state": self.state,
        }


class ShippingAddress(Address):
    """Model Representing Shipping Address"""

    __tablename__ = "shipping_addresses"

    full_name: Mapped[str] = mapped_column(db.String())

    def serialize(self):
        return {
            "full_name": self.full_name,
            "address_id": self.address_id,
            "customer_id": self.customer_id,
            "email_address": self.email_address,
            "address_line_2": self.address_line_2,
            "street_address": self.street_address,
            "city": self.city,
            "country": self.country,
            "phone_number": self.phone_number,
            "postal_code": self.postal_code,
            "state": self.state,
        }


class Customer(db.Model):
    """Model Representing Users"""

    __tablename__ = "customers"

    customer_id: Mapped[str] = mapped_column(db.String, primary_key=True)
    first_name: Mapped[str] = mapped_column(db.String())
    middle_name: Mapped[str] = mapped_column(db.String())
    last_name: Mapped[str] = mapped_column(db.String())
    phone: Mapped[str] = mapped_column(db.String())
    email: Mapped[str] = mapped_column(db.String())
    address: Mapped[str] = mapped_column(db.String)
    shipping_address: Mapped[str] = mapped_column(db.String)
    reg_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now()
    )

    def serialize(self):
        return {
            "customer_id": self.customer_id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "shipping_address": self.shipping_address,
            "reg_date": self.reg_date,
        }


class Image(db.Model):
    """Model representing images"""

    __tablename__ = 'images'

    id = db.Column(db.Text, primary_key=True)
    image_name = db.Column(db.Text, unique=True, nullable=False)
    image = db.Column(LargeBinary, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)


class Product(db.Model):
    """Model Representing Staffs"""

    __tablename__ = "products"

    product_id = db.Column(db.String, primary_key=True)
    product_name = db.Column(db.String, nullable=False)
    product_unit_price = db.Column(db.Numeric, nullable=False)
    description = db.Column(db.String, nullable=False)
    product_category = db.Column(db.String, nullable=False)
    available_colors = db.Column(db.String, nullable=False)
    is_available = db.Column(db.Boolean, nullable=False)
    in_stock = db.Column(db.Integer, nullable=False)
    product_image = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=True)
    brand = db.Column(db.String, nullable=True)
    battery = db.Column(db.String, nullable=True)
    cameras = db.Column(db.String, nullable=True)
    processor = db.Column(db.String, nullable=True)
    display = db.Column(db.String, nullable=True)
    ram = db.Column(db.String, nullable=True)

    @property
    def available_colors_list(self):
        if self.available_colors:
            return json.loads(self.available_colors)

        return []

    @available_colors_list.setter
    def available_colors_list(self, value):
        self.available_colors = json.dumps(value)

    def serialize(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_unit_price": float(self.product_unit_price),
            "description": self.description,
            "product_category": self.product_category,
            "available_colors": self.available_colors_list,
            "is_available": self.is_available,
            "in_stock": self.in_stock,
            "product_image": self.product_image,
            "brand": self.brand,
            "model": self.model,
            "battery": self.battery,
            "cameras": self.cameras,
            "processor": self.processor,
            "display": self.display,
            "ram": self.ram
        }


class Order(db.Model):
    """Model representing an order"""

    __tablename__ = "orders"

    order_id = db.Column(db.String, primary_key=True, nullable=False)
    cart_id = db.Column(db.String)
    total_amount = db.Column(db.Numeric)
    first_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    last_name = db.Column(db.String)
    street_address = db.Column(db.String)
    city = db.Column(db.String)
    zip_code = db.Column(db.String)
    state_or_province = db.Column(db.String, nullable=False)
    email_address = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default="Processing")
    shipped = db.Column(db.Boolean, default=False)
    payment_status = db.Column(db.String, default="not_completed")
    tracking_number = db.Column(db.String)
    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now()
    )

    def serialize(self):

        return {
            "order_id": self.order_id,
            "cart_id": self.cart_id,
            "email_address": self.email_address,
            "phone": self.phone_number,
            "state_or_province": self.state_or_province,
            "street_address": self.street_address,
            "city": self.city,
            "zipcode": self.zipcode,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "status": self.last_name,
            "created_at": self.created_at,
            "shipping_address": self.shipping_address,
        }


class Roles(db.Model):
    """Model Representing Roles available to registered users"""

    __tablename__ = "roles"

    role_id: Mapped[str] = mapped_column(db.String, primary_key=True, nullable=False)
    role_name: Mapped[str] = mapped_column(db.String(), unique=True, nullable=False)
    role_description: Mapped[str] = mapped_column(db.String())

    def serialize(self):
        return {
            "role_id": self.role_id,
            "role_name": self.role_name,
        }


class CartItem(db.Model):
    """Cart Model"""
    __tablename__ = 'cart_items'

    item_id = db.Column(db.String, primary_key=True)
    cart_id = db.Column(db.String, nullable=False)
    product_id = db.Column(db.String, nullable=False)
    product_name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String, nullable=True)
    created_at = db.Column(DateTime(timezone=True), default=datetime.datetime.now())

    def price(self) -> float:
        """Get product price"""
        price = db.session.query(Product.product_unit_price).filter_by(product_id=self.product_id).scalar()
        return price

    def serialize(self):
        return {
            "item_id": self.item_id,
            "cart_id": self.cart_id,
            "product_id": self.item_id,
            "quantity": self.quantity,
            "product_unit_price": self.price(),
            "in_stock": db.session.query(Product.in_stock).filter_by(product_id=self.product_id).scalar(),
            "color": self.color,
            "product_name": self.product_name,
            "brand": db.session.query(Product.brand).filter_by(product_id=self.product_id).scalar(),
            "model": db.session.query(Product.model).filter_by(product_id=self.product_id).scalar(),
            "product_image": db.session.query(Product.product_image).filter_by(product_id=self.product_id).scalar(),
            "created_at": self.created_at
        }


class Cart(db.Model):
    """Cart Model"""
    __tablename__ = 'cart'
    cart_id = db.Column(db.String, primary_key=True)
    checked_out = db.Column(db.Boolean, default=False)
    created_at = db.Column(DateTime(timezone=True), default=datetime.datetime.now())

    def serialize(self):
        return {
            "cart_id": self.cart_id,
            "created_at": self.created_at
        }

    @property
    def total_amount(self) -> float:
        """Get the total amount of a cart item"""
        cart_items = db.session.query(CartItem).filter_by(cart_id=self.cart_id).all()
        total: float = 0.0

        for item in cart_items:
            product_unit_price = (db.session.query(Product.product_unit_price)
                                  .filter_by(product_id=item.product_id).scalar())
            total += item.quantity * float(product_unit_price)

        return total
