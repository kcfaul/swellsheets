from datetime import datetime
from extensions import db


class BaseModelMixin(object):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.now,
                           onupdate=datetime.now)

#
#user_product_prices = db.Table('user_product_price',
#                               db.Column('user_id', db.Integer,
#                                         db.ForeignKey('user.id')),
#                               db.Column('product_price_id', db.Integer,
#                                         db.ForeignKey('product_price.id')),
#                               )


class User(BaseModelMixin, db.Model):

    email = db.Column(db.String(127), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    admin = db.Column(db.Boolean, nullable=False, default=False)

    store_name = db.Column(db.String(127), unique=True)
    contact_name = db.Column(db.String(127), unique=True)
#    product_prices = db.relationship('ProductPrice',
#                                     secondary=user_product_prices,
#                                     backref=db.backref('users',
#                                                        lazy='dynamic')
#                                     )

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Category(BaseModelMixin, db.Model):
    name = db.Column(db.String(64), nullable=False)
    products = db.relationship('Product', backref='category', lazy='dynamic', )

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Category '{}'>".format(self.name)


class Product(BaseModelMixin, db.Model):
    name = db.Column(db.String(256), nullable=False, unique=True)
    category_id = db.Column(db.Integer(), db.ForeignKey('category.id'))
    skus = db.relationship('ProductSku', backref='product',
                           lazy='subquery')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Product '{}'>".format(self.name)


class ProductSku(BaseModelMixin, db.Model):
    sku_code = db.Column(db.String(16), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    product_id = db.Column(db.Integer(), db.ForeignKey('product.id'))
    product_name = db.Column(db.String(), db.ForeignKey('product.name'))

    prices = db.relationship('ProductPrice', backref='sku',
                             lazy='subquery', )

    cost = db.Column(db.Float())
    msrp = db.Column(db.Float())

    def __init__(self, sku_code, description):
        self.sku_code = sku_code
        self.description = description

    def __repr__(self):
        return "<SKU '{}'>".format(self.sku_code)


class PriceTier(BaseModelMixin, db.Model):
    pass


class ProductSkuPrice(BaseModelMixin, db.Model):
    product_id = db.Column(db.Integer(), db.ForeignKey('product.id'))
    price = db.Column(db.Float(), nullable=False)

    def __repr__(self):
        print "<ProductPrice '{}'>".format(self.product_id)


class OrderItem(BaseModelMixin, db.Model):
    """ attributes:
         - Sku
         - Qty
         - SkuPrice
         - line-price (dynamic?)
    """
    pass


class Order(BaseModelMixin, db.Model):
    """ attributes:
        - user
        - OrderItems (list)
        - Sub total
    """
    pass
