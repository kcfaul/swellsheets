from flask import request, jsonify
from flask_login import login_required, login_user

from extensions import login_manager
from core import app
from core.models import db, User


# consider moving to core/services.py?
@login_manager.user_loader
def user_loader(email):
    return User.query.filter_by(email).first()


@app.route('/')
@login_required
def index():
    return 'Hello World!'


@app.route('/api/1/register', methods=['POST'])
def register():
    json_data = request.json
    user = User(
        email=json_data['email'],
        password=json_data['password'],
    )
    try:
        db.session.add(user)
        db.session.commit()
        status = 'sucess'
    except:
        status = 'this user is already registered'
    db.session.close()
    return jsonify({'result': status})


@app.route('/api/1/auth', methods=['POST'])
def login():
    json_data = request.json
    # validation step here ?

    user = User.query.filter_by(email=json_data['email']).first()
    login(user)
