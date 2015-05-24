from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

#import placed after to avoid circular import errors
# models -> database models
from app import views

