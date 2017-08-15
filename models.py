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
    title = db.Column(db.String())
    ads = db.Column(db.String())
    name = db.Column(db.String())
    phone = db.Column(db.String())
    phone_number = db.Column(db.String())
    price = db.Column(db.String())
    description = db.Column(db.String())
    sub_category = db.Column(db.String())
    novo_usado = db.Column(db.String())
    city = db.Column(db.String())
    suburb = db.Column(db.String())
    zipcode = db.Column(db.String())
    adcode = db.Column(db.String())
    image_urls = db.Column(JSON)
    main_image_urls = db.Column(JSON)
    day = db.Column(db.String())
    month = db.Column(db.String())
    time = db.Column(db.String())
    main_category = db.Column(db.String())

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