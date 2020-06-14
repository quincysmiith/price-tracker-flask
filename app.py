from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap

# Database
import os
from flask_sqlalchemy import SQLAlchemy

# Forms
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    DecimalField,
    SelectField,
    BooleanField,
    DateField,
)
from wtforms.validators import DataRequired

from dateutil.parser import parse
from datetime import datetime
from time import sleep
import boto3
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET = os.environ.get("S3_BUCKET")
S3_KEY = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")

s3_resource = boto3.resource(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["SECRET_KEY"] = "secret"

# Database settings
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

### Database Models ###


class ProductPurchase(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(64))
    price = db.Column(db.Float())
    date = db.Column(db.Date())
    store = db.Column(db.String(64))
    location = db.Column(db.String(64))
    category = db.Column(db.String(64))
    volume = db.Column(db.Float())
    units = db.Column(db.String(15))
    special = db.Column(db.String(15))
    brand = db.Column(db.String(64))


### Forms ###


class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ItemForm(FlaskForm):
    product = StringField("Product", default="", validators=[DataRequired()])
    price = DecimalField("Price $", validators=[DataRequired()])
    date = StringField("Date")
    store = SelectField(
        "Store",
        choices=["Woolworths", "Coles", "Aldi", "Harris Farm"],
        validate_choice=False,
    )  # https://wtforms.readthedocs.io/en/2.3.x/fields/
    location = StringField("Location")
    category = StringField("Product Category")
    volume = DecimalField("Volume / Quantity of item")
    units = SelectField(
        "Units", choices=["kgs", "grams", "litres", "packets"], validate_choice=False
    )
    special = BooleanField("On special")
    brand = StringField("Brand")
    submit = SubmitField("Submit")


### Helper function ###


def parse_dates(a_string):
    try:
        date = parse(a_string)
        date = date.date()
    except:
        date = datetime.now().date()
    return date


### Routes ###


@app.route("/")
def index():
    form = NameForm()
    return render_template("index.html", form=form)


@app.route("/additem", methods=["GET", "POST"])
def input_item():
    form = ItemForm()
    # print(form.store.data)
    if form.validate_on_submit():
        print("test")
        item_log = ProductPurchase(
            product=form.product.data,
            price=form.price.data,
            date=parse_dates(form.date.data),
            store=form.store.data,
            location=form.location.data,
            category=form.category.data,
            volume=form.volume.data,
            units=form.units.data,
            special=form.special.data,
            brand=form.brand.data,
        )
        db.session.add(item_log)
        db.session.commit()
        flash("item saved to database")
        sleep(1)
        return redirect(url_for("index"))
    return render_template("additem.html", form=form)

# blob upload to amazon s3 materials
# https://kishstats.com/python/2018/03/15/flask-amazon-s3-part-2.html
# https://kishstats.com/python/2018/03/22/flask-amazon-s3-part-3.html

@app.route("/receipt")
def receipt_list_and_upload():
    """[summary]

    Returns:
        [type]: [description]
    """    

@app.route("/receipt_upload")
def upload_receipts():
    """[summary]
    """   

    file = request.files['file']
    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    my_bucket.Object(file.filename).put(Body=file)

    return "uploaded"    
