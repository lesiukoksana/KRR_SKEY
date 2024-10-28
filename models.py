from flask_sqlalchemy import SQLAlchemy
from hashlib import sha256

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    secret = db.Column(db.String(120), nullable=False)

    def generate_one_time_passwords(self, n):
        """Генерація n одноразових паролів на основі хешування."""
        passwords = []
        current_secret = self.secret
        for i in range(n):
            current_secret = sha256((current_secret + str(i)).encode()).hexdigest()
            passwords.append(current_secret)
        return passwords
