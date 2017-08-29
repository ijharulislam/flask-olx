from app import db
from sqlalchemy.dialects.postgresql import JSON

from sqlalchemy.inspection import inspect

class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class OLX(db.Model, Serializer):
    __tablename__ = 'olx'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=True)
    ads = db.Column(db.String(), nullable=True)
    name = db.Column(db.String(), nullable=True)
    phone = db.Column(db.String(), nullable=True)
    phone_number = db.Column(db.String(), nullable=True)
    price = db.Column(db.String(), nullable=True)
    description = db.Column(db.String(), nullable=True)
    sub_category = db.Column(db.String(), nullable=True)
    novo_usado = db.Column(db.String(), nullable=True)
    city = db.Column(db.String(), nullable=True)
    suburb = db.Column(db.String(), nullable=True)
    zipcode = db.Column(db.String(), nullable=True)
    adcode = db.Column(db.String(), nullable=True)
    image_urls = db.Column(JSON, nullable=True)
    main_image_urls = db.Column(JSON, nullable=True)
    day = db.Column(db.String(), nullable=True)
    month = db.Column(db.String(), nullable=True)
    time = db.Column(db.String(), nullable=True)
    main_category = db.Column(db.String(), nullable=True)

    def __init__(self, title, ads, name, phone, phone_number, price, description, sub_category, novo_usado, city, suburb, zipcode, image_urls, adcode, main_image_urls, day, month, time, main_category):
        self.title = title
        self.ads = ads
        self.name = name
        self.phone = phone
        self.phone_number = phone_number
        self.price = price
        self.description = description
        self.sub_category = sub_category
        self.novo_usado = novo_usado
        self.city = city
        self.suburb = suburb
        self.zipcode = zipcode
        self.image_urls = image_urls
        self.adcode = adcode
        self.main_image_urls = main_image_urls
        self.day = day
        self.month = month
        self.time = time
        self.main_category = main_category

    def __repr__(self):
        return '<id {}>'.format(self.id)