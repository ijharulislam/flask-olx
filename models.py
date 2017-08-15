from app import db
from sqlalchemy.dialects.postgresql import JSON


class OLX(db.Model):
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
    image_urls = db.Column(db.String())
    main_image_urls = db.Column(db.String())
    day = db.Column(db.String())
    month = db.Column(db.String())
    time = db.Column(db.String())
    main_category = db.Column(db.String())

    def __init__(self, url, result_all, result_no_stop_words):
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