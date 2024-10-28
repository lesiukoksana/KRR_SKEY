from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User
import pyotp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    secret = pyotp.random_base32()
    new_user = User(username=username, secret=secret)
    db.session.add(new_user)
    db.session.commit()
    flash(f'User {username} registered successfully!')
    return redirect(url_for('index'))

@app.route('/generate_otp', methods=['GET', 'POST'])
def generate_otp():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user:
            totp = pyotp.TOTP(user.secret)
            otp = totp.now()
            flash(f'OTP для користувача {username}: {otp}')
            return redirect(url_for('index'))
        flash('User not found.')
    return render_template('generate_otp.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    
    if user:
        totp = pyotp.TOTP(user.secret)
        if totp.verify(password):
            flash("Authenticated successfully!")
            return redirect(url_for('index'))
    flash("Authentication failed.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

