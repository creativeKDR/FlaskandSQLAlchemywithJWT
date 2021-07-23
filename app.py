from functools import wraps
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import jwt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///practice.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SECRET_KEY'] = 'thisissecret'
db = SQLAlchemy(app)


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = ''
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            # current_user = User.query.filter_by(user_id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token is missing!'}), 401
        return func(*args, **kwargs)

    return decorated


@app.route('/')
def home():
    return "Hello"


@app.route('/index')
@token_required
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
