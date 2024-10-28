from flask_sqlalchemy import SQLAlchemy
from hashlib import sha256
import os

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    secret = db.Column(db.String(120), nullable=False)

    def generate_one_time_password(self, n):
        for i in range(n):
            self.secret = sha256((self.secret + str(i)).encode()).hexdigest()
        return self.secret