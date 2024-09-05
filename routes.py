from flask import request, Blueprint, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db
from config import Config
from models import User
import datetime
import jwt
import re

routes_bp = Blueprint("routes", __name__)


@routes_bp.route('/sign-in', methods=["GET", "POST"])
def sign_in():
    try:
        if request.method == "POST":
            user_id = request.form.get('email') or request.form.get('mobile_no')
            password = request.form.get('password')
            if not user_id or not password:
                return jsonify({"error": "Email and Password are required"}), 400
            if re.match(Config.EMAIL_REGEX, user_id):
                user = User.query.filter_by(email=user_id).first()
                if check_password_hash(user.password, password):
                    token = jwt.encode({
                        'user_id': user.id,
                        'exp': datetime.datetime.now() + datetime.timedelta(hours=1)
                    }, Config.SECRET_KEY)
                    return jsonify({"token": token, "message": "Sign-In Successful."}), 200
                else:
                    return jsonify({"error": "Invalid Password."}), 400
            elif re.match(Config.PHONE_REGEX, user_id):
                user = User.query.filter_by(mobile_no=user_id).first()
                if check_password_hash(user.password, password):
                    token = jwt.encode({
                        'user_id': user.id,
                        'exp': datetime.datetime.now() + datetime.timedelta(hours=1)
                    }, Config.SECRET_KEY)
                    return jsonify({"token": token, "message": "Sign-In Successful."}), 200
                else:
                    return jsonify({"error": "Invalid Password."}), 400
                
        return jsonify({"message": "Welcome to Sign-In."})

    except Exception as e:
        return jsonify({"error": "An error occurred during Sign-In", "details": str(e)})


@routes_bp.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        try:
            mobile = request.form.get('mobile')
            if not re.match(Config.PHONE_REGEX, mobile):
                return jsonify({'error': 'The Mobile Number must be 10 digits.'})
            email = request.form.get('email')
            if not re.match(Config.EMAIL_REGEX, email):
                return jsonify({'error': "Email must contain '@' and '.com'."})
            new_user = User(
                name=request.form.get('name'),
                mobile_no=mobile,
                email=email,
                password=generate_password_hash(request.form.get('password'), method='pbkdf2:sha256', salt_length=8),
                age=request.form.get('age'),
                address=request.form.get('address')
            )

            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User Created Successfully"}), 200

        except Exception as e:
            return jsonify({"error": "An error occurred during Sign-In", "details": str(e)})
    return jsonify({"message": "Welcome to Sign-Up"})
